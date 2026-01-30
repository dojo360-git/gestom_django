from django.urls import path

from . import views, views_api
from .views import (
    AgentListView, AgentDetailView, AgentCreateView, AgentUpdateView, AgentDeleteView,
    FluxListView, FluxDetailView, FluxCreateView, FluxUpdateView, FluxDeleteView,
    EnergieListView, EnergieDetailView, EnergieCreateView, EnergieUpdateView, EnergieDeleteView,
    VehiculeListView, VehiculeDetailView, VehiculeCreateView, VehiculeUpdateView, VehiculeDeleteView,
    CollecteListView, CollecteDetailView, CollecteCreateView, CollecteUpdateView, CollecteDeleteView,
    PlanningView,
)

app_name = "core"


urlpatterns = [
    # Home
    path("", views.home, name="home"),
    path("planning/", PlanningView.as_view(), name="planning"),
    path("agents/", AgentListView.as_view(), name="agent_list"),

    # Agents
    path("agents/nouveau/", AgentCreateView.as_view(), name="agent_create"),
    path("agents/<int:pk>/", AgentDetailView.as_view(), name="agent_detail"),
    path("agents/<int:pk>/modifier/", AgentUpdateView.as_view(), name="agent_update"),
    path("agents/<int:pk>/supprimer/", AgentDeleteView.as_view(), name="agent_delete"),

    # Vehicules
    path("vehicules/", VehiculeListView.as_view(), name="vehicule_list"),
    path("vehicules/nouveau/", VehiculeCreateView.as_view(), name="vehicule_create"),
    path("vehicules/<int:pk>/", VehiculeDetailView.as_view(), name="vehicule_detail"),
    path("vehicules/<int:pk>/modifier/", VehiculeUpdateView.as_view(), name="vehicule_update"),
    path("vehicules/<int:pk>/supprimer/", VehiculeDeleteView.as_view(), name="vehicule_delete"),

    # Collectes
    path("collectes/", CollecteListView.as_view(), name="collecte_list"),
    path("collectes/nouveau/", CollecteCreateView.as_view(), name="collecte_create"),
    path("collectes/<int:pk>/", CollecteDetailView.as_view(), name="collecte_detail"),
    path("collectes/<int:pk>/modifier/", CollecteUpdateView.as_view(), name="collecte_update"),
    path("collectes/<int:pk>/supprimer/", CollecteDeleteView.as_view(), name="collecte_delete"),

    # Flux
    path("flux/", FluxListView.as_view(), name="flux_list"),
    path("flux/nouveau/", FluxCreateView.as_view(), name="flux_create"),
    path("flux/<int:pk>/", FluxDetailView.as_view(), name="flux_detail"),
    path("flux/<int:pk>/modifier/", FluxUpdateView.as_view(), name="flux_update"),
    path("flux/<int:pk>/supprimer/", FluxDeleteView.as_view(), name="flux_delete"),

    # Energies
    path("energies/", EnergieListView.as_view(), name="energie_list"),
    path("energies/nouveau/", EnergieCreateView.as_view(), name="energie_create"),
    path("energies/<int:pk>/", EnergieDetailView.as_view(), name="energie_detail"),
    path("energies/<int:pk>/modifier/", EnergieUpdateView.as_view(), name="energie_update"),
    path("energies/<int:pk>/supprimer/", EnergieDeleteView.as_view(), name="energie_delete"),

    # API
    #path("api/tonnages_json/", views_api.tonnages_json, name="home"),

]
