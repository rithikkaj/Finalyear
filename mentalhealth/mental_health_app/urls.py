from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_choice, name='login'),
    path('user_login/', views.login_view, name='user_login'),
    path('signup/', views.signup_view, name='signup'),
    path('user_signup/', views.signup_view, name='user_signup'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('assessment/', views.assessment, name='assessment'),
    path('chatbot/', views.chatbot, name='chatbot'),
    path('profile/', views.profile, name='profile'),
    path('games/', views.games, name='games'),
    path('exercise/', views.exercise, name='exercise'),
    path('games/breathing/', views.breathing, name='breathing'),
    path('games/puzzle/', views.puzzle, name='puzzle'),
    path('games/memory-puzzle/', views.memory_puzzle, name='memory_puzzle'),
    path('games/meditation/', views.meditation, name='meditation'),
    path('admin_login/', views.login_view, name='admin_login'),
    path('admin_signup/', views.signup_view, name='admin_signup'),
    path('admin/', views.admin_dashboard, name='admin_redirect'),
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('user_history/<int:user_id>/', views.user_history, name='user_history'),
    path('articles/', views.articles, name='articles'),
    path('articles/<slug:slug>/', views.article_detail, name='article_detail'),
    path('logout/', views.logout_view, name='logout'),
]
