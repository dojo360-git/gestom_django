from django.contrib import admin

from .models import Agent, Collecte, HeuresManuelles
@admin.register(Agent)
class AgentAdmin(admin.ModelAdmin):
    list_display = ("id", "nom", "prenom", "service", "employeur", "tel")
    search_fields = ("nom", "prenom", "tel")
    list_filter = ("service", "employeur")


@admin.register(Collecte)
class CollecteAdmin(admin.ModelAdmin):
    list_display = ("id_collecte", "date_collecte", "id_agent_1", "id_vehicule")
    list_filter = ("date_collecte",)


@admin.register(HeuresManuelles)
class HeuresManuellesAdmin(admin.ModelAdmin):
    list_display = ("date", "agent", "heure_debut", "heure_fin", "presence", "motif_heures_sup")
    list_filter = ("date", "presence")
    search_fields = ("agent__nom", "agent__prenom", "motif_heures_sup")
