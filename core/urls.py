from django.urls import path
from .import views

from django.urls import path
from .views import (
    AgentListView, AgentDetailView, AgentCreateView, AgentUpdateView, AgentDeleteView,
    VehiculeListView, VehiculeDetailView, VehiculeCreateView, VehiculeUpdateView, VehiculeDeleteView,
    FluxListView, FluxDetailView, FluxCreateView, FluxUpdateView, FluxDeleteView,
    EnergieListView, EnergieDetailView, EnergieCreateView, EnergieUpdateView, EnergieDeleteView,
)

from .views import (
    PlanningView
)

app_name = "core" 


urlpatterns = [
    path("", views.home, name="home"),  # 👈 page d’accueil
    path("products/", views.products_list, name="products_list"),
    path("products/new/", views.product_create, name="product_create"),
    path("products/<int:pk>/edit/", views.product_update, name="product_update"),
    path("products/<int:pk>/delete/", views.product_delete, name="product_delete"),
    path("planning/", PlanningView.as_view(), name="planning"),
    path("agents/", AgentListView.as_view(), name="agent_list"),
    path("agents/nouveau/", AgentCreateView.as_view(), name="agent_create"),
    path("agents/<int:pk>/", AgentDetailView.as_view(), name="agent_detail"),
    path("agents/<int:pk>/modifier/", AgentUpdateView.as_view(), name="agent_update"),
    path("agents/<int:pk>/supprimer/", AgentDeleteView.as_view(), name="agent_delete"),
    path("vehicules/", VehiculeListView.as_view(), name="vehicule_list"),
    path("vehicules/nouveau/", VehiculeCreateView.as_view(), name="vehicule_create"),
    path("vehicules/<str:pk>/", VehiculeDetailView.as_view(), name="vehicule_detail"),
    path("vehicules/<str:pk>/modifier/", VehiculeUpdateView.as_view(), name="vehicule_update"),
    path("vehicules/<str:pk>/supprimer/", VehiculeDeleteView.as_view(), name="vehicule_delete"),
    path("flux/", FluxListView.as_view(), name="flux_list"),
    path("flux/nouveau/", FluxCreateView.as_view(), name="flux_create"),
    path("flux/<int:pk>/", FluxDetailView.as_view(), name="flux_detail"),
    path("flux/<int:pk>/modifier/", FluxUpdateView.as_view(), name="flux_update"),
    path("flux/<int:pk>/supprimer/", FluxDeleteView.as_view(), name="flux_delete"),
    path("energies/", EnergieListView.as_view(), name="energie_list"),
    path("energies/nouveau/", EnergieCreateView.as_view(), name="energie_create"),
    path("energies/<int:pk>/", EnergieDetailView.as_view(), name="energie_detail"),
    path("energies/<int:pk>/modifier/", EnergieUpdateView.as_view(), name="energie_update"),
    path("energies/<int:pk>/supprimer/", EnergieDeleteView.as_view(), name="energie_delete"),
]

