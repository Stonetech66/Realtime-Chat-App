from django.contrib import admin
from .models import Group, GroupMessage, ChatMessages
# Register your models here.
admin.site.register(Group)
admin.site.register(GroupMessage)