from django.urls import path
from . import views

app_name = 'user'

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path("feedback/", views.submit_feedback, name="feedback"),
    path('', views.index, name='index'),
    path('dashboard/', views.user_dashboard, name='dashboard'),
    path('profile/', views.user_profile, name='profile'),
    path('my_vote/', views.my_votes, name='my_vote'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('poll_list/', views.poll_list, name='poll_list'),
    path('vote/<int:poll_id>/', views.submit_vote, name='submit_vote'),
    path('poll_results/<int:poll_id>/', views.poll_results, name='poll_results'),

]