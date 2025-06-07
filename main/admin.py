from django.contrib import admin
from django import forms
from .models import Murders, Suspects, Investigators, Interviews, ChatRoom, ChatMessage


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


@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ('chat_room_info', 'sender', 'message_preview', 'is_admin', 'timestamp', 'is_read')
    list_filter = ('is_admin', 'is_read', 'timestamp', 'chat_room__user')
    search_fields = ('message', 'sender__username', 'chat_room__subject', 'chat_room__user__username')
    readonly_fields = ('timestamp',)
    ordering = ('-timestamp',)
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('chat_room', 'sender', 'chat_room__user')
    
    def chat_room_info(self, obj):
        return f"💬 {obj.chat_room.user.username} - {obj.chat_room.subject}"
    chat_room_info.short_description = "Chat Room (User)"
    
    def message_preview(self, obj):
        icon = "🛡️" if obj.is_admin else "👤"
        preview = obj.message[:60] + "..." if len(obj.message) > 60 else obj.message
        return f"{icon} {preview}"
    message_preview.short_description = "Message"
    
    def save_model(self, request, obj, form, change):
        if not change:  # New message (admin reply)
            obj.sender = request.user
            obj.is_admin = True
        super().save_model(request, obj, form, change)
    
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if not obj:  # Creating new message (admin reply)
            # Auto-set sender and admin flag
            form.base_fields['sender'].initial = request.user
            form.base_fields['sender'].widget = forms.HiddenInput()
            form.base_fields['is_admin'].initial = True
            form.base_fields['is_admin'].widget = forms.HiddenInput()
        return form

@admin.register(ChatRoom)
class ChatRoomAdmin(admin.ModelAdmin):
    list_display = ('user_info', 'subject', 'murder_case', 'unread_count', 'last_activity', 'is_active')
    list_filter = ('is_active', 'created_at', 'murder_case')
    search_fields = ('user__username', 'subject', 'user__email')
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('-updated_at',)
    
    def user_info(self, obj):
        return f"👤 {obj.user.username} ({obj.user.email})"
    user_info.short_description = "User"
    
    def unread_count(self, obj):
        count = obj.messages.filter(is_admin=False, is_read=False).count()
        if count > 0:
            return f"🔴 {count} unread"
        return "✅ All read"
    unread_count.short_description = "Status"
    
    def last_activity(self, obj):
        last_msg = obj.messages.order_by('-timestamp').first()
        if last_msg:
            return f"{last_msg.timestamp.strftime('%m/%d %H:%M')} - {last_msg.sender.username}"
        return "No messages"
    last_activity.short_description = "Last Activity"
