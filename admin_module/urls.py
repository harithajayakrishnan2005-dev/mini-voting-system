from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = 'admin_module'

urlpatterns = [
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('polls/', views.poll_list_admin, name='poll_list'),
    path('polls/add/', views.add_poll, name='add_poll'),
    path('votes/', views.vote_list, name='vote_list'),
    path('feedback/', views.feedback_list, name='feedback_list'),
    path('polls/edit/<int:poll_id>/', views.edit_poll, name='edit_poll'),
    path('polls/delete/<int:poll_id>/', views.delete_poll, name='delete_poll'),
    path('login/', views.admin_login, name='admin_login'),
    path('logout/', views.admin_logout, name='admin_logout'),

]
