from django.shortcuts import render, redirect, get_object_or_404
from .models import Produit
from .forms import ProduitForm

import json
from django.db import transaction
from django.http import JsonResponse, HttpResponseNotAllowed
from django.shortcuts import render, get_object_or_404
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.http import require_POST
from .models import Vehicule, Flux, Energie




def home(request):
    return render(request, "core/home.html")



def products_list(request):
    produits = Produit.objects.all()
    return render(request, "core/products_list.html", {"produits": produits})




def products_list(request):
    produits = Produit.objects.all().order_by("nom")
    return render(request, "core/products_list.html", {"produits": produits})

def product_create(request):
    if request.method == "POST":
        form = ProduitForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("products_list")
    else:
        form = ProduitForm()
    return render(request, "core/product_form.html", {"form": form, "title": "Créer un produit"})

def product_update(request, pk):
    produit = get_object_or_404(Produit, pk=pk)
    if request.method == "POST":
        form = ProduitForm(request.POST, instance=produit)
        if form.is_valid():
            form.save()
            return redirect("products_list")
    else:
        form = ProduitForm(instance=produit)
    return render(request, "core/product_form.html", {"form": form, "title": "Modifier un produit"})

def product_delete(request, pk):
    produit = get_object_or_404(Produit, pk=pk)
    if request.method == "POST":
        produit.delete()
        return redirect("products_list")
    return render(request, "core/product_confirm_delete.html", {"produit": produit})






from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Agent
from .forms import AgentForm, VehiculeForm, FluxForm, EnergieForm


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



from django.views.generic import TemplateView
from .models import Agent

class PlanningView(TemplateView):
    template_name = "core/planning.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)

        # ⚠️ adapte les noms de champs à ton modèle
        # exemple: qualification peut s'appeler "role", "categorie", "poste", etc.
        agents_qs = Agent.objects.all().order_by("nom")

        ctx["agents"] = list(
            agents_qs.values("id", "nom", "qualification")
        )
        return ctx












def vehicules_page(request):
    vehicules = Vehicule.objects.order_by("vehicule")
    return render(request, "vehicules/index.html", {"vehicules": vehicules})

@require_POST
@csrf_protect
def vehicules_save(request):
    """
    Attend un JSON:
    { "items": [ {"vehicule": "ABC", "type": "Camion", "archive": true}, ... ] }
    """
    try:
        payload = json.loads(request.body.decode("utf-8"))
        items = payload.get("items", [])
    except Exception:
        return JsonResponse({"ok": False, "error": "JSON invalide"}, status=400)

    if not isinstance(items, list):
        return JsonResponse({"ok": False, "error": "`items` doit être une liste"}, status=400)

    # On met à jour uniquement les champs éditables
    vehicules_map = {v.vehicule: v for v in Vehicule.objects.filter(vehicule__in=[i.get("vehicule") for i in items])}

    updated = []
    with transaction.atomic():
        for i in items:
            pk = i.get("vehicule")
            if not pk or pk not in vehicules_map:
                continue
            v = vehicules_map[pk]
            v.type = (i.get("type") or "").strip()
            v.archive = bool(i.get("archive"))
            updated.append(v)

        if updated:
            Vehicule.objects.bulk_update(updated, ["type", "archive", "date_modif"])

    return JsonResponse({"ok": True, "updated": len(updated)})

@require_POST
@csrf_protect
def vehicule_delete(request, pk):
    v = get_object_or_404(Vehicule, pk=pk)
    v.delete()
    return JsonResponse({"ok": True})
