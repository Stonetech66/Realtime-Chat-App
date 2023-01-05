from django.shortcuts import render
from .models import User
from django.shortcuts import get_object_or_404
from .models import  Group,Conversation
from .serializers import GroupCreateSerializer,ChatHistorySerializer, GroupDetailSerializer, GroupListSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView
from .models import Group
# Create your views here.

def group(request, pk):
    x=get_object_or_404(Group, id=pk)
    return render(request, 'group.html', {'group':x ,'pk':pk})

def groups(request):
    x=Group.objects.all()
    return render(request, 'groups.html', {'groups':x})

def chat(request, username):
    u=get_object_or_404(User, username=username)
    return render(request, 'new.html', {'user':u, 'pk':username})

class GroupList(ListAPIView):
    queryset=Group.objects.all()
    serializer_class=GroupListSerializer

class GroupDetails(RetrieveAPIView):
    queryset=Group.objects.all()
    serializer_class=GroupDetailSerializer
     
class JoinGroup(APIView):
    def post(self, request, *args, **kwargs):
        group=self.kwargs['group_id']
        R=get_object_or_404(Group, id=group)
        R.join_group(request.user)
        return Response({'message':'successfuly joined room'})

class LeaveGroup(APIView):
    def post(self, request, *args, **kwargs):
        group=self.kwargs['group_id']
        R=get_object_or_404(Group, id=group)
        R.leave_group(request.user)
        return Response({'message':'successfuly left room'})


class CreateGroup(CreateAPIView):
    queryset=Group.objects.all()
    serializer_class=GroupCreateSerializer

    def perform_create(self, serializer):
        return serializer.save(admin=self.request.user)


class ChatHistory(ListAPIView):
    serializer_class=ChatHistorySerializer

    def get_queryset(self):
        return Conversation.objects.filter(user=User.objects.get(id=self.request.user))

 

