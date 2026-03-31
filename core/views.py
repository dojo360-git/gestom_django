from django.db import connection
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.utils.http import url_has_allowed_host_and_scheme
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
import calendar
import re
from collections import defaultdict
from datetime import datetime, date, timedelta

from .forms import (
    AgentForm,
    FluxForm,
    EnergieForm,
    PresenceMotifForm,
    ItineraireForm,
    VehiculeForm,
    CollecteForm,
    HeuresManuellesForm,
)
from .models import Agent, Flux, Energie, PresenceMotif, Itineraire, Vehicule, Collecte, HeuresManuelles


def home(request):
    today = timezone.localdate()

    date_debut_str = request.GET.get("date_debut")
    date_fin_str = request.GET.get("date_fin")

    def parse_date(value, default):
        if not value:
            return default
        try:
            return timezone.datetime.strptime(value, "%Y-%m-%d").date()
        except ValueError:
            return default

    date_debut = parse_date(date_debut_str, today)
    date_fin = parse_date(date_fin_str, today)

    if date_debut > date_fin:
        date_debut, date_fin = date_fin, date_debut

    sql = """
        WITH cflux AS (
            SELECT *
            FROM core_flux
        )
        
        SELECT
            cflux.flux,
            SUM(tonnages.tonnage) / 1000.0 AS tonnage,
            COUNT(*) AS nb_vidages,
            COUNT(DISTINCT tonnages.id_collecte) AS nb_tournees,
            SUM(tonnages.tonnage) / 1000.0 / NULLIF(COUNT(*), 0) AS tonnage_moyen
        FROM (
            SELECT
                id_collecte,
                date_collecte,
                id_flux1_id AS id_flux,
                tonnage1 AS tonnage
            FROM core_collecte
            WHERE tonnage1 IS NOT NULL

            UNION ALL

            SELECT
                id_collecte,
                date_collecte,
                id_flux2_id AS id_flux,
                tonnage2 AS tonnage
            FROM core_collecte
            WHERE tonnage2 IS NOT NULL

            UNION ALL

            SELECT
                id_collecte,
                date_collecte,
                id_flux3_id AS id_flux,
                tonnage3 AS tonnage
            FROM core_collecte
            WHERE tonnage3 IS NOT NULL
        ) tonnages
        LEFT JOIN cflux ON tonnages.id_flux = cflux.id_flux
        WHERE tonnages.date_collecte BETWEEN %s AND %s
        GROUP BY cflux.flux
        ORDER BY cflux.flux
    """

    with connection.cursor() as cursor:
        cursor.execute(sql, [date_debut, date_fin])
        rows = cursor.fetchall()

    stats = [
        {
            "flux": row[0],
            "tonnage": row[1],
            "nb_vidages": row[2],
            "nb_tournees": row[3],
            "tonnage_moyen": row[4],
        }
        for row in rows
    ]

    return render(
        request,
        "core/home.html",
        {
            "date_debut": date_debut,
            "date_fin": date_fin,
            "stats": stats,
        },
    )


def statistiques_collecte(request):
    today = timezone.localdate()
    first_day_of_year = today.replace(month=1, day=1)
    last_day_of_year = today.replace(month=12, day=31)

    def parse_date(value, default):
        if not value:
            return default
        try:
            return timezone.datetime.strptime(value, "%Y-%m-%d").date()
        except ValueError:
            return default

    date_debut = parse_date(request.GET.get("date_debut"), first_day_of_year)
    date_fin = parse_date(request.GET.get("date_fin"), last_day_of_year)

    if date_debut > date_fin:
        date_debut, date_fin = date_fin, date_debut

    requete_collectes = """
        SELECT
            id_collecte,
            id_vidage,
            date_collecte,
            id_vehicule_id,
            nom_vehicule,
            type_vehicule,
            id_itineraire_id,
            itineraire,
            duree_tournee,
            id_flux,
            flux,
            couleur_flux,
            tonnage,
            km,
            energie,
            energie_qte
        FROM stat_vidages
        WHERE date_collecte BETWEEN %s AND %s
        ORDER BY date_collecte, flux, id_collecte
    """

    with connection.cursor() as cursor:
        cursor.execute(requete_collectes, [date_debut, date_fin])
        columns = [col[0] for col in cursor.description]
        rows = [dict(zip(columns, row)) for row in cursor.fetchall()]
    nb_tournees = len({row.get("id_collecte") for row in rows if row.get("id_collecte") is not None})

    total_tonnage = 0.0
    total_km = 0.0
    tonnage_by_month_flux = defaultdict(lambda: defaultdict(float))
    km_by_month_flux = defaultdict(lambda: defaultdict(float))
    energie_qte_by_month_flux_energie = defaultdict(lambda: defaultdict(float))
    tournees_ids_by_month_flux = defaultdict(lambda: defaultdict(set))
    tournees_ids_by_month = defaultdict(set)
    tournees_ids_by_flux = defaultdict(set)
    tournees_ids_all = set()
    month_labels_set = set()
    colors_by_flux = {}
    fallback_palette = [
        "#16a34a",
        "#2563eb",
        "#f59e0b",
        "#dc2626",
        "#0ea5e9",
        "#9333ea",
        "#f97316",
        "#14b8a6",
    ]

    for row in rows:
        tonnage = float(row.get("tonnage") or 0)
        km = float(row.get("km") or 0)
        total_tonnage += tonnage
        total_km += km

        date_collecte = row.get("date_collecte")
        mois = date_collecte.strftime("%Y-%m") if date_collecte else "-"
        month_labels_set.add(mois)
        flux_label = row.get("flux") or f"Flux {row.get('id_flux')}" if row.get("id_flux") else "-"
        energie_label = row.get("energie") or "-"

        tonnage_by_month_flux[mois][flux_label] += tonnage
        km_by_month_flux[mois][flux_label] += km
        energie_qte = float(row.get("energie_qte") or 0)
        energie_qte_by_month_flux_energie[mois][(flux_label, energie_label)] += energie_qte
        id_collecte = row.get("id_collecte")
        if id_collecte is not None:
            tournees_ids_by_month_flux[mois][flux_label].add(id_collecte)
            tournees_ids_by_month[mois].add(id_collecte)
            tournees_ids_by_flux[flux_label].add(id_collecte)
            tournees_ids_all.add(id_collecte)

        couleur_flux = (row.get("couleur_flux") or "").strip()
        if flux_label not in colors_by_flux and couleur_flux:
            colors_by_flux[flux_label] = couleur_flux

    labels = sorted(month_labels_set)
    flux_labels = sorted({flux for month_data in tonnage_by_month_flux.values() for flux in month_data.keys()})
    energie_columns = sorted(
        {
            (flux_label, energie_label)
            for month_data in energie_qte_by_month_flux_energie.values()
            for (flux_label, energie_label) in month_data.keys()
        },
        key=lambda value: (value[0], value[1]),
    )

    energie_flux_groups = []
    for flux_label in sorted({flux_label for flux_label, _ in energie_columns}):
        energie_flux_groups.append(
            {
                "flux": flux_label,
                "count": len([1 for column_flux_label, _ in energie_columns if column_flux_label == flux_label]),
            }
        )

    pivot_rows = []
    flux_totals = [0.0 for _ in flux_labels]
    grand_total = 0.0
    for month_label in labels:
        row_cells = []
        row_total = 0.0
        for index, flux_label in enumerate(flux_labels):
            cell_value = tonnage_by_month_flux[month_label].get(flux_label, 0.0)
            row_cells.append(cell_value)
            row_total += cell_value
            flux_totals[index] += cell_value
        pivot_rows.append(
            {
                "month": month_label,
                "cells": row_cells,
                "total": row_total,
            }
        )
        grand_total += row_total

    tournees_pivot_rows = []
    tournees_flux_totals = [len(tournees_ids_by_flux.get(flux_label, set())) for flux_label in flux_labels]
    tournees_grand_total = len(tournees_ids_all)
    for month_label in labels:
        row_cells = []
        for flux_label in flux_labels:
            cell_value = len(tournees_ids_by_month_flux[month_label].get(flux_label, set()))
            row_cells.append(cell_value)
        tournees_pivot_rows.append(
            {
                "month": month_label,
                "cells": row_cells,
                "total": len(tournees_ids_by_month.get(month_label, set())),
            }
        )

    km_pivot_rows = []
    km_flux_totals = [0.0 for _ in flux_labels]
    km_grand_total = 0.0
    for month_label in labels:
        row_cells = []
        row_total = 0.0
        for index, flux_label in enumerate(flux_labels):
            cell_value = km_by_month_flux[month_label].get(flux_label, 0.0)
            row_cells.append(cell_value)
            row_total += cell_value
            km_flux_totals[index] += cell_value
        km_pivot_rows.append(
            {
                "month": month_label,
                "cells": row_cells,
                "total": row_total,
            }
        )
        km_grand_total += row_total

    energie_pivot_rows = []
    energie_column_totals = [0.0 for _ in energie_columns]
    energie_grand_total = 0.0
    for month_label in labels:
        row_cells = []
        row_total = 0.0
        for index, column in enumerate(energie_columns):
            cell_value = energie_qte_by_month_flux_energie[month_label].get(column, 0.0)
            row_cells.append(cell_value)
            row_total += cell_value
            energie_column_totals[index] += cell_value
        energie_pivot_rows.append(
            {
                "month": month_label,
                "cells": row_cells,
                "total": row_total,
            }
        )
        energie_grand_total += row_total

    datasets = []
    for index, flux_label in enumerate(flux_labels):
        raw_color = colors_by_flux.get(flux_label, "")
        if raw_color.startswith("#") and len(raw_color) in {4, 7}:
            color = raw_color
        else:
            color = fallback_palette[index % len(fallback_palette)]

        datasets.append(
            {
                "label": flux_label,
                "data": [round(tonnage_by_month_flux[label].get(flux_label, 0.0), 3) for label in labels],
                "backgroundColor": color,
            }
        )

    chart_payload = {
        "labels": labels,
        "datasets": datasets,
    }

    return render(
        request,
        "core/statistiques_collecte.html",
        {
            "date_debut": date_debut,
            "date_fin": date_fin,
            "total_tonnage": round(total_tonnage, 0),
            "total_km": round(total_km, 0),
            "nb_tournees": nb_tournees,
            "chart_payload": chart_payload,
            "flux_labels": flux_labels,
            "pivot_rows": pivot_rows,
            "flux_totals": flux_totals,
            "grand_total": grand_total,
            "tournees_pivot_rows": tournees_pivot_rows,
            "tournees_flux_totals": tournees_flux_totals,
            "tournees_grand_total": tournees_grand_total,
            "km_pivot_rows": km_pivot_rows,
            "km_flux_totals": km_flux_totals,
            "km_grand_total": km_grand_total,
            "energie_columns": [{"flux": flux_label, "energie": energie_label} for flux_label, energie_label in energie_columns],
            "energie_flux_groups": energie_flux_groups,
            "energie_pivot_rows": energie_pivot_rows,
            "energie_column_totals": energie_column_totals,
            "energie_grand_total": energie_grand_total,
            "rows": rows[:200],
        },
    )


def statistiques_absences(request):
    today = timezone.localdate()
    first_day_of_year = today.replace(month=1, day=1)
    last_day_of_year = today.replace(month=12, day=31)

    def parse_date(value, default):
        if not value:
            return default
        try:
            return timezone.datetime.strptime(value, "%Y-%m-%d").date()
        except ValueError:
            return default

    date_debut = parse_date(request.GET.get("date_debut"), first_day_of_year)
    date_fin = parse_date(request.GET.get("date_fin"), last_day_of_year)
    employeur_filtre = (request.GET.get("employeur") or "").strip()
    qualification_filtre = (request.GET.get("qualification") or "").strip()

    if date_debut > date_fin:
        date_debut, date_fin = date_fin, date_debut

    filtre_employeur_heures = ""
    filtre_employeur_absences = ""
    filtre_qualification_heures = ""
    filtre_qualification_absences = ""
    params_heures = [date_debut, date_fin]
    params_absences = [date_debut, date_fin]
    if employeur_filtre:
        filtre_employeur_heures = " AND employeur = %s"
        filtre_employeur_absences = " AND sh.employeur = %s"
        params_heures.append(employeur_filtre)
        params_absences.append(employeur_filtre)
    if qualification_filtre:
        filtre_qualification_heures = " AND qualification = %s"
        filtre_qualification_absences = " AND sh.qualification = %s"
        params_heures.append(qualification_filtre)
        params_absences.append(qualification_filtre)

    requete_heures = """
        SELECT
            id_agent,
            date,
            id_stat,
            type,
            id_flux,
            id_itineraire,
            is_heures_sup,
            hr_debut,
            hr_fin,
            motif_hs,
            presence_id,
            stat_planning,
            nom,
            employeur,
            qualification,
            service,
            background_color,
            border_color
        FROM stat_heures
        WHERE date BETWEEN %s AND %s
        {filtre_employeur_heures}
        {filtre_qualification_heures}
        ORDER BY id_agent, date, stat_planning;
    """.format(
        filtre_employeur_heures=filtre_employeur_heures,
        filtre_qualification_heures=filtre_qualification_heures,
    )

    requete_absences_par_pres = """
        SELECT
            COALESCE(pm.pres, 'Non renseigne') AS pres,
            COALESCE(pm.presence, '') AS presence,
            COALESCE(pm.couleur_hex_motif_presence, '#F1F1F1') AS background_color,
            TO_CHAR(sh.date, 'YYYY-Mon') AS annee_mois,
            DATE_TRUNC('month', sh.date)::date AS mois_date,
            COUNT(*) AS nb_absences
        FROM stat_heures sh
        LEFT JOIN core_presencemotif pm ON pm.id = sh.presence_id
        WHERE sh.presence_id IS NOT NULL
          AND sh.date BETWEEN %s AND %s
          {filtre_employeur_absences}
          {filtre_qualification_absences}
        GROUP BY pm.pres, pm.presence, pm.couleur_hex_motif_presence, annee_mois, mois_date
        ORDER BY pres, mois_date;
    """.format(
        filtre_employeur_absences=filtre_employeur_absences,
        filtre_qualification_absences=filtre_qualification_absences,
    )

    requete_employeurs = """
        SELECT DISTINCT employeur
        FROM stat_heures
        WHERE employeur IS NOT NULL
          AND employeur <> ''
        ORDER BY employeur;
    """

    requete_qualifications = """
        SELECT DISTINCT qualification
        FROM stat_heures
        WHERE qualification IS NOT NULL
          AND qualification <> ''
        ORDER BY qualification;
    """

    with connection.cursor() as cursor:
        cursor.execute(requete_heures, params_heures)
        columns_heures = [col[0] for col in cursor.description]
        rows_heures = [dict(zip(columns_heures, row)) for row in cursor.fetchall()]

        cursor.execute(requete_absences_par_pres, params_absences)
        columns_absences = [col[0] for col in cursor.description]
        absences_par_pres = [dict(zip(columns_absences, row)) for row in cursor.fetchall()]

        cursor.execute(requete_employeurs)
        employeurs = [row[0] for row in cursor.fetchall() if row[0]]

        cursor.execute(requete_qualifications)
        qualifications = [row[0] for row in cursor.fetchall() if row[0]]

    mois_fr = {
        1: "jan",
        2: "fev",
        3: "mar",
        4: "avr",
        5: "mai",
        6: "jun",
        7: "jul",
        8: "aou",
        9: "sep",
        10: "oct",
        11: "nov",
        12: "dec",
    }

    month_dates = set()
    pivot_by_pres = {}
    for row in absences_par_pres:
        month_date = row.get("mois_date")
        if month_date:
            month_dates.add(month_date)

        pres_key = row.get("pres") or "Non renseigne"
        if pres_key not in pivot_by_pres:
            pivot_by_pres[pres_key] = {
                "pres": pres_key,
                "presence": row.get("presence") or "",
                "background_color": row.get("background_color") or "#F1F1F1",
                "by_month": {},
            }
        pivot_by_pres[pres_key]["by_month"][month_date] = int(row.get("nb_absences") or 0)

    sorted_month_dates = sorted(month_dates)
    month_labels = [f"{month_date.year}-{mois_fr.get(month_date.month, '')}" for month_date in sorted_month_dates]

    absences_pivot_rows = []
    month_totals = [0 for _ in month_labels]
    total_absences = 0
    for pres_key in sorted(pivot_by_pres.keys()):
        row = pivot_by_pres[pres_key]
        cells = []
        row_total = 0
        for idx, month_date in enumerate(sorted_month_dates):
            value = int(row["by_month"].get(month_date, 0))
            cells.append(value)
            row_total += value
            month_totals[idx] += value
        total_absences += row_total
        absences_pivot_rows.append(
            {
                "pres": row["pres"],
                "presence": row["presence"],
                "background_color": row["background_color"],
                "cells": cells,
                "total": row_total,
            }
        )

    return render(
        request,
        "core/statistiques_absences.html",
        {
            "date_debut": date_debut,
            "date_fin": date_fin,
            "employeurs": employeurs,
            "employeur_filtre": employeur_filtre,
            "qualifications": qualifications,
            "qualification_filtre": qualification_filtre,
            "rows_heures_count": len(rows_heures),
            "absences_pivot_rows": absences_pivot_rows,
            "month_labels": month_labels,
            "month_totals": month_totals,
            "total_absences": total_absences,
        },
    )


def flux2(request):
    fluxes = Flux.objects.all().order_by("flux")
    create_form = FluxForm(prefix="create")
    invalid_update_id = None
    invalid_update_form = None

    if request.method == "POST":
        action = request.POST.get("action")

        if action == "create":
            create_form = FluxForm(request.POST, prefix="create")
            if create_form.is_valid():
                create_form.save()
                return redirect("core:flux2")

        elif action == "update":
            flux_id = request.POST.get("id_flux")
            flux_obj = get_object_or_404(Flux, pk=flux_id)
            update_form = FluxForm(request.POST, instance=flux_obj, prefix=f"row-{flux_obj.pk}")
            if update_form.is_valid():
                update_form.save()
                return redirect("core:flux2")
            invalid_update_id = flux_obj.pk
            invalid_update_form = update_form

        elif action == "delete":
            flux_id = request.POST.get("id_flux")
            flux_obj = get_object_or_404(Flux, pk=flux_id)
            flux_obj.delete()
            return redirect("core:flux2")

    row_forms = []
    for flux in fluxes:
        if invalid_update_id == flux.pk and invalid_update_form is not None:
            row_forms.append({"flux": flux, "form": invalid_update_form})
        else:
            row_forms.append({"flux": flux, "form": FluxForm(instance=flux, prefix=f"row-{flux.pk}")})

    return render(
        request,
        "core/flux2_list.html",
        {
            "row_forms": row_forms,
            "create_form": create_form,
        },
    )


def agents2(request):
    def _show_all() -> bool:
        return request.GET.get("all") in {"1", "true", "True"}

    def _sort_key() -> str:
        value = (request.GET.get("sort") or "nom").strip().lower()
        if value in {"service", "qualification", "nom"}:
            return value
        return "nom"

    def _selected_date():
        date_str = request.GET.get("date")
        if date_str:
            try:
                return timezone.datetime.strptime(date_str, "%Y-%m-%d").date()
            except ValueError:
                return timezone.localdate()
        return timezone.localdate()

    selected_date = _selected_date()
    show_all = _show_all()
    sort_key = _sort_key()
    sort_fields_map = {
        "nom": ("nom", "prenom"),
        "service": ("service", "nom", "prenom"),
        "qualification": ("qualification", "nom", "prenom"),
    }
    sort_fields = sort_fields_map[sort_key]

    if show_all:
        agents = Agent.objects.all().order_by(*sort_fields)
    else:
        agents = Agent.objects.filter(
            (Q(arrivee__isnull=True) | Q(arrivee__lte=selected_date))
            & (Q(depart__isnull=True) | Q(depart__gte=selected_date))
        ).order_by(*sort_fields)

    create_form = AgentForm(prefix="create")
    invalid_update_id = None
    invalid_update_form = None

    if request.method == "POST":
        action = request.POST.get("action")

        if action == "create":
            create_form = AgentForm(request.POST, prefix="create")
            if create_form.is_valid():
                create_form.save()
                return redirect("core:agents2")

        elif action == "update":
            agent_id = request.POST.get("id_agent")
            agent_obj = get_object_or_404(Agent, pk=agent_id)
            update_form = AgentForm(request.POST, instance=agent_obj, prefix=f"row-{agent_obj.pk}")
            if update_form.is_valid():
                update_form.save()
                return redirect("core:agents2")
            invalid_update_id = agent_obj.pk
            invalid_update_form = update_form

        elif action == "delete":
            agent_id = request.POST.get("id_agent")
            agent_obj = get_object_or_404(Agent, pk=agent_id)
            agent_obj.delete()
            return redirect("core:agents2")

    row_forms = []
    for agent in agents:
        if invalid_update_id == agent.pk and invalid_update_form is not None:
            row_forms.append({"agent": agent, "form": invalid_update_form})
        else:
            row_forms.append({"agent": agent, "form": AgentForm(instance=agent, prefix=f"row-{agent.pk}")})

    return render(
        request,
        "core/agents2_list.html",
        {
            "row_forms": row_forms,
            "create_form": create_form,
            "selected_date": selected_date,
            "show_all": show_all,
            "sort_key": sort_key,
        },
    )


class AgentListView(ListView):
    model = Agent
    template_name = "core/agent_list.html"
    context_object_name = "agents"

    def _show_all(self):
        return self.request.GET.get("all") in {"1", "true", "True"}

    def _selected_date(self):
        date_str = self.request.GET.get("date")
        if date_str:
            try:
                return timezone.datetime.strptime(date_str, "%Y-%m-%d").date()
            except ValueError:
                return timezone.localdate()
        return timezone.localdate()

    def get_queryset(self):
        if self._show_all():
            return Agent.objects.all().order_by("nom", "prenom")

        selected_date = self._selected_date()
        return Agent.objects.filter(
            (Q(arrivee__isnull=True) | Q(arrivee__lte=selected_date))
            & (Q(depart__isnull=True) | Q(depart__gte=selected_date))
        ).order_by("nom", "prenom")

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["selected_date"] = self._selected_date()
        ctx["show_all"] = self._show_all()
        return ctx


class AgentDetailView(DetailView):
    model = Agent
    template_name = "core/agent_detail.html"
    context_object_name = "agent"


class AgentCreateView(CreateView):
    model = Agent
    form_class = AgentForm
    template_name = "core/agent_form.html"
    success_url = reverse_lazy("core:agents2")


class AgentUpdateView(UpdateView):
    model = Agent
    form_class = AgentForm
    template_name = "core/agent_form.html"
    success_url = reverse_lazy("core:agents2")


class AgentDeleteView(DeleteView):
    model = Agent
    template_name = "core/agent_confirm_delete.html"
    success_url = reverse_lazy("core:agents2")


class FluxListView(ListView):
    model = Flux
    template_name = "core/flux_list.html"
    context_object_name = "fluxes"


class FluxDetailView(DetailView):
    model = Flux
    template_name = "core/flux_detail.html"
    context_object_name = "flux"


class FluxCreateView(CreateView):
    model = Flux
    form_class = FluxForm
    template_name = "core/flux_form.html"
    success_url = reverse_lazy("core:flux_list")

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["title"] = "Nouveau flux"
        return ctx


class FluxUpdateView(UpdateView):
    model = Flux
    form_class = FluxForm
    template_name = "core/flux_form.html"
    success_url = reverse_lazy("core:flux_list")

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["title"] = "Modifier flux"
        return ctx


class FluxDeleteView(DeleteView):
    model = Flux
    template_name = "core/flux_confirm_delete.html"
    success_url = reverse_lazy("core:flux_list")


class EnergieListView(ListView):
    model = Energie
    template_name = "core/energie_list.html"
    context_object_name = "energies"


class EnergieDetailView(DetailView):
    model = Energie
    template_name = "core/energie_detail.html"
    context_object_name = "energie"


class EnergieCreateView(CreateView):
    model = Energie
    form_class = EnergieForm
    template_name = "core/energie_form.html"
    success_url = reverse_lazy("core:energie_list")

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["title"] = "Nouvelle energie"
        return ctx


class EnergieUpdateView(UpdateView):
    model = Energie
    form_class = EnergieForm
    template_name = "core/energie_form.html"
    success_url = reverse_lazy("core:energie_list")

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["title"] = "Modifier energie"
        return ctx


class EnergieDeleteView(DeleteView):
    model = Energie
    template_name = "core/energie_confirm_delete.html"
    success_url = reverse_lazy("core:energie_list")


class PresenceMotifListView(ListView):
    model = PresenceMotif
    template_name = "core/presence_motif_list.html"
    context_object_name = "presence_motifs"


class PresenceMotifDetailView(DetailView):
    model = PresenceMotif
    template_name = "core/presence_motif_detail.html"
    context_object_name = "presence_motif"


class PresenceMotifCreateView(CreateView):
    model = PresenceMotif
    form_class = PresenceMotifForm
    template_name = "core/presence_motif_form.html"
    success_url = reverse_lazy("core:presence_motif_list")

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["title"] = "Nouveau motif de presence"
        return ctx


class PresenceMotifUpdateView(UpdateView):
    model = PresenceMotif
    form_class = PresenceMotifForm
    template_name = "core/presence_motif_form.html"
    success_url = reverse_lazy("core:presence_motif_list")

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["title"] = "Modifier motif de presence"
        return ctx


class PresenceMotifDeleteView(DeleteView):
    model = PresenceMotif
    template_name = "core/presence_motif_confirm_delete.html"
    success_url = reverse_lazy("core:presence_motif_list")


class ItineraireListView(ListView):
    model = Itineraire
    template_name = "core/itineraire_list.html"
    context_object_name = "itineraires"

    def get_queryset(self):
        return Itineraire.objects.order_by("regie", "itineraire")


class ItineraireDetailView(DetailView):
    model = Itineraire
    template_name = "core/itineraire_detail.html"
    context_object_name = "itineraire"


class ItineraireCreateView(CreateView):
    model = Itineraire
    form_class = ItineraireForm
    template_name = "core/itineraire_form.html"
    success_url = reverse_lazy("core:itineraire_list")

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["title"] = "Nouvel itineraire"
        return ctx


class ItineraireUpdateView(UpdateView):
    model = Itineraire
    form_class = ItineraireForm
    template_name = "core/itineraire_form.html"
    success_url = reverse_lazy("core:itineraire_list")

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["title"] = "Modifier itineraire"
        return ctx


class ItineraireDeleteView(DeleteView):
    model = Itineraire
    template_name = "core/itineraire_confirm_delete.html"
    success_url = reverse_lazy("core:itineraire_list")


class VehiculeListView(ListView):
    model = Vehicule
    template_name = "core/vehicule_list.html"
    context_object_name = "vehicules"

    def _show_all(self):
        return self.request.GET.get("all") in {"1", "true", "True"}

    def get_queryset(self):
        qs = Vehicule.objects.order_by("-nom_vehicule")
        if self._show_all():
            return qs
        return qs.filter(archive=False)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["show_all"] = self._show_all()
        ctx["energie_options"] = list(
            Energie.objects.exclude(energie__isnull=True)
            .exclude(energie__exact="")
            .values_list("energie", flat=True)
            .distinct()
            .order_by("energie")
        )
        return ctx


class VehiculeDetailView(DetailView):
    model = Vehicule
    template_name = "core/vehicule_detail.html"
    context_object_name = "vehicule"


class VehiculeCreateView(CreateView):
    model = Vehicule
    form_class = VehiculeForm
    template_name = "core/vehicule_form.html"
    success_url = reverse_lazy("core:vehicule_list")

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["title"] = "Nouveau vehicule"
        return ctx


class VehiculeUpdateView(UpdateView):
    model = Vehicule
    form_class = VehiculeForm
    template_name = "core/vehicule_form.html"
    success_url = reverse_lazy("core:vehicule_list")

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["title"] = "Modifier vehicule"
        return ctx


class VehiculeDeleteView(DeleteView):
    model = Vehicule
    template_name = "core/vehicule_confirm_delete.html"
    success_url = reverse_lazy("core:vehicule_list")


class CollecteListView(ListView):
    model = Collecte
    template_name = "core/collecte_list.html"
    context_object_name = "collectes"

    @staticmethod
    def _parse_date(value, default):
        if not value:
            return default
        try:
            return timezone.datetime.strptime(value, "%Y-%m-%d").date()
        except ValueError:
            return default

    def _get_date_range(self):
        today = timezone.localdate()
        date_fin = self._parse_date(self.request.GET.get("date_fin"), today)
        default_date_debut = date_fin - timedelta(days=7)
        date_debut = self._parse_date(self.request.GET.get("date_debut"), default_date_debut)

        if date_debut > date_fin:
            date_debut, date_fin = date_fin, date_debut

        return date_debut, date_fin

    def get_queryset(self):
        date_debut, date_fin = self._get_date_range()

        qs = (
            Collecte.objects.select_related(
                "id_itineraire",
                "id_agent_1",
                "id_agent_2",
                "id_agent_3",
                "id_vehicule",
                "id_flux1",
                "id_flux2",
                "id_flux3",
            )
            .filter(date_collecte__range=(date_debut, date_fin))
            .order_by("-date_collecte", "id_itineraire__itineraire", "id_collecte")
        )
        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        date_debut, date_fin = self._get_date_range()

        collectes_by_day = defaultdict(list)
        for collecte in ctx.get("collectes", []):
            km = None
            if collecte.km_depart is not None and collecte.km_retour is not None:
                km = collecte.km_retour - collecte.km_depart
            hs = None
            if collecte.hr_sup_debut and collecte.hr_sup_fin:
                hs_start = datetime.combine(date.min, collecte.hr_sup_debut)
                hs_end = datetime.combine(date.min, collecte.hr_sup_fin)
                if hs_end < hs_start:
                    hs_end += timedelta(days=1)
                hs_delta = hs_end - hs_start
                hs = max(hs_delta.total_seconds() / 3600.0, 0.0)

            tonnages = []
            for flux_field, tonnage_field in (
                ("id_flux1", "tonnage1"),
                ("id_flux2", "tonnage2"),
                ("id_flux3", "tonnage3"),
            ):
                tonnage_value = getattr(collecte, tonnage_field)
                if tonnage_value is None:
                    continue
                flux = getattr(collecte, flux_field)
                tonnages.append(
                    {
                        "value_tonnes": tonnage_value / 1000.0,
                        "background": (flux.couleur_flux if flux and flux.couleur_flux else "#e5e7eb"),
                        "flux_name": str(flux) if flux else "",
                    }
                )

            collectes_by_day[collecte.date_collecte].append(
                {
                    "obj": collecte,
                    "itineraire": collecte.id_itineraire.itineraire if collecte.id_itineraire else "-",
                    "vehicule": str(collecte.id_vehicule) if collecte.id_vehicule else "-",
                    "vehicule_title": (
                        f"Depart: {collecte.hr_depot_depart.strftime('%H:%M') if collecte.hr_depot_depart else '-'}"
                        f" | Retour: {collecte.hr_depot_retour.strftime('%H:%M') if collecte.hr_depot_retour else '-'}"
                    ),
                    "agent_1": collecte.id_agent_1.nom if collecte.id_agent_1 else "-",
                    "agent_2": collecte.id_agent_2.nom if collecte.id_agent_2 else "-",
                    "agent_3": collecte.id_agent_3.nom if collecte.id_agent_3 else "-",
                    "agent_1_title": collecte.a1_hr_fin.strftime("%H:%M") if collecte.a1_hr_fin else "-",
                    "agent_2_title": collecte.a2_hr_fin.strftime("%H:%M") if collecte.a2_hr_fin else "-",
                    "agent_3_title": collecte.a3_hr_fin.strftime("%H:%M") if collecte.a3_hr_fin else "-",
                    "km": km,
                    "km_title": (
                        f"Depart: {collecte.km_depart if collecte.km_depart is not None else '-'}"
                        f" | Retour: {collecte.km_retour if collecte.km_retour is not None else '-'}"
                    ),
                    "hs": hs,
                    "hs_title": (
                        f"{collecte.motif_heures_sup or '-'}"
                        f" | {collecte.hr_sup_debut.strftime('%H:%M') if collecte.hr_sup_debut else '-'}"
                        f" -> {collecte.hr_sup_fin.strftime('%H:%M') if collecte.hr_sup_fin else '-'}"
                    ),
                    "energie_qte": collecte.energie_qte_1,
                    "tonnages": tonnages,
                }
            )

        grouped_days = [
            {"date": day, "rows": rows}
            for day, rows in collectes_by_day.items()
        ]
        grouped_days.sort(key=lambda item: item["date"], reverse=True)

        ctx["date_debut"] = date_debut
        ctx["date_fin"] = date_fin
        ctx["collectes_by_day"] = grouped_days
        return ctx


class CollecteDetailView(DetailView):
    model = Collecte
    template_name = "core/collecte_detail.html"
    context_object_name = "collecte"


class CollecteCreateView(CreateView):
    model = Collecte
    form_class = CollecteForm
    template_name = "core/collecte_form.html"
    success_url = reverse_lazy("core:collecte_list")

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["title"] = "Nouvelle collecte"
        return ctx


class CollecteUpdateView(UpdateView):
    model = Collecte
    form_class = CollecteForm
    template_name = "core/collecte_form.html"
    success_url = reverse_lazy("core:collecte_list")

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["title"] = "Modifier collecte"
        return ctx


class CollecteDeleteView(DeleteView):
    model = Collecte
    template_name = "core/collecte_confirm_delete.html"
    success_url = reverse_lazy("core:collecte_list")


class HeuresManuellesListView(ListView):
    model = HeuresManuelles
    template_name = "core/heures_manuelles_list.html"
    context_object_name = "heures_manuelles"

    def get_queryset(self):
        date_str = self.request.GET.get("date")
        if date_str:
            try:
                selected_date = timezone.datetime.strptime(date_str, "%Y-%m-%d").date()
            except ValueError:
                selected_date = timezone.localdate()
        else:
            selected_date = timezone.localdate()

        return (
            HeuresManuelles.objects.select_related("agent")
            .filter(date=selected_date)
            .order_by("agent__nom", "agent__prenom", "heure_debut", "id")
        )

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        date_str = self.request.GET.get("date")
        if date_str:
            try:
                selected_date = timezone.datetime.strptime(date_str, "%Y-%m-%d").date()
            except ValueError:
                selected_date = timezone.localdate()
        else:
            selected_date = timezone.localdate()
        ctx["selected_date"] = selected_date
        return ctx


class HeuresManuellesDetailView(DetailView):
    model = HeuresManuelles
    template_name = "core/heures_manuelles_detail.html"
    context_object_name = "heures_manuel"


class HeuresManuellesCreateView(CreateView):
    model = HeuresManuelles
    form_class = HeuresManuellesForm
    template_name = "core/heures_manuelles_form.html"
    success_url = reverse_lazy("core:heures_manuelles_list")

    def _is_embedded(self):
        return (self.request.GET.get("embedded") or self.request.POST.get("embedded")) == "1"

    def get_template_names(self):
        if self._is_embedded():
            return ["core/heures_manuelles_form_embedded.html"]
        return [self.template_name]

    def _get_next_url(self):
        next_url = self.request.POST.get("next") or self.request.GET.get("next") or ""
        if not next_url:
            return ""
        if not url_has_allowed_host_and_scheme(
            url=next_url,
            allowed_hosts={self.request.get_host()},
            require_https=self.request.is_secure(),
        ):
            return ""
        return next_url

    def get_success_url(self):
        return self._get_next_url() or str(self.success_url)

    def get_initial(self):
        initial = super().get_initial()
        agent_id = self.request.GET.get("agent")
        date_str = self.request.GET.get("date")
        if agent_id:
            initial["agent"] = agent_id
        if date_str:
            try:
                initial["date"] = timezone.datetime.strptime(date_str, "%Y-%m-%d").date()
            except ValueError:
                pass
        return initial

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["title"] = "Nouvelle heure manuelle"
        ctx["next_url"] = self._get_next_url()
        ctx["embedded"] = self._is_embedded()
        ctx["form_action"] = self.request.get_full_path()
        ctx["delete_url"] = ""
        return ctx


class HeuresManuellesUpdateView(UpdateView):
    model = HeuresManuelles
    form_class = HeuresManuellesForm
    template_name = "core/heures_manuelles_form.html"
    success_url = reverse_lazy("core:heures_manuelles_list")

    def _is_embedded(self):
        return (self.request.GET.get("embedded") or self.request.POST.get("embedded")) == "1"

    def get_template_names(self):
        if self._is_embedded():
            return ["core/heures_manuelles_form_embedded.html"]
        return [self.template_name]

    def _get_next_url(self):
        next_url = self.request.POST.get("next") or self.request.GET.get("next") or ""
        if not next_url:
            return ""
        if not url_has_allowed_host_and_scheme(
            url=next_url,
            allowed_hosts={self.request.get_host()},
            require_https=self.request.is_secure(),
        ):
            return ""
        return next_url

    def get_success_url(self):
        return self._get_next_url() or str(self.success_url)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["title"] = "Modifier heure manuelle"
        ctx["next_url"] = self._get_next_url()
        ctx["embedded"] = self._is_embedded()
        ctx["form_action"] = self.request.get_full_path()
        ctx["delete_url"] = reverse_lazy("core:heures_manuelles_delete", kwargs={"pk": self.object.pk})
        return ctx


class HeuresManuellesDeleteView(DeleteView):
    model = HeuresManuelles
    template_name = "core/heures_manuelles_confirm_delete.html"
    success_url = reverse_lazy("core:heures_manuelles_list")

    def _get_next_url(self):
        next_url = self.request.POST.get("next") or self.request.GET.get("next") or ""
        if not next_url:
            return ""
        if not url_has_allowed_host_and_scheme(
            url=next_url,
            allowed_hosts={self.request.get_host()},
            require_https=self.request.is_secure(),
        ):
            return ""
        return next_url

    def get_success_url(self):
        return self._get_next_url() or str(self.success_url)


def planning(request):
    today = timezone.localdate()
    date_str = request.GET.get("date")
    if date_str:
        try:
            selected_date = timezone.datetime.strptime(date_str, "%Y-%m-%d").date()
        except ValueError:
            selected_date = today
    else:
        selected_date = today

    month_start = selected_date.replace(day=1)
    last_day = calendar.monthrange(selected_date.year, selected_date.month)[1]
    month_end = selected_date.replace(day=last_day)
    days = [month_start + timezone.timedelta(days=offset) for offset in range(last_day)]

    agents = list(
        Agent.objects.filter(
            (Q(arrivee__isnull=True) | Q(arrivee__lte=month_end))
            & (Q(depart__isnull=True) | Q(depart__gte=month_start))
        ).order_by("service", "qualification", "nom", "prenom")
    )

    def _safe_hex_color(raw_value, fallback):
        value = (raw_value or "").strip()
        if re.fullmatch(r"#[0-9A-Fa-f]{6}([0-9A-Fa-f]{2})?", value):
            return value
        return fallback

    sql = """
        SELECT
            id_agent,
            date,
            id_stat,
            type,
            id_flux,
            id_itineraire,
            is_heures_sup,
            hr_debut,
            hr_fin,
            motif_hs,
            presence_id,
            stat_planning,
            nom,
            employeur,
            qualification,
            service,
            background_color,
            border_color
        FROM stat_heures
        WHERE date BETWEEN %s AND %s
        ORDER BY id_agent, date, stat_planning;
    """

    entries_map = defaultdict(list)
    with connection.cursor() as cursor:
        cursor.execute(sql, [month_start, month_end])
        columns = [col[0] for col in cursor.description]
        for row in cursor.fetchall():
            item = dict(zip(columns, row))
            stat_label = item.get("stat_planning") or ""
            entries_map[(item["id_agent"], item["date"])].append(
                {
                    "id_stat": item["id_stat"],
                    "type": item.get("type") or "",
                    "stat_label": stat_label,
                    "background_color": _safe_hex_color(item.get("background_color"), "#F1F1F1"),
                    "border_color": _safe_hex_color(item.get("border_color"), "#666666"),
                    "width_px": max(26, min(180, 10 + (len(str(stat_label)) * 9))),
                }
            )

    table_rows = []
    for agent in agents:
        day_cells = [
            {
                "day": day,
                "entries": entries_map.get((agent.id, day), []),
            }
            for day in days
        ]
        table_rows.append({"agent": agent, "day_cells": day_cells})

    return render(
        request,
        "core/planning.html",
        {
            "selected_date": selected_date,
            "days": days,
            "rows": table_rows,
        },
    )
