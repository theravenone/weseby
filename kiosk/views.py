from django.utils import timezone
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.contrib.staticfiles.templatetags.staticfiles import static

from decimal import *
from tablib import Dataset
import datetime
import csv
from django.core import serializers

from .models import Laki, Zelt, Konto, Buchung
from .resources import *
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
    current_user = request.user

    buchungen = laki.konto.buchung_set.all().order_by('-datetime')

    if request.method == 'POST':
        form = ManualForm(request.POST)

        if form.is_valid():
            amount = form.cleaned_data['amount']

            laki.konto.withdraw(amount, current_user)
            laki.konto.save()

            laki.zelt.zeltkonto.withdraw(amount, current_user)
            laki.zelt.zeltkonto.save()

            return redirect('laki-list')

    else:
        form = ManualForm()

    return render(request, 'kiosk/laki_detail.html', {
        'form': form,
        'laki': laki,
        'buchungen': buchungen
        })


@login_required
def LakiDeposit(request, pk):
    """ LakiDepositView """
    laki = Laki.objects.get(pk=pk)
    current_user = request.user

    if request.method == 'POST':
        form_manual = ManualForm(request.POST)

        if form_manual.is_valid():
            amount = form_manual.cleaned_data['amount']

            laki.konto.deposit(amount, current_user)
            laki.konto.save()

            laki.zelt.zeltkonto.deposit(amount, current_user)
            laki.zelt.zeltkonto.save()

            laki.zelt.zeltlager.lagerkonto.deposit(amount, current_user)
            laki.zelt.zeltlager.lagerkonto.save()

    return redirect('laki-detail', pk=pk)


@login_required
def LakiWithdraw(request, pk):
    """ LakiWithdrawView """
    laki = Laki.objects.get(pk=pk)
    current_user = request.user

    if request.method == 'POST':
        form_manual = ManualForm(request.POST)

        if form_manual.is_valid():
            amount = form_manual.cleaned_data['amount']

            laki.konto.withdraw(amount, current_user)
            laki.konto.save()

            laki.zelt.zeltkonto.withdraw(amount, current_user)
            laki.zelt.zeltkonto.save()

            laki.zelt.zeltlager.lagerkonto.withdraw(amount, current_user)
            laki.zelt.zeltlager.lagerkonto.save()

    return redirect('laki-detail', pk=pk)


@login_required
def LakiKiosk(request, pk):
    """ LakiKioskView """
    today = 0
    date_today = timezone.now().date()
    date_yesterday = date_today - datetime.timedelta(1)
    date_tomorrow = date_today + datetime.timedelta(1)

    laki = Laki.objects.get(pk=pk)
    buchungen_withdraw = laki.konto.buchung_set.all().filter(datetime__range=(date_yesterday, date_tomorrow)).order_by('-datetime')
    current_user = request.user

    for buchung in buchungen_withdraw:
        #check if buchung from today
        if buchung.datetime.date() == date_today and buchung.type == "withdraw":
            today += buchung.amount

    if request.method == 'POST':
        form = KioskForm(request.POST)
        form_manual = ManualForm(request.POST)

        if form.is_valid():
            if form.cleaned_data['betrag'] == "einzahlung":
                amount = form.cleaned_data['betrag']

                laki.konto.deposit(amount, current_user)
                laki.konto.save()

                laki.zelt.zeltkonto.deposit(amount, current_user)
                laki.zelt.zeltkonto.save()

                laki.zelt.zeltlager.lagerkonto.deposit(amount, current_user)
                laki.zelt.zeltlager.lagerkonto.save()

                return redirect('laki-kiosk', pk)

            if form.cleaned_data['betrag'] != "0":
                amount = Decimal(form.cleaned_data['betrag'])/100

                laki.konto.withdraw(amount, current_user)
                laki.konto.save()

                laki.zelt.zeltkonto.withdraw(amount, current_user)
                laki.zelt.zeltkonto.save()

                laki.zelt.zeltlager.lagerkonto.withdraw(amount, current_user)
                laki.zelt.zeltlager.lagerkonto.save()

                return redirect('laki-kiosk', pk)

        if form_manual.is_valid():
            amount = form_manual.cleaned_data['amount']

            laki.konto.withdraw(amount, current_user)
            laki.konto.save()

            laki.zelt.zeltkonto.withdraw(amount, current_user)
            laki.zelt.zeltkonto.save()

            laki.zelt.zeltlager.lagerkonto.withdraw(amount, current_user)
            laki.zelt.zeltlager.lagerkonto.save()


            return redirect('kiosk-overview')

    else:
        form = KioskForm()
        form_manual = ManualForm()

    return render(request, 'kiosk/laki_kiosk.html', {
        'form': form,
        'form_manual' : form_manual,
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


@login_required
def simple_upload(request):
    """ LakiUploadView"""
    if request.method == 'POST':
        laki_resource = LakiResource()
        dataset = Dataset()
        new_lakis = request.FILES['myfile']

        imported_data = dataset.load(new_lakis.read())
        result = laki_resource.import_data(dataset, dry_run=True)  # Test the data import

        if not result.has_errors():
            laki_resource.import_data(dataset, dry_run=False)  # Actually import now

    return render(request, 'core/simple_upload.html')


@login_required
def LagerDetail(request):
    """ LagerDetailView """

    buchungen_zelt1 = Zelt.objects.get(pk=1).zeltkonto.buchung_set.all().order_by('-datetime')
    buchungen_zelt2 = Zelt.objects.get(pk=2).zeltkonto.buchung_set.all().order_by('-datetime')
    buchungen_zelt3 = Zelt.objects.get(pk=3).zeltkonto.buchung_set.all().order_by('-datetime')
    buchungen_zelt4 = Zelt.objects.get(pk=4).zeltkonto.buchung_set.all().order_by('-datetime')
    buchungen_zelt5 = Zelt.objects.get(pk=5).zeltkonto.buchung_set.all().order_by('-datetime')
    buchungen_zelt6 = Zelt.objects.get(pk=6).zeltkonto.buchung_set.all().order_by('-datetime')
    buchungen_zelt7 = Zelt.objects.get(pk=7).zeltkonto.buchung_set.all().order_by('-datetime')
    buchungen_zelt8 = Zelt.objects.get(pk=8).zeltkonto.buchung_set.all().order_by('-datetime')
    buchungen_zelt9 = Zelt.objects.get(pk=9).zeltkonto.buchung_set.all().order_by('-datetime')
    buchungen_zelt10 = Zelt.objects.get(pk=10).zeltkonto.buchung_set.all().order_by('-datetime')
    buchungen_zelt11 = Zelt.objects.get(pk=11).zeltkonto.buchung_set.all().order_by('-datetime')
    buchungen_zelt12 = Zelt.objects.get(pk=12).zeltkonto.buchung_set.all().order_by('-datetime')
    buchungen_zelt13 = Zelt.objects.get(pk=13).zeltkonto.buchung_set.all().order_by('-datetime')
    buchungen_zelt14 = Zelt.objects.get(pk=14).zeltkonto.buchung_set.all().order_by('-datetime')
    buchungen_zelt15 = Zelt.objects.get(pk=15).zeltkonto.buchung_set.all().order_by('-datetime')
    buchungen_lager = Zelt.objects.get(pk=1).zeltlager.lagerkonto.buchung_set.all().order_by('-datetime')

    url = static('kiosk/import/lakis.csv')
    return render(request, 'kiosk/lager_detail.html', {
        'url' : url,
        'buchungen_zelt1' : buchungen_zelt1,
        'buchungen_zelt2' : buchungen_zelt2,
        'buchungen_zelt3' : buchungen_zelt3,
        'buchungen_zelt4' : buchungen_zelt4,
        'buchungen_zelt5' : buchungen_zelt5,
        'buchungen_zelt6' : buchungen_zelt6,
        'buchungen_zelt7' : buchungen_zelt7,
        'buchungen_zelt8' : buchungen_zelt8,
        'buchungen_zelt9' : buchungen_zelt9,
        'buchungen_zelt10' : buchungen_zelt10,
        'buchungen_zelt11' : buchungen_zelt11,
        'buchungen_zelt12' : buchungen_zelt12,
        'buchungen_zelt13' : buchungen_zelt13,
        'buchungen_zelt14' : buchungen_zelt14,
        'buchungen_zelt15' : buchungen_zelt15,
        'buchungen_lager': buchungen_lager
        })


@login_required
def ExportBalanceZelt(request):
    """ ExportBalanceZelt View"""

    zelt_recource = ZeltResource()
    dataset = zelt_recource.export()

    response = HttpResponse(dataset.csv, content_type='text/csv')
    response['Content-Dispostion'] = 'attachement; filename="zelt.csv"'

    return response


@login_required
def KontoAuszug(request, pk):
    """ KontoAuszug View"""
    laki = Laki.objects.get(pk=pk)
    laki_konto = laki.konto

    buchung_recource = BuchungResource()
    queryset = Buchung.objects.filter(konto=laki_konto)
    dataset = buchung_recource.export(queryset)

    response = HttpResponse(dataset.csv, content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="auszug.csv"'

    return response


@login_required
def ImportDetail(request):
    """ ImportDetailView"""

    current_user = request.user
    #url = static('kiosk/import/lakis.csv')
    url = '/home/sven/enviroments/weseby/kiosk/static/kiosk/import/lakis.csv'
    with open(url, mode='r') as csv_file:
        csv_reader = csv.DictReader(csv_file, delimiter=';')
        for row in csv_reader:
            lakis_db = Laki.objects.filter(vorname=row["Vorname"]).filter(nachname=row["Name"])
            if not lakis_db:
                amount = Decimal(row["Geld"])
                new_konto = Konto()
                new_konto.kontoNr = row["Konto-Nr."]
                new_konto.save()
                new_konto.deposit(amount, current_user)
                new_konto.save()

                new_laki = Laki()
                new_laki.vorname = row["Vorname"]
                new_laki.nachname = row["Name"]
                new_laki.telefon = row["Tel_pr"]
                new_laki.handy = row["Handy"]
                new_laki.geschlecht = row["Geschlecht"]

                if row["Ort"]:
                    adresse = row["Ort"].split(" ")
                    new_laki.plz = adresse[0]
                    new_laki.ort = adresse[1]

                if row["Strasse"]:
                    new_laki.strase = row["Strasse"]

                if row["Geboren"]:
                    new_laki.geburtsdatum = row["Geboren"]

                if row["KK-Karte"] == 'j':
                    new_laki.krankenkassenkarteVorhanden = True
                    new_laki.privatVersichert = False
                elif row["KK-Karte"] == 'p':
                    new_laki.krankenkassenkarteVorhanden = False
                    new_laki.privatVersichert = True
                else:
                    new_laki.krankenkassenkarteVorhanden = False
                    new_laki.privatVersichert = False

                if row["Elternzettel"] == "j":
                    new_laki.elternzettelVorhanden = True
                else:
                    new_laki.elternzettelVorhanden = False

                if row["Arztzettel"] == "j":
                    new_laki.arztzettelVorhanden = True
                else:
                    new_laki.arztzettelVorhanden = False

                if row["Impfpass"] == "j":
                    new_laki.impfpassVorhanden = True
                else:
                    new_laki.impfpassVorhanden = False

                new_laki.zelt = Zelt.objects.get(pk=row["Zelt"])
                new_laki.konto = new_konto
                new_laki.save()


                new_laki.zelt.zeltkonto.deposit(amount, current_user)
                new_laki.zelt.zeltkonto.save()

                new_laki.zelt.zeltlager.lagerkonto.deposit(amount, current_user)
                new_laki.zelt.zeltlager.lagerkonto.save()

    return redirect('lager-detail')
