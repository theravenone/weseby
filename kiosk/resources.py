from import_export import resources
from .models import Laki

class LakiResource(resources.ModelResource):
    class Meta:
        model = Laki
        