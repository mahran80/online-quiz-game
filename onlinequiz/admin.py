from django.contrib import admin
from .models import ChatRoom
from .models import ChatMessage
# Register your models here.
admin.site.register(ChatRoom)
admin.site.register(ChatMessage)