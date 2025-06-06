from django.contrib import admin
from django import forms
from .models import Murders, suspects, investigators, interviews


@admin.register(suspects)
class SuspectsAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'age', 'image')
    search_fields = ('name', 'description')

@admin.register(investigators)
class InvestigatorsAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'age', 'image')
    search_fields = ('name', 'description')

@admin.register(Murders)
class MurdersAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'image')
    search_fields = ('name', 'description')

class InterviewsForm(forms.ModelForm):
    class Meta:
        model = interviews
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Initially show empty querysets for suspects and investigators
        self.fields['suspects'].queryset = suspects.objects.none()
        self.fields['investigators'].queryset = investigators.objects.none()
        
        # If there's data (form was submitted)
        if 'murders' in self.data:
            try:
                murder_id = int(self.data.get('murders'))
                self.fields['suspects'].queryset = suspects.objects.filter(murders_id=murder_id)
                self.fields['investigators'].queryset = investigators.objects.filter(murders_id=murder_id)
            except (ValueError, TypeError):
                pass
        # If editing existing interview
        elif self.instance.pk:
            self.fields['suspects'].queryset = suspects.objects.filter(murders=self.instance.murders)
            self.fields['investigators'].queryset = investigators.objects.filter(murders=self.instance.murders)

@admin.register(interviews)
class InterviewsAdmin(admin.ModelAdmin):
    form = InterviewsForm
    list_display = ('murders', 'suspects', 'investigators', 'content', 'date', 'image')
    search_fields = ('suspects__name', 'investigators__name', 'content')
    
    class Media:
        js = ('admin/js/dynamic_interview.js',)