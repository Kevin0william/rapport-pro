from django.contrib import admin
from .models import Rapport
# Register your models here.

@admin.register(Rapport)
class RapportAdmin(admin.ModelAdmin):
    list_display=('user','prix','probleme','contact','create_at')
    list_filter=('user','prix','create_at')
    search_fields=('user__username','prix')
    # ordering=('-create_at')
