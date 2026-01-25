from django.urls import path
from .import views

from django.urls import path
from .views import (
    AgentListView, AgentDetailView, AgentCreateView, AgentUpdateView, AgentDeleteView
)

from .views import (
    PlanningView
)

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
]

