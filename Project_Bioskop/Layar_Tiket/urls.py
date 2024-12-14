from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('home/<str:id>/', views.base, name='base'),
    path('home/<str:id>/<str:judul>/', views.film, name='film'),
]
