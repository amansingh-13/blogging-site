from django.urls import path
from django.contrib.auth.views import LoginView
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('signup/', views.signup, name='signup'),
    path('login/', LoginView.as_view(template_name='blogs/login.html'), name="login"),
    path('accounts/<int:user_id>/dashboard/', views.dashboard, name='dashboard'),
    path('accounts/<int:user_id>/add/', views.add, name='add'),
    path('accounts/<int:user_id>/blog/<int:blog_id>/', views.blog, name='blog'),
    path('accounts/<int:user_id>/blog/<int:blog_id>/edit/', views.edit, name='edit'),
    path('accounts/<int:user_id>/blog/<int:blog_id>/view/', views.blog_view, name='blog_view'),
    path('accounts/<int:user_id>/dashboard/view/', views.dashboard_view, name='dashboard_view'),
    path('trending/<int:days>/', views.trending, name='trending'),
    path('accounts/<int:user_id>/blog/<int:blog_id>/delete/', views.delete, name='delete'),
    path('logout/', views.logout_user, name='logout'),
    path('logout_view/', views.logout_view, name='logout_view'),
    path('accounts/<int:user_id>/blog/<int:blog_id>/comment/', views.comment, name='comment'),
]
