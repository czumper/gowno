from django.db.models import F
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from .models import Wybor, Pytanie


class IndexView(generic.ListView):
    template_name = "apka/index.html"
    context_object_name = "lista_ostatnich_pytan"

    def get_queryset(self):
        return Pytanie.objects.order_by("-data_pub")[:5]

class DetaleView(generic.DetailView):
    model = Pytanie
    template_name = "apka/detale.html"

class WynikiView(generic.DetailView):
    model = Pytanie
    template_name = "apka/wyniki.html"

def glos(request, pytanie_id):
    pytanie = get_object_or_404(Pytanie, pk=pytanie_id)
    try:
        wybrany_wybor = pytanie.wybor_set.get(pk=request.POST["wybor"])
    except (KeyError, Wybor.DoesNotExist):
        return render(
            request,
            "apka/detale.html",
            {
                "pytanie": pytanie,
                "error_message": "Nie wybrałeś żadnej opcji.",
            },
        )
    else:
        wybrany_wybor.glosy = F("glosy") +1
        wybrany_wybor.save()
        return HttpResponseRedirect(reverse('apka:wyniki', args=(pytanie.id,)))


# Create your views here.
