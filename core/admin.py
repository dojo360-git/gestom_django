from django.contrib import admin

from .models import Agent, Collecte
@admin.register(Agent)
class AgentAdmin(admin.ModelAdmin):
    list_display = ("id", "nom", "prenom", "service", "employeur", "tel", "supp")
    search_fields = ("nom", "prenom", "tel")
    list_filter = ("service", "employeur", "supp")


@admin.register(Collecte)
class CollecteAdmin(admin.ModelAdmin):
    list_display = ("id_collecte", "date_collecte", "id_agent_1", "id_vehicule")
    list_filter = ("date_collecte",)
