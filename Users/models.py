from django.contrib.auth.models import AbstractUser
from Chat import models
class User(AbstractUser):
    
    def get_unread_messages(self):
        return  models.ChatMessages.objects.filter(to_user=self, read=False).count()