import datetime
from django.db import models
from django.utils import timezone


class Zeltlager(models.Model):
    jahr = models.IntegerField(default=1900)
    haelfte = models.IntegerField(default=1)
    kasse = models.DecimalField(default=0, max_digits=6, decimal_places=2)


class Zelt(models.Model):
    zeltnummer = models.CharField(max_length=2)
    zeltname = models.CharField(max_length=20)
    zeltlager = models.ForeignKey(Zeltlager, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.zeltnummer


class Konto(models.Model):
    kontoNr = models.CharField(max_length=10)
    balance = models.DecimalField(default=0, max_digits=6, decimal_places=2)

    def __str__(self):
        return self.kontoNr

    def getBalance(self):
        return self.balance

    def getKontoNr(self):
        return self.kontoNr

    def checkWithdraw(self, amount):
        if self.balance - amount >= 0.0:
            return True
        else:
            return False

    def deposit(self, amount):
        self.balance += amount
        buchung = Buchung()
        buchung.amount = amount
        buchung.konto = self
        buchung.balance = self.balance
        buchung.type = 'deposit'

        return True

    def withdraw(self, amount):
        if self.checkWithdraw(amount):
            self.balance -= amount
            buchung = Buchung()
            buchung.amount = amount
            buchung.konto = self
            buchung.balance = self.balance
            buchung.type = 'withdraw'
            buchung.save()
            return True
        else:
            return False


class Buchung(models.Model):
    konto = models.ForeignKey(Konto, on_delete=models.SET_NULL, null=True)
    balance = models.DecimalField(default=0, max_digits=6, decimal_places=2)
    amount = models.DecimalField(default=0, max_digits=6, decimal_places=2)
    datetime = models.DateTimeField(default=timezone.now)
    type = models.CharField(max_length=10)


class Laki(models.Model):
    vorname = models.CharField(max_length=20)
    nachname = models.CharField(max_length=20)
    geschlecht = models.CharField(max_length=10, default='unknown')
    geburtsdatum = models.DateField(default=datetime.date(1900, 1, 1))
    konto = models.ForeignKey(Konto, on_delete=models.SET_NULL, null=True)
    zelt = models.ForeignKey(Zelt, on_delete=models.SET_NULL, null=True)
    krankenkassenkarteVorhanden = models.BooleanField(default=False)
    impfpassVorhanden = models.BooleanField(default=False)
    elternzettelVorhanden = models.BooleanField(default=False)
    arztzettelVorhanden = models.BooleanField(default=False)
    telefon = models.CharField(max_length=20)
    handy = models.CharField(max_length=20)
    strase = models.CharField(max_length=30)
    plz = models.CharField(max_length=20)
    ort = models.CharField(max_length=20)
    hinweis = models.TextField()

    def __str__(self):
        return self.vorname + " " + self.nachname

