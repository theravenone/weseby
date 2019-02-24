import datetime

from django.utils import timezone
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from django.contrib.auth.decorators import login_required
from decimal import *

from .models import Laki, Zelt
from .forms import LakiForm, KioskForm, ManualForm


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

    buchungen = laki.konto.buchung_set.all().order_by('-datetime')

    if request.method == 'POST':
        form = ManualForm(request.POST)

        if form.is_valid():
            amount = form.cleaned_data['amount']

            laki.konto.withdraw(amount)
            laki.konto.save()

            return redirect('laki-list')

    else:
        form = ManualForm()

    return render(request, 'kiosk/laki_detail.html', {
        'form': form,
        'laki': laki,
        'buchungen': buchungen
        })


@login_required
def LakiKiosk(request, pk):
    """ LakiKioskView """
    today = 0
    date_today = timezone.now().date()
    date_yesterday = date_today - datetime.timedelta(1)
    date_tomorrow = date_today + datetime.timedelta(1)

    laki = Laki.objects.get(pk=pk)
    buchungen_withdraw = laki.konto.buchung_set.all().filter(type='withdraw').filter(datetime__range=(date_yesterday, date_tomorrow)).order_by('-datetime')

    for buchung in buchungen_withdraw:
        #check if buchung from today
        if buchung.datetime.date() == date_today:
            today += buchung.amount

    if request.method == 'POST':
        form = KioskForm(request.POST)

        if form.is_valid():
            if form.cleaned_data['betrag'] == "0":
                amount = form.cleaned_data['amount']
            else:
                amount = Decimal(form.cleaned_data['betrag'])/100

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
    zelt = Zelt.objects.get(pk=pk)

    for laki in lakis_zelt:
        zeltbalance += laki.konto.get_balance()

    return render(request, 'kiosk/zelt_detail.html', {
        'laki_liste': lakis_zelt,
        'zeltbalance': zeltbalance,
        'zelt': zelt
        })
