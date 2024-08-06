from django.contrib import admin
from django.urls import path, include
from task2.views import ReviewEmailView, TaskUpdate, DeleteView, TaskList, CreateGroup, JoinGroupView, VerifyOtpView, LobbyView
from django.shortcuts import redirect
# from task2.views import lobby


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', TaskList.as_view(), name="task"),
    path('join-group/', JoinGroupView.as_view(), name='join-group'),
    path('reviews/', ReviewEmailView.as_view(), name="reviews"),
    path('create-group/', CreateGroup.as_view(), name="create-group"),
    path('task-update/<int:pk>/', TaskUpdate.as_view(), name="task-update"),
    path('task-delete/<int:pk>/', DeleteView.as_view(), name="task-delete"),
    path('verify-otp/', VerifyOtpView.as_view(), name='verify_otp'),
    # path('group-task/', GroupTaskList.as_view(), name='group-task'),
    path('chat-room/', LobbyView.as_view(), name= 'chat-room'),
    # path('', lambda request: redirect('task/', permanent=False)),

]