import datetime

from django.utils import timezone
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from django.contrib.auth.decorators import login_required

from .models import Laki, Zelt
from .forms import LakiForm, KioskForm


@login_required
def LakiList(request):
    """ LakiListView """
    lakis = Laki.objects.all().order_by('vorname')

    return render(request, 'kiosk/laki_list.html', {'laki_liste': lakis})

@login_required
def KioskList(request):
    """ KioskListView """
    lakis = Laki.objects.all()

    return render(request, 'kiosk/kiosk_list.html', {'laki_liste': lakis})


@login_required
def KioskOverview(request):
    """ KioskOverviewView """
    zelte = Zelt.objects.all().order_by('zeltnummer')

    return render(request, 'kiosk/kiosk_overview.html', {'zelte': zelte})


@login_required
def KioskDetail(request, pk):
    """ KioskDetailView """
    lakis_zelt = Laki.objects.filter(zelt__zeltnummer=pk).order_by('vorname')

    zelt = Zelt.objects.get(pk=pk)


    return render(request, 'kiosk/kiosk_detail.html', {
        'laki_liste': lakis_zelt,
        'zelt': zelt
        })


@login_required
def LakiDetail(request, pk):
    """ LakiDetailView """
    laki = Laki.objects.get(pk=pk)

    buchungen = laki.konto.buchung_set.all()

    return render(request, 'kiosk/laki_detail.html', {
        'laki': laki,
        'buchungen': buchungen
        })


@login_required
def LakiKiosk(request, pk):
    """ LakiKioskView """
    laki = Laki.objects.get(pk=pk)
    #buchungen = laki.konto.buchung_set.all()
    buchungen_withdraw = laki.konto.buchung_set.all().filter(type='withdraw')
    today = 0
    date_today = timezone.now().date()

    for buchung in buchungen_withdraw:
        #check if buchung from today
        if buchung.datetime.date() == date_today:
            today += buchung.amount

    if request.method == 'POST':
        form = KioskForm(request.POST)

        if form.is_valid():

            amount = form.cleaned_data['amount']

            laki.konto.withdraw(amount)
            laki.konto.save()

            return redirect('kiosk-overview')

    else:
        form = KioskForm()

    return render(request, 'kiosk/laki_kiosk.html', {
        'form': form,
        'laki': laki,
        'buchungen': buchungen_withdraw,
        'today': today
        })


@login_required
def ZeltDetail(request, pk):
    """ ZeltDetailView """
    lakis_zelt = Laki.objects.filter(zelt__zeltnummer=pk)

    zeltbalance = 0
    zelt = pk

    for laki in lakis_zelt:
        zeltbalance += laki.konto.get_balance()

    return render(request, 'kiosk/zelt_detail.html', {
        'laki_liste': lakis_zelt,
        'zeltbalance': zeltbalance,
        'zelt': zelt
        })
