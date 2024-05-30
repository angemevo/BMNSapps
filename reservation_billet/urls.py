from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name= "home"),
    path('login/', views.singin, name="login"),
    path('signup/', views.signup, name="signup"),
    path('reservation/', views.reservation, name="reservation"),
    path('destination/', views.destination, name="destination"),
    path('profil/', views.profil, name="profil"),
    path('deconnexion/', views.deconnexion, name="logout"),
    path('reserver/<int:trajet_id>/', views.show_reservation_form, name='show_reservation_form'),
    # path('reserver/<int:trajet_id>/', views.reserver, name='reserver'),
    path('confirmation/', views.confirmation, name="confirmation"),
    # path('deconnexion/', views.deconnexion, name="logout"),
    path("reserve/<int:trajet_id>/", views.reservation_voyage, name='reserve'),
    path('billet/', views.billet, name="billet")
]
