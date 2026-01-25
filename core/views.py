from django.shortcuts import render, redirect, get_object_or_404
from .models import Produit
from .forms import ProduitForm


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
from .forms import AgentForm


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
