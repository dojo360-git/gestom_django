from django.urls import path
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required

from . import views, views_api
from .views import (
    AgentDetailView, AgentCreateView, AgentUpdateView, AgentDeleteView,
    EnergieListView, EnergieDetailView, EnergieCreateView, EnergieUpdateView, EnergieDeleteView,
    PresenceMotifListView, PresenceMotifDetailView, PresenceMotifCreateView, PresenceMotifUpdateView, PresenceMotifDeleteView,
    ItineraireListView, ItineraireDetailView, ItineraireCreateView, ItineraireUpdateView, ItineraireDeleteView,
    VehiculeListView, VehiculeDetailView, VehiculeCreateView, VehiculeUpdateView, VehiculeDeleteView,
    CollecteListView, CollecteDetailView, CollecteCreateView, CollecteUpdateView, CollecteDeleteView,
    HeuresManuellesListView, HeuresManuellesDetailView, HeuresManuellesCreateView, HeuresManuellesUpdateView, HeuresManuellesDeleteView,
    TacheUpdateView,
    ParametreListCreateView,
    planning,
    calendrier,
)

app_name = "core"


def login_and_perm(permission, view):
    return login_required(permission_required(permission, raise_exception=True)(view))


urlpatterns = [
    # Home
    path("", login_required(views.home), name="home"),
    path("statistiques_collecte/", login_required(views.statistiques_collecte), name="statistiques_collecte"),
    path("statistiques_hercule/", login_required(views.statistiques_hercule), name="statistiques_hercule"),
    path("statistiques_absences/", login_required(views.statistiques_absences), name="statistiques_absences"),
    path("statistiques_heure_sup/", login_required(views.statistiques_heure_sup), name="statistiques_heure_sup"),
    path("statistiques_hpne/", login_required(views.statistiques_hpne), name="statistiques_hpne"),
    path("statistiques_agents/", login_required(views.statistiques_agents), name="statistiques_agents"),
    path("planning/", login_required(planning), name="planning"),
    path("calendrier/", login_and_perm("core.view_tache", calendrier), name="calendrier"),
    path("previsions-semaines/", login_and_perm("core.view_collectprev", views.previsions_semaines), name="previsions_semaines"),
    path("previsions-jour/", login_and_perm("core.view_collectprev", views.previsions_jour), name="previsions_jour"),
    path("agents/", login_and_perm("core.view_agent", views.agents2), name="agents2"),

    # Agents
    path("agents/nouveau/", login_and_perm("core.add_agent", AgentCreateView.as_view()), name="agent_create"),
    path("agents/<int:pk>/", login_and_perm("core.view_agent", AgentDetailView.as_view()), name="agent_detail"),
    path("agents/<int:pk>/modifier/", login_and_perm("core.change_agent", AgentUpdateView.as_view()), name="agent_update"),
    path("agents/<int:pk>/supprimer/", login_and_perm("core.delete_agent", AgentDeleteView.as_view()), name="agent_delete"),

    # Vehicules
    path("vehicules/", login_and_perm("core.view_vehicule", VehiculeListView.as_view()), name="vehicule_list"),
    path("vehicules/nouveau/", login_and_perm("core.add_vehicule", VehiculeCreateView.as_view()), name="vehicule_create"),
    path("vehicules/<int:pk>/", login_and_perm("core.view_vehicule", VehiculeDetailView.as_view()), name="vehicule_detail"),
    path("vehicules/<int:pk>/modifier/", login_and_perm("core.change_vehicule", VehiculeUpdateView.as_view()), name="vehicule_update"),
    path("vehicules/<int:pk>/supprimer/", login_and_perm("core.delete_vehicule", VehiculeDeleteView.as_view()), name="vehicule_delete"),

    # Collectes
    path("collectes/", login_and_perm("core.view_collecte", CollecteListView.as_view()), name="collecte_list"),
    path("collectes/nouveau/", login_and_perm("core.add_collecte", CollecteCreateView.as_view()), name="collecte_create"),
    path("collectes/<int:pk>/", login_and_perm("core.view_collecte", CollecteDetailView.as_view()), name="collecte_detail"),
    path("collectes/<int:pk>/modifier/", login_and_perm("core.change_collecte", CollecteUpdateView.as_view()), name="collecte_update"),
    path("collectes/<int:pk>/supprimer/", login_and_perm("core.delete_collecte", CollecteDeleteView.as_view()), name="collecte_delete"),

    # Heures manuelles
    path("heures-manuelles/", login_and_perm("core.view_heuresmanuelles", HeuresManuellesListView.as_view()), name="heures_manuelles_list"),
    path("heures-manuelles/nouveau/", login_and_perm("core.add_heuresmanuelles", HeuresManuellesCreateView.as_view()), name="heures_manuelles_create"),
    path("heures-manuelles/<int:pk>/", login_and_perm("core.view_heuresmanuelles", HeuresManuellesDetailView.as_view()), name="heures_manuelles_detail"),
    path("heures-manuelles/<int:pk>/modifier/", login_and_perm("core.change_heuresmanuelles", HeuresManuellesUpdateView.as_view()), name="heures_manuelles_update"),
    path("heures-manuelles/<int:pk>/supprimer/", login_and_perm("core.delete_heuresmanuelles", HeuresManuellesDeleteView.as_view()), name="heures_manuelles_delete"),

    # Taches
    path("taches/<int:pk>/modifier/", login_and_perm("core.change_tache", TacheUpdateView.as_view()), name="tache_update"),

    # Flux (edition rapide uniquement)
    path("flux/", login_and_perm("core.view_flux", views.flux2), name="flux2"),

    # Energies
    path("energies/", login_and_perm("core.view_energie", EnergieListView.as_view()), name="energie_list"),
    path("energies/nouveau/", login_and_perm("core.add_energie", EnergieCreateView.as_view()), name="energie_create"),
    path("energies/<int:pk>/", login_and_perm("core.view_energie", EnergieDetailView.as_view()), name="energie_detail"),
    path("energies/<int:pk>/modifier/", login_and_perm("core.change_energie", EnergieUpdateView.as_view()), name="energie_update"),
    path("energies/<int:pk>/supprimer/", login_and_perm("core.delete_energie", EnergieDeleteView.as_view()), name="energie_delete"),

    # Presence motifs
    path("presence-motifs/", login_and_perm("core.view_presencemotif", PresenceMotifListView.as_view()), name="presence_motif_list"),
    path("presence-motifs/nouveau/", login_and_perm("core.add_presencemotif", PresenceMotifCreateView.as_view()), name="presence_motif_create"),
    path("presence-motifs/<int:pk>/", login_and_perm("core.view_presencemotif", PresenceMotifDetailView.as_view()), name="presence_motif_detail"),
    path("presence-motifs/<int:pk>/modifier/", login_and_perm("core.change_presencemotif", PresenceMotifUpdateView.as_view()), name="presence_motif_update"),
    path("presence-motifs/<int:pk>/supprimer/", login_and_perm("core.delete_presencemotif", PresenceMotifDeleteView.as_view()), name="presence_motif_delete"),

    # Itineraires
    path("itineraires/", login_and_perm("core.view_itineraire", ItineraireListView.as_view()), name="itineraire_list"),
    path("itineraires/nouveau/", login_and_perm("core.add_itineraire", ItineraireCreateView.as_view()), name="itineraire_create"),
    path("itineraires/<int:pk>/", login_and_perm("core.view_itineraire", ItineraireDetailView.as_view()), name="itineraire_detail"),
    path("itineraires/<int:pk>/modifier/", login_and_perm("core.change_itineraire", ItineraireUpdateView.as_view()), name="itineraire_update"),
    path("itineraires/<int:pk>/supprimer/", login_and_perm("core.delete_itineraire", ItineraireDeleteView.as_view()), name="itineraire_delete"),

    # Parametres
    path("parametres/", login_and_perm("core.view_parametre", ParametreListCreateView.as_view()), name="parametre_list"),

    # API
    path("api/tonnages_json/", login_and_perm("core.view_collecte", views_api.tonnages_json), name="tonnages_json"),

]
