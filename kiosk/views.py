from django.utils import timezone
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.urls import reverse
from django.views import generic
# Create your views here.

from .models import *
from .forms import *


class LakiListView(generic.ListView):
    context_object_name = 'laki_liste'

    def get_queryset(self):
       return Laki.objects.all()


def KioskList(request):
    lakis = Laki.objects.all()

    return render(request, 'kiosk/kiosk_list.html', {'laki_liste': lakis})


class LakiDetailView(generic.DetailView):
    model = Laki
    context_object_name = 'laki'


def LakiKiosk(request, pk):
    laki = Laki.objects.get(pk=pk)
    #buchungen = laki.konto.buchung_set.all()
    buchungen_withdraw = laki.konto.buchung_set.all().filter(type='withdraw')

    if request.method == 'POST':
        form = KioskForm(request.POST)

        if form.is_valid():

            amount = form.cleaned_data['amount']

            laki.konto.withdraw(amount)
            laki.konto.save()

            return redirect('kiosk-list')

    else:
        form = KioskForm()

    return render(request, 'kiosk/laki_kiosk.html', {'form': form, 'laki': laki, 'buchungen': buchungen_withdraw})


def ZeltDetail(request, pk):
    lakisZelt = Laki.objects.filter(zelt__zeltnummer=pk)

    return render(request, 'kiosk/zelt_detail.html', {'laki_liste': lakisZelt})
