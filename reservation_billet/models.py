from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Client(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    Adresse = models.CharField(max_length=250)
    Contact = models.CharField(max_length=15)
    
    def __str__(self) -> str:
        return f"{self.user.first_name}-{self.user.last_name}"

class Car(models.Model):
    Numero_Car = models.IntegerField()
    Capacité = models.IntegerField()
    Disponibilité = models.BooleanField()
    Numéro_siège = models.IntegerField(default=50)
    sieges_reserves = models.IntegerField(default=0) 
    
    def __str__(self) -> str:
        return f"{self.Numero_Car}"

class Trajet(models.Model):
    car = models.ForeignKey(Car, on_delete=models.DO_NOTHING)
    Ville_Depart = models.CharField(max_length=250)
    Ville_Arrivée = models.CharField(max_length=250)
    Prix = models.FloatField()
    Date = models.DateField()
    Heure_Depart = models.TimeField()
    Heure_Arrivée = models.TimeField()
    
    def __str__(self) -> str:
        return f"{self.Ville_Depart}-{self.Ville_Arrivée}"

class Reservation(models.Model):
    client = models.ForeignKey(Client, on_delete=models.DO_NOTHING)
    trajet = models.ForeignKey(Trajet, on_delete=models.DO_NOTHING)
    Date_Reservation = models.DateField(auto_now_add=True)
    Statut = models.CharField(max_length=250, default="accepter")
    

class Billet(models.Model):
    Destination = models.CharField(max_length=250)
    Depart = models.CharField(max_length=250)
    Numéro_Siège = models.IntegerField()
    Prix = models.FloatField()  # Ajusté ici
    Nom_Voyageur = models.CharField(max_length=250, default='dede')
    Prenom_Voyageur = models.CharField(max_length=250, default='dede')
    Contact_Voyageur = models.CharField(max_length=15)
    Reservation = models.OneToOneField(Reservation, on_delete=models.DO_NOTHING)
    

