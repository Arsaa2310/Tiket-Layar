from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('home/<str:id_pelanggan>/', views.base, name='base'),
    path('home/<str:id_pelanggan>/Profil/', views.profil, name='profil'),
    path('home/<str:id_pelanggan>/<str:judul>/', views.film, name='film'),
]
