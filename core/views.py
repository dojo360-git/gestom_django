from django.db import connection
from django.shortcuts import render
from django.utils import timezone
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView

from .forms import AgentForm, FluxForm, EnergieForm, PresenceMotifForm, VehiculeForm, CollecteForm
from .models import Agent, Flux, Energie, PresenceMotif, Vehicule, Collecte


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


class PlanningView(TemplateView):
    template_name = "core/planning.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        agents_qs = Agent.objects.all().order_by("nom")
        ctx["agents"] = list(agents_qs.values("id", "nom", "qualification"))
        return ctx
