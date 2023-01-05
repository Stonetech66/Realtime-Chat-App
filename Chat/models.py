from django.db import models
from Users.models import User
import uuid
# Create your models here.
from django.urls import reverse
class Group(models.Model):
    name=models.CharField(max_length=80)
    admin=models.ForeignKey(User, on_delete=models.CASCADE)
    description=models.TextField()
    date=models.DateTimeField(auto_now_add=True)
    members=models.ManyToManyField(User, related_name='members')
    online=models.ManyToManyField(User, related_name='online')

    class Meta:
        unique_together= ('admin', 'name')

    def join_group(self, user):
        self.members.add(user)
        self.save()

    def leave_group(self, user):
        self.members.remove(user)
        self.save()
    
    def connect(self, user):
        self.online.add(user)
        self.save()

    def get_total_online(self):
        return self.online.count()
    
    def total_members(self):
        return self.members.count()
    
    def  disconnect(self, user):
        self.online.remove(user)
        self.save()

    def get_absolute_url(self):
        return reverse('group_detail', args=[self.id])

class GroupMessage(models.Model):
    id=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    user=models.ForeignKey(User, related_name='messages', on_delete=models.CASCADE)
    group=models.ForeignKey(Group, on_delete=models.CASCADE, related_name='message')
    message=models.TextField()
    date_created=models.DateTimeField(auto_now_add=True)

class Conversation(models.Model):
    name=models.CharField(max_length=200)
    user=models.ForeignKey(User, related_name='coversations', on_delete=models.CASCADE)
    to_user=models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    last_chatted=models.DateTimeField(null=True)

    class Meta:
        ordering= ['-last_chatted']

class ChatMessages(models.Model):
    conversation=models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='messages')
    from_user=models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_sent_messages')
    to_user=models.ForeignKey(User,on_delete=models.CASCADE, related_name='user_recieved_messages')
    date=models.DateTimeField(auto_now_add=True)
    message=models.TextField()
    read=models.BooleanField(default=False)









    



