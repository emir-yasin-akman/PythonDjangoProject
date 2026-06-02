from django.contrib import admin
from .models import Hedef, HedefNot, SecilenHedef

# Register your models here.

class HedefAdmin(admin.ModelAdmin):
    list_display = ('baslik', 'ikon', 'aciklama')
    editable_fields = ('baslik', 'ikon', 'aciklama')
    search_fields = ('baslik',)

admin.site.register(Hedef, HedefAdmin)
admin.site.register(SecilenHedef)
admin.site.register(HedefNot)

