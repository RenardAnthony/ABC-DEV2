from django.contrib import admin
from .models import ChatRoom, Message

@admin.register(ChatRoom)
class ChatRoomAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_general', 'created_at', 'updated_at')
    search_fields = ('name',)
    list_filter = ('is_general',)

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('room', 'user', 'content', 'is_deleted', 'created_at', 'updated_at')
    search_fields = ('content', 'user__username')
    list_filter = ('is_deleted', 'created_at')
