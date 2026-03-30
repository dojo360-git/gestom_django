from django.urls import path
from django.contrib.auth.decorators import login_required

from . import views, views_api
from .views import (
    AgentDetailView, AgentCreateView, AgentUpdateView, AgentDeleteView,
    EnergieListView, EnergieDetailView, EnergieCreateView, EnergieUpdateView, EnergieDeleteView,
    PresenceMotifListView, PresenceMotifDetailView, PresenceMotifCreateView, PresenceMotifUpdateView, PresenceMotifDeleteView,
    ItineraireListView, ItineraireDetailView, ItineraireCreateView, ItineraireUpdateView, ItineraireDeleteView,
    VehiculeListView, VehiculeDetailView, VehiculeCreateView, VehiculeUpdateView, VehiculeDeleteView,
    CollecteListView, CollecteDetailView, CollecteCreateView, CollecteUpdateView, CollecteDeleteView,
    HeuresManuellesListView, HeuresManuellesDetailView, HeuresManuellesCreateView, HeuresManuellesUpdateView, HeuresManuellesDeleteView,
    planning,
)

app_name = "core"


urlpatterns = [
    # Home
    path("", login_required(views.home), name="home"),
    path("statistiques_collecte/", login_required(views.statistiques_collecte), name="statistiques_collecte"),
    path("statistiques_heures/", login_required(views.statistiques_heures), name="statistiques_heures"),
    path("planning/", login_required(planning), name="planning"),
    path("agents/", login_required(views.agents2), name="agents2"),

    # Agents
    path("agents/nouveau/", login_required(AgentCreateView.as_view()), name="agent_create"),
    path("agents/<int:pk>/", login_required(AgentDetailView.as_view()), name="agent_detail"),
    path("agents/<int:pk>/modifier/", login_required(AgentUpdateView.as_view()), name="agent_update"),
    path("agents/<int:pk>/supprimer/", login_required(AgentDeleteView.as_view()), name="agent_delete"),

    # Vehicules
    path("vehicules/", login_required(VehiculeListView.as_view()), name="vehicule_list"),
    path("vehicules/nouveau/", login_required(VehiculeCreateView.as_view()), name="vehicule_create"),
    path("vehicules/<int:pk>/", login_required(VehiculeDetailView.as_view()), name="vehicule_detail"),
    path("vehicules/<int:pk>/modifier/", login_required(VehiculeUpdateView.as_view()), name="vehicule_update"),
    path("vehicules/<int:pk>/supprimer/", login_required(VehiculeDeleteView.as_view()), name="vehicule_delete"),

    # Collectes
    path("collectes/", login_required(CollecteListView.as_view()), name="collecte_list"),
    path("collectes/nouveau/", login_required(CollecteCreateView.as_view()), name="collecte_create"),
    path("collectes/<int:pk>/", login_required(CollecteDetailView.as_view()), name="collecte_detail"),
    path("collectes/<int:pk>/modifier/", login_required(CollecteUpdateView.as_view()), name="collecte_update"),
    path("collectes/<int:pk>/supprimer/", login_required(CollecteDeleteView.as_view()), name="collecte_delete"),

    # Heures manuelles
    path("heures-manuelles/", login_required(HeuresManuellesListView.as_view()), name="heures_manuelles_list"),
    path("heures-manuelles/nouveau/", login_required(HeuresManuellesCreateView.as_view()), name="heures_manuelles_create"),
    path("heures-manuelles/<int:pk>/", login_required(HeuresManuellesDetailView.as_view()), name="heures_manuelles_detail"),
    path("heures-manuelles/<int:pk>/modifier/", login_required(HeuresManuellesUpdateView.as_view()), name="heures_manuelles_update"),
    path("heures-manuelles/<int:pk>/supprimer/", login_required(HeuresManuellesDeleteView.as_view()), name="heures_manuelles_delete"),

    # Flux (edition rapide uniquement)
    path("flux/", login_required(views.flux2), name="flux2"),

    # Energies
    path("energies/", login_required(EnergieListView.as_view()), name="energie_list"),
    path("energies/nouveau/", login_required(EnergieCreateView.as_view()), name="energie_create"),
    path("energies/<int:pk>/", login_required(EnergieDetailView.as_view()), name="energie_detail"),
    path("energies/<int:pk>/modifier/", login_required(EnergieUpdateView.as_view()), name="energie_update"),
    path("energies/<int:pk>/supprimer/", login_required(EnergieDeleteView.as_view()), name="energie_delete"),

    # Presence motifs
    path("presence-motifs/", login_required(PresenceMotifListView.as_view()), name="presence_motif_list"),
    path("presence-motifs/nouveau/", login_required(PresenceMotifCreateView.as_view()), name="presence_motif_create"),
    path("presence-motifs/<int:pk>/", login_required(PresenceMotifDetailView.as_view()), name="presence_motif_detail"),
    path("presence-motifs/<int:pk>/modifier/", login_required(PresenceMotifUpdateView.as_view()), name="presence_motif_update"),
    path("presence-motifs/<int:pk>/supprimer/", login_required(PresenceMotifDeleteView.as_view()), name="presence_motif_delete"),

    # Itineraires
    path("itineraires/", login_required(ItineraireListView.as_view()), name="itineraire_list"),
    path("itineraires/nouveau/", login_required(ItineraireCreateView.as_view()), name="itineraire_create"),
    path("itineraires/<int:pk>/", login_required(ItineraireDetailView.as_view()), name="itineraire_detail"),
    path("itineraires/<int:pk>/modifier/", login_required(ItineraireUpdateView.as_view()), name="itineraire_update"),
    path("itineraires/<int:pk>/supprimer/", login_required(ItineraireDeleteView.as_view()), name="itineraire_delete"),

    # API
    path("api/tonnages_json/", login_required(views_api.tonnages_json), name="tonnages_json"),

]
