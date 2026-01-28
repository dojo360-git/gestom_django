from django.contrib import admin

from .models import Agent
@admin.register(Agent)
class AgentAdmin(admin.ModelAdmin):
    list_display = ("id_ag", "nom", "prenom", "service", "employeur", "tel", "supp")
    search_fields = ("nom", "prenom", "id_ag", "tel")
    list_filter = ("service", "employeur", "supp")
