from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from helpers.decorators import contactLoginRequired
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import redirect
from .models import ChatRoom, ChatMessage
# Create your views here.
@contactLoginRequired
def contactView(request):
    # Get or create active chat room for user
    chat_room, created = ChatRoom.objects.get_or_create(
        user=request.user,
        is_active=True,
        defaults={
            'subject': f'Support Chat - {request.user.username}',
        }
    )
    
    # Get all messages for this chat room
    messages = chat_room.messages.all()
    
    # Mark admin messages as read
    ChatMessage.objects.filter(
        chat_room=chat_room,
        is_admin=True,
        is_read=False
    ).update(is_read=True)
    
    # Handle new message
    if request.method == 'POST':
        message_text = request.POST.get('message', '').strip()
        if message_text:
            ChatMessage.objects.create(
                chat_room=chat_room,
                sender=request.user,
                message=message_text,
                is_admin=False
            )
            # Update chat room timestamp
            chat_room.save()
            return redirect('contact')
    
    context = {
        'chat_room': chat_room,
        'messages': messages,
    }
    return render(request, 'chat/contact.html', context)

@staff_member_required
def admin_chat_dashboard(request):
    # Get all active chat rooms
    chat_rooms = ChatRoom.objects.filter(is_active=True).order_by('-updated_at')
    
    # Handle selecting a specific chat room
    active_room_id = request.GET.get('room')
    active_room = None
    messages = []
    
    if active_room_id:
        try:
            active_room = chat_rooms.get(id=active_room_id)
            messages = active_room.messages.all()
            
            # Mark user messages as read
            ChatMessage.objects.filter(
                chat_room=active_room,
                is_admin=False,
                is_read=False
            ).update(is_read=True)
            
            # Handle new message from admin
            if request.method == 'POST':
                message_text = request.POST.get('message', '').strip()
                if message_text:
                    ChatMessage.objects.create(
                        chat_room=active_room,
                        sender=request.user,
                        message=message_text,
                        is_admin=True
                    )
                    # Update chat room timestamp
                    active_room.save()
                    return redirect(f'/support/chat/?room={active_room_id}')
        except ChatRoom.DoesNotExist:
            pass
    
    # Get unread message counts for each chat room
    for room in chat_rooms:
        room.unread_count = room.messages.filter(is_admin=False, is_read=False).count()
    
    context = {
        'chat_rooms': chat_rooms,
        'active_room': active_room,
        'messages': messages,
    }
    return render(request, 'admin/admin_chat.html', context)

# API views to get suspects and investigators AJAX
from django.http import JsonResponse
from django.contrib.admin.views.decorators import staff_member_required

from .models import ChatRoom, ChatMessage

# AJAX endpoint to get new messages
@login_required
def get_new_messages(request):
    chat_room_id = request.GET.get('chat_room_id')
    last_message_id = request.GET.get('last_message_id', 0)
    
    try:
        chat_room = ChatRoom.objects.get(id=chat_room_id, user=request.user)
        new_messages = chat_room.messages.filter(id__gt=last_message_id)
        
        messages_data = []
        for msg in new_messages:
            messages_data.append({
                'id': msg.id,
                'sender': msg.sender.username,
                'message': msg.message,
                'is_admin': msg.is_admin,
                'timestamp': msg.timestamp.strftime('%I:%M %p'),
                'full_timestamp': msg.timestamp.strftime('%B %d, %Y at %I:%M %p'),
            })
        
        # Mark admin messages as read
        new_messages.filter(is_admin=True, is_read=False).update(is_read=True)
        
        return JsonResponse({
            'success': True,
            'messages': messages_data
        })
    except ChatRoom.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Chat room not found'})

# AJAX endpoint to send message
@login_required
def send_message(request):
    if request.method == 'POST':
        chat_room_id = request.POST.get('chat_room_id')
        message_text = request.POST.get('message', '').strip()
        
        if not message_text:
            return JsonResponse({'success': False, 'error': 'Message cannot be empty'})
        
        try:
            chat_room = ChatRoom.objects.get(id=chat_room_id, user=request.user)
            message = ChatMessage.objects.create(
                chat_room=chat_room,
                sender=request.user,
                message=message_text,
                is_admin=False
            )
            # Update chat room timestamp
            chat_room.save()
            
            return JsonResponse({
                'success': True,
                'message': {
                    'id': message.id,
                    'sender': message.sender.username,
                    'message': message.message,
                    'is_admin': False,
                    'timestamp': message.timestamp.strftime('%I:%M %p'),
                }
            })
        except ChatRoom.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Chat room not found'})
    
    return JsonResponse({'success': False, 'error': 'Invalid request'})

@login_required
def clear_chat(request):
    if request.method == 'POST':
        chat_room_id = request.POST.get('chat_room_id')
        
        try:
            chat_room = ChatRoom.objects.get(id=chat_room_id, user=request.user)
            
            # Delete all messages in this chat room
            deleted_count = chat_room.messages.all().delete()[0]
            
            # Update chat room timestamp
            chat_room.save()
            chat_room.delete()  # Optionally delete the chat room
            
            return JsonResponse({
                'success': True,
                'message': f'Chat cleared successfully! ({deleted_count} messages removed)'
            })
        except ChatRoom.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Chat room not found'})
    
    return JsonResponse({'success': False, 'error': 'Invalid request'})

@staff_member_required
def admin_get_new_messages(request):
    chat_room_id = request.GET.get('chat_room_id')
    last_message_id = request.GET.get('last_message_id', 0)
    
    try:
        chat_room = ChatRoom.objects.get(id=chat_room_id)
        new_messages = chat_room.messages.filter(id__gt=last_message_id)
        
        messages_data = []
        for msg in new_messages:
            messages_data.append({
                'id': msg.id,
                'sender': msg.sender.username,
                'message': msg.message,
                'is_admin': msg.is_admin,
                'timestamp': msg.timestamp.strftime('%I:%M %p'),
            })
        
        # Mark user messages as read
        new_messages.filter(is_admin=False, is_read=False).update(is_read=True)
        
        return JsonResponse({
            'success': True,
            'messages': messages_data
        })
    except ChatRoom.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Chat room not found'})

@staff_member_required
def admin_clear_chat(request):
    if request.method == 'POST':
        chat_room_id = request.POST.get('chat_room_id')
        
        if not chat_room_id:
            return JsonResponse({'success': False, 'error': 'Chat room ID is required'})
        
        try:
            # Note: No user restriction since admin can clear any chat
            chat_room = ChatRoom.objects.get(id=chat_room_id)
            
            # Delete all messages in this chat room
            deleted_count, _ = chat_room.messages.all().delete()
            
            # Update chat room timestamp
            chat_room.save()
            chat_room.delete()  # Optionally delete the chat room
            
            return JsonResponse({
                'success': True,
                'message': f'Chat cleared successfully! ({deleted_count} messages removed)'
            })
        except ChatRoom.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Chat room not found'})
        except Exception as e:
            import logging
            logger = logging.getLogger(__name__)
            logger.error(f"Error clearing chat: {str(e)}")
            return JsonResponse({'success': False, 'error': f'An error occurred: {str(e)}'})
    
    return JsonResponse({'success': False, 'error': 'Invalid request method'})