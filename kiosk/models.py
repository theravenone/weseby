import datetime
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class Zeltlager(models.Model):
    """ Model Zeltlager """
    jahr = models.IntegerField(default=1900)
    haelfte = models.IntegerField(default=1)
    kasse = models.DecimalField(default=0, max_digits=6, decimal_places=2)


class Zelt(models.Model):
    """ Model Zelt """
    zeltnummer = models.IntegerField(default=1)
    zeltname = models.CharField(max_length=20)
    zeltlager = models.ForeignKey(Zeltlager, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return str(self.zeltnummer)


class Konto(models.Model):
    """ Model Konto """
    kontoNr = models.CharField(max_length=10)
    balance = models.DecimalField(default=0, max_digits=6, decimal_places=2)

    def __str__(self):
        return self.kontoNr

    def get_balance(self):
        """ Konto getBalance function """
        return self.balance

    def get_konto_nr(self):
        """ Konto getKontoNr function """
        return self.kontoNr

    def check_withdraw(self, amount):
        """ Konto checkWithdraw function """
        if self.balance - amount >= 0.0:
            return True
        else:
            return False

    def deposit(self, amount):
        """ Konti deposit function """
        self.balance += amount
        buchung = Buchung()
        buchung.amount = amount
        buchung.konto = self
        buchung.balance = self.balance
        buchung.type = 'deposit'
        buchung.save()

        return True

    def withdraw(self, amount, user):
        """ Konto withdraw frunction """
        if self.check_withdraw(amount):
            self.balance -= amount
            buchung = Buchung()
            buchung.amount = amount
            buchung.user = user
            buchung.konto = self
            buchung.balance = self.balance
            buchung.type = 'withdraw'
            buchung.save()
            return True
        else:
            return False


class Buchung(models.Model):
    """ Model class Buchung """
    konto = models.ForeignKey(Konto, on_delete=models.SET_NULL, null=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    balance = models.DecimalField(default=0, max_digits=6, decimal_places=2)
    amount = models.DecimalField(default=0, max_digits=6, decimal_places=2)
    datetime = models.DateTimeField(default=timezone.now)
    type = models.CharField(max_length=10)


class Laki(models.Model):
    """ Model class Laki """
    vorname = models.CharField(max_length=20)
    nachname = models.CharField(max_length=20)
    geschlecht = models.CharField(max_length=10, default='unknown')
    geburtsdatum = models.DateField(default=datetime.date(1900, 1, 1))
    konto = models.ForeignKey(Konto, on_delete=models.SET_NULL, null=True)
    zelt = models.ForeignKey(Zelt, on_delete=models.SET_NULL, null=True)
    krankenkassenkarteVorhanden = models.BooleanField(default=False)
    privatVersichert = models.BooleanField(default=False)
    impfpassVorhanden = models.BooleanField(default=False)
    elternzettelVorhanden = models.BooleanField(default=False)
    arztzettelVorhanden = models.BooleanField(default=False)
    telefon = models.CharField(max_length=20, blank=True)
    handy = models.CharField(max_length=50, blank=True)
    strase = models.CharField(max_length=30, blank=True)
    plz = models.CharField(max_length=20, blank=True)
    ort = models.CharField(max_length=100, blank=True)
    hinweis = models.TextField(blank=True)

    def __str__(self):
        return self.vorname + " " + self.nachname
