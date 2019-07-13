from import_export import resources
from .models import Laki, Buchung

class LakiResource(resources.ModelResource):
    class Meta:
        model = Laki


class BuchungResource(resources.ModelResource):
    class Meta:
        model = Buchung
        fields = ('datetime', 'balance', 'amount', 'type',)


class ZeltResource(resources.ModelResource):
    class Meta:
        model = Laki
        fields = ('id', 'vorname', 'nachname', 'zelt__zeltnummer', 'konto__balance',)
