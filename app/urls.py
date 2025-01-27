from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views

urlpatterns = [
    path('', views.index, name="index" ),
    path('auth/register/', views.register, name="register" ),
    path('auth/login/', views.user_login, name="user_login" ),
    path('logout/', views.logout_user, name='logout'),
    path('inbox/', views.inbox, name="inbox" ),
    path('inbox/delete/<int:note_id>/', views.delete_note, name='delete_message'),
    path('inbox/write/', views.write, name="write" ),
    path('inbox/sent/', views.sent, name="sent" ),
    path('inbox/sent/delete/<int:note_id>/', views.delete_note, name='delete_message'),
]
