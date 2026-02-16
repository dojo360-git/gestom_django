from django.db import connection
from django.db.models import Q
from django.shortcuts import render
from django.utils import timezone
from django.utils.http import url_has_allowed_host_and_scheme
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
import calendar
from collections import defaultdict

from .forms import AgentForm, FluxForm, EnergieForm, PresenceMotifForm, VehiculeForm, CollecteForm, HeuresManuellesForm
from .models import Agent, Flux, Energie, PresenceMotif, Vehicule, Collecte, HeuresManuelles


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


class AgentListView(ListView):
    model = Agent
    template_name = "core/agent_list.html"
    context_object_name = "agents"

    def _selected_date(self):
        date_str = self.request.GET.get("date")
        if date_str:
            try:
                return timezone.datetime.strptime(date_str, "%Y-%m-%d").date()
            except ValueError:
                return timezone.localdate()
        return timezone.localdate()

    def get_queryset(self):
        selected_date = self._selected_date()
        return Agent.objects.filter(
            (Q(arrivee__isnull=True) | Q(arrivee__lte=selected_date))
            & (Q(depart__isnull=True) | Q(depart__gte=selected_date))
        ).order_by("nom", "prenom")

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["selected_date"] = self._selected_date()
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


class VehiculeListView(ListView):
    model = Vehicule
    template_name = "core/vehicule_list.html"
    context_object_name = "vehicules"


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
                "id_energie_1",
                "id_energie_2",
                "id_energie_3",
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
        return ctx


class HeuresManuellesDeleteView(DeleteView):
    model = HeuresManuelles
    template_name = "core/heures_manuelles_confirm_delete.html"
    success_url = reverse_lazy("core:heures_manuelles_list")


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
