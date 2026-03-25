from django.db import connection
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.utils.http import url_has_allowed_host_and_scheme
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
import calendar
from collections import defaultdict

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


def donnee_collectes(request):
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
        WITH cflux AS (
            SELECT *
            FROM core_flux
        ),
        tournees AS (
            SELECT
                id_collecte,
                COALESCE(km_retour - km_depart, 0) AS km_tournee,
                COALESCE(tonnage1, 0) + COALESCE(tonnage2, 0) + COALESCE(tonnage3, 0) AS tonnage_tournee,
                energie_qte_1 AS energie_qte_1_tournee
            FROM core_collecte
        ),
        vidages AS (
            SELECT
                t.id_collecte,
                t.date_collecte,
                t.id_flux,
                t.tonnage
            FROM (
                SELECT id_collecte, date_collecte, id_flux1_id AS id_flux, tonnage1 AS tonnage
                FROM core_collecte
                WHERE tonnage1 IS NOT NULL

                UNION ALL

                SELECT id_collecte, date_collecte, id_flux2_id AS id_flux, tonnage2 AS tonnage
                FROM core_collecte
                WHERE tonnage2 IS NOT NULL

                UNION ALL

                SELECT id_collecte, date_collecte, id_flux3_id AS id_flux, tonnage3 AS tonnage
                FROM core_collecte
                WHERE tonnage3 IS NOT NULL
            ) t
        ),
        vidages2 AS (
            SELECT
                v.id_collecte,
                v.date_collecte,
                v.id_flux,
                (v.tonnage / 1000)::numeric AS tonnage,
                tr.km_tournee,
                tr.tonnage_tournee,
                tr.energie_qte_1_tournee,
                CASE
                    WHEN NULLIF(tr.tonnage_tournee, 0) IS NULL THEN 0
                    ELSE round((v.tonnage / NULLIF(tr.tonnage_tournee, 0))::numeric, 6)
                END AS ventil
            FROM vidages v
            LEFT JOIN tournees tr ON tr.id_collecte = v.id_collecte
        )
        SELECT
            v2.*,
            cflux.flux,
            cflux.couleur_flux,
            round((v2.km_tournee * v2.ventil)::numeric, 6) AS km,
            round((v2.energie_qte_1_tournee * v2.ventil)::numeric, 6) AS energie_qte_1
        FROM vidages2 v2
        LEFT JOIN cflux ON cflux.id_flux = v2.id_flux
        WHERE v2.date_collecte BETWEEN %s AND %s
        ORDER BY v2.date_collecte, cflux.flux, v2.id_collecte
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
    tournees_ids_by_month_flux = defaultdict(lambda: defaultdict(set))
    tournees_ids_by_month = defaultdict(set)
    tournees_ids_by_flux = defaultdict(set)
    tournees_ids_all = set()
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
        mois = date_collecte.strftime("%Y-%m") if date_collecte else "Sans date"
        flux_label = row.get("flux") or f"Flux {row.get('id_flux')}" if row.get("id_flux") else "Flux non renseigne"

        tonnage_by_month_flux[mois][flux_label] += tonnage
        km_by_month_flux[mois][flux_label] += km
        id_collecte = row.get("id_collecte")
        if id_collecte is not None:
            tournees_ids_by_month_flux[mois][flux_label].add(id_collecte)
            tournees_ids_by_month[mois].add(id_collecte)
            tournees_ids_by_flux[flux_label].add(id_collecte)
            tournees_ids_all.add(id_collecte)

        couleur_flux = (row.get("couleur_flux") or "").strip()
        if flux_label not in colors_by_flux and couleur_flux:
            colors_by_flux[flux_label] = couleur_flux

    labels = sorted(tonnage_by_month_flux.keys())
    flux_labels = sorted({flux for month_data in tonnage_by_month_flux.values() for flux in month_data.keys()})

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
        for index, flux_label in enumerate(flux_labels):
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
        "core/donnee_collectes.html",
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
            "rows": rows[:200],
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

    if show_all:
        agents = Agent.objects.all().order_by("nom", "prenom")
    else:
        agents = Agent.objects.filter(
            (Q(arrivee__isnull=True) | Q(arrivee__lte=selected_date))
            & (Q(depart__isnull=True) | Q(depart__gte=selected_date))
        ).order_by("nom", "prenom")

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
    success_url = reverse_lazy("core:agent_list")


class AgentUpdateView(UpdateView):
    model = Agent
    form_class = AgentForm
    template_name = "core/agent_form.html"
    success_url = reverse_lazy("core:agent_list")


class AgentDeleteView(DeleteView):
    model = Agent
    template_name = "core/agent_confirm_delete.html"
    success_url = reverse_lazy("core:agent_list")


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

    def get_queryset(self):
        return Vehicule.objects.order_by("-nom_vehicule")

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
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

    def get_queryset(self):
        date_str = self.request.GET.get("date")
        if date_str:
            try:
                selected_date = timezone.datetime.strptime(date_str, "%Y-%m-%d").date()
            except ValueError:
                selected_date = timezone.localdate()
        else:
            selected_date = timezone.localdate()

        qs = (
            Collecte.objects.select_related(
                "id_agent_1",
                "id_agent_2",
                "id_agent_3",
                "id_vehicule",
                "id_flux1",
                "id_flux2",
                "id_flux3",
            )
            .filter(date_collecte=selected_date)
        )
        return qs

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


class PlanningView(TemplateView):
    template_name = "core/planning.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        agents_qs = Agent.objects.all().order_by("nom")
        ctx["agents"] = list(agents_qs.values("id", "nom", "qualification"))
        return ctx


def planning3(request):
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

    sql = """
        WITH hr_manuelles AS (
            SELECT
                CASE
                    WHEN COALESCE(NULLIF(BTRIM(motif_heures_sup), ''), '') <> '' THEN 'Heures Sup'
                    ELSE 'Manuelles'
                END AS type,
                id AS id_stat,
                agent_id AS id_agent,
                date,
                heure_debut AS hr_debut,
                heure_fin AS hr_fin,
                presence
            FROM core_heuresmanuelles
        ),
        hr_collecte AS (
            SELECT
                'collecte' AS type,
                id_collecte AS id_stat,
                id_agent_1_id AS id_agent,
                date_collecte AS date,
                a1_hr_debut AS hr_debut,
                a1_hr_fin AS hr_fin,
                '' AS presence
            FROM core_collecte
            WHERE id_agent_1_id IS NOT NULL

            UNION ALL

            SELECT
                'collecte' AS type,
                id_collecte AS id_stat,
                id_agent_2_id AS id_agent,
                date_collecte AS date,
                a2_hr_debut AS hr_debut,
                a2_hr_fin AS hr_fin,
                '' AS presence
            FROM core_collecte
            WHERE id_agent_2_id IS NOT NULL

            UNION ALL

            SELECT
                'collecte' AS type,
                id_collecte AS id_stat,
                id_agent_3_id AS id_agent,
                date_collecte AS date,
                a3_hr_debut AS hr_debut,
                a3_hr_fin AS hr_fin,
                '' AS presence
            FROM core_collecte
            WHERE id_agent_3_id IS NOT NULL
        ),
        entries AS (
            SELECT * FROM hr_collecte
            UNION ALL
            SELECT * FROM hr_manuelles
        )
        SELECT
            id_agent,
            date,
            type,
            id_stat,
            CASE
                WHEN COALESCE(NULLIF(BTRIM(presence), ''), '') <> '' THEN presence
                WHEN hr_fin IS NOT NULL THEN TO_CHAR(hr_fin, 'HH24:MI')
                ELSE ''
            END AS stat
        FROM entries
        WHERE date BETWEEN %s AND %s
        ORDER BY id_agent, date, stat;
    """

    entries_map = defaultdict(list)
    with connection.cursor() as cursor:
        cursor.execute(sql, [month_start, month_end])
        for agent_id, date_value, entry_type, id_stat, stat in cursor.fetchall():
            stat_value = stat #float(stat or 0)
            entries_map[(agent_id, date_value)].append(
                {
                    "type": entry_type,
                    "id_stat": id_stat,
                    "stat": stat,
                    "stat_label": stat,
                    "width_class": "planning3__w-100"
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
        "core/planning3.html",
        {
            "selected_date": selected_date,
            "days": days,
            "rows": table_rows,
        },
    )


def planning2(request):
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
    days = [
        month_start + timezone.timedelta(days=offset)
        for offset in range(last_day)
    ]

    agents = list(
        Agent.objects.order_by("qualification", "nom", "prenom")
    )

    sql = """
    WITH 
               collecte AS (
        SELECT
            'collecte' type,
            id_collecte,
            id_agent_1_id AS id_agent,
            date_collecte AS date,
            a1_hr_debut AS hr_debut,
            a1_hr_fin AS hr_fin
        FROM core_collecte
        WHERE id_agent_1_id IS NOT NULL

        UNION ALL

        SELECT
            'Manuelles' type, 
            id_collecte,
            id_agent_2_id AS id_agent,
            date_collecte AS date,
            a2_hr_debut AS hr_debut,
            a2_hr_fin AS hr_fin
        FROM core_collecte
        WHERE id_agent_2_id IS NOT NULL

        UNION ALL

        SELECT
            'Heures Sup' type,
            id_collecte,
            id_agent_3_id AS id_agent,
            date_collecte AS date,
            a3_hr_debut AS hr_debut,
            a3_hr_fin AS hr_fin
        FROM core_collecte
        WHERE id_agent_3_id IS NOT NULL
    )
    SELECT
        type,
        id_collecte,
        id_agent,
        date,
        CASE
            WHEN hr_debut IS NOT NULL AND hr_fin IS NOT NULL THEN
                round((
                    (EXTRACT(EPOCH FROM (hr_fin - hr_debut))::bigint + 86400)
                    % 86400
                )/3600,1)
            ELSE 0
        END AS duree_heure
    FROM collecte
        WHERE date BETWEEN %s AND %s
        GROUP BY id_agent, date
    """

    with connection.cursor() as cursor:
        cursor.execute(sql, [month_start, month_end])
        rows = cursor.fetchall()

    durations_map = {}
    for agent_id, date_value, duree_sec in rows:
        if not duree_sec:
            continue
        total_minutes = int(duree_sec // 60)
        hours = total_minutes // 60
        minutes = total_minutes % 60
        durations_map[(agent_id, date_value)] = f"{hours:02d}:{minutes:02d}"

    table_rows = []
    for agent in agents:
        durations = [
            durations_map.get((agent.id, day), "")
            for day in days
        ]
        table_rows.append({"agent": agent, "durations": durations})

    return render(
        request,
        "core/planning2.html",
        {
            "selected_date": selected_date,
            "days": days,
            "rows": table_rows,
        },
    )
