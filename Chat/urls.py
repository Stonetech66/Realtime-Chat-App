from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenObtainPairView
urlpatterns=[ 
    path('', views.groups),
    path('<int:pk>/', views.group, name='group_detail'),
    path('groups/', views.GroupList.as_view()),
    path('group/<int:pk>', views.GroupDetails.as_view()),
    path('token/', TokenObtainPairView.as_view()),
    path('create-room/', views.CreateGroup.as_view()),
    path('join-room/<int:group_id>/',views.JoinGroup.as_view()),
    path('leave-room/<int:group_id>/', views.LeaveGroup.as_view()),
    path('chat/history', views.ChatHistory.as_view()), 
]