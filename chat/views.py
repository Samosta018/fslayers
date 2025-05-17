from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib.auth import get_user_model
from .models import Chat, Message
from .forms import MessageForm
import json

User = get_user_model()

@login_required
def chat_list(request):
    return render(request, 'chat/chat_list.html')

@login_required
def chat_detail(request, chat_id=None, user_id=None):
    if user_id:
        other_user = get_object_or_404(User, id=user_id)
        chat = Chat.objects.filter(participants=request.user).filter(participants=other_user).first()
        if not chat:
            chat = Chat.objects.create()
            chat.participants.add(request.user, other_user)
        return redirect('chat:chat_detail', chat_id=chat.id)
    
    chat = get_object_or_404(Chat.objects.prefetch_related('participants', 'messages'), id=chat_id)
    
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.chat = chat
            message.sender = request.user
            message.save()
            chat.updated_at = message.created_at
            chat.save()
            
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': True,
                    'message': {
                        'id': message.id,
                        'text': message.text,
                        'created_at': message.created_at.strftime('%H:%M'),
                        'sender_id': message.sender.id,
                    }
                })
            return redirect('chat:chat_detail', chat_id=chat.id)
    
    chat.messages.filter(is_read=False).exclude(sender=request.user).update(is_read=True)
    messages = chat.messages.all().order_by('id')
    other_user = chat.participants.exclude(id=request.user.id).first()
    
    return render(request, 'chat/chat_detail.html', {
        'chat': chat,
        'messages': messages,
        'other_user': other_user,
        'form': MessageForm()
    })


@login_required
def get_messages(request, chat_id):
    chat = get_object_or_404(Chat, id=chat_id)
    last_message_id = int(request.GET.get('last_message_id', 0))

    messages = chat.messages.filter(id__gt=last_message_id).order_by('id')
    
    messages_list = [{
        'id': m.id,
        'text': m.text,
        'sender_id': m.sender.id,
        'created_at': m.created_at.strftime('%H:%M'),
    } for m in messages]
    
    return JsonResponse({'messages': messages_list})

@login_required
def get_chats(request):
    chats = request.user.chats.all().prefetch_related('participants', 'messages').order_by('-updated_at')
    chats_list = []
    
    for chat in chats:
        other_user = chat.participants.exclude(id=request.user.id).first()
        last_message = chat.get_last_message()
        
        chats_list.append({
            'id': chat.id,
            'other_user': {
                'id': other_user.id,
                'name': other_user.name,
            },
            'last_message': last_message.text if last_message else '',
            'unread_count': chat.get_unread_count(request.user),
            'updated_at': chat.updated_at.strftime('%H:%M')
        })
    
    return JsonResponse({'chats': chats_list})