from django.contrib import admin
from .models import *

@admin.register(Car)
class CarAdmnin(admin.ModelAdmin):
    list_display = ["Capacité", "Disponibilité"]

@admin.register(Client)
class ClientAdmnin(admin.ModelAdmin):
    list_display = ["user", "Adresse", "Contact"]
    
@admin.register(Trajet)
class TrajetAdmnin(admin.ModelAdmin):
    list_display = ["car", "Ville_Depart", "Ville_Arrivée", "Heure_Depart", "Heure_Arrivée"]
    
@admin.register(Reservation)
class ReservationAdmnin(admin.ModelAdmin):
    list_display = ["client", "trajet", "Date_Reservation", "Statut", "billet"]
    
@admin.register(Billet)
class BilletAdmnin(admin.ModelAdmin):
    list_display = ["Destination", "Depart", "Numéro_Siège", "Prix", "Nom_Voyageur","Prenom_Voyageur","Contact_Voyageur"]