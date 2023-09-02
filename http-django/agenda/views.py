from django.shortcuts import render, get_object_or_404
from django.http.response import HttpResponseRedirect
from django.urls import reverse
from datetime import date

from agenda.models import Categoria, Evento


def categoria_list(request):
  nome = request.POST.get("nome")
  Categoria.objects.create(nome=nome)
  
  return HttpResponseRedirect("/eventos")

def evento_list(request):
  if request.method == "GET":
    categorias = Categoria.objects.all()
    eventos = Evento.objects.exclude(data__lt=date.today()).order_by("data")

    return render(
      request=request,
      context={"categorias": categorias, "eventos": eventos},
      template_name="agenda/evento_list.html"
    )
  
  if request.method == "POST":
    nome = request.POST.get("nome")
    categoria_id = request.POST.get("categoria_id")
    local = request.POST.get("local")
    link = request.POST.get("link")
    data = request.POST.get("data")
    if not data:
      data = None

    categoria = get_object_or_404(Categoria, id=categoria_id)
    Evento.objects.create(
      nome=nome,
      categoria=categoria,
      local=local,
      link=link,
      data=data
    )

    return HttpResponseRedirect("/eventos")

def evento_detail(request, id):
  evento = get_object_or_404(Evento, id=id)

  return render(
    request=request,
    context={"evento": evento},
    template_name="agenda/evento_detail.html"
  )

def evento_actions(request):
  evento_id = request.POST.get("evento_id")
  evento = get_object_or_404(Evento, id=evento_id)
  evento.participantes += 1
  evento.save()

  return HttpResponseRedirect(reverse("evento_detail", args=(evento_id,)))