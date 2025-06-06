from django.contrib import admin
from .models import Murders, suspects, investigators, interviews


@admin.register(suspects)
class SuspectsAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'age', 'image')
    search_fields = ('name', 'description')
@admin.register(investigators)
class InvestigatorsAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'age', 'image')
    search_fields = ('name', 'description')
@admin.register(interviews)
class InterviewsAdmin(admin.ModelAdmin):
    list_display = ('suspects', 'investigators', 'content', 'date', 'image')
    search_fields = ('suspects__name', 'investigators__name', 'content')
@admin.register(Murders)
class MurdersAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'image')
    search_fields = ('name', 'description')
# Register your models here.
