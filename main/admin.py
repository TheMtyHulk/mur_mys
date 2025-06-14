from django.contrib import admin
from django import forms
from .models import Murders, Suspects, Investigators, Interviews, UserProfile
@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'email_verified', 'email_token')
    search_fields = ('user__username', 'user__email')
@admin.register(Suspects)
class SuspectsAdmin(admin.ModelAdmin):
    list_display = ('murders','name', 'description', 'age', 'image')
    search_fields = ('name', 'description', 'murders__name')

@admin.register(Investigators)
class InvestigatorsAdmin(admin.ModelAdmin):
    list_display = ('murders','name', 'description', 'age', 'image')
    search_fields = ('name', 'description', 'murders__name')

@admin.register(Murders)
class MurdersAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'image')
    search_fields = ('name', 'description')

class InterviewsForm(forms.ModelForm):
    class Meta:
        model = Interviews
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Initially show empty querysets for suspects and investigators
        self.fields['suspects'].queryset = Suspects.objects.none()
        self.fields['investigators'].queryset = Investigators.objects.none()
        
        # If there's data (form was submitted)
        if 'murders' in self.data:
            try:
                murder_id = int(self.data.get('murders'))
                self.fields['suspects'].queryset = Suspects.objects.filter(murders_id=murder_id)
                self.fields['investigators'].queryset = Investigators.objects.filter(murders_id=murder_id)
            except (ValueError, TypeError):
                pass
        # If editing existing interview
        elif self.instance.pk:
            self.fields['suspects'].queryset = Suspects.objects.filter(murders=self.instance.murders)
            self.fields['investigators'].queryset = Investigators.objects.filter(murders=self.instance.murders)

@admin.register(Interviews)
class InterviewsAdmin(admin.ModelAdmin):
    form = InterviewsForm
    list_display = ('murders', 'suspects', 'investigators', 'content', 'date', 'image')
    search_fields = ('suspects__name', 'investigators__name', 'content','murders__name')
    
    class Media:
        js = ('admin/js/dynamic_interview.js',)



