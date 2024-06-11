from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from .forms import*
from .models import *
from django.shortcuts import render, get_object_or_404
from .models import Trajet, Car, Client, Billet, Reservation

# Create your views here.

def home(request):
    return render(request, 'Home.html')

def singin(request):
    if request.method == "POST":
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            pseudo = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
        
            user = authenticate(request, username=pseudo, password=password)
        
            if user is not None:
                login(request, user)
                messages.success(request, 'Vous êtes connecté')
                return redirect("home")
            else:
                messages.error(request, "Nom d'utilisateur ou mot de passe incorect" )
    else:
        form = AuthenticationForm()
    return render(request, 'Login.html', {"form": form})

def signup(request):
    if request.method == 'POST':
        pseudo = request.POST.get("pseudo")
        nom = request.POST.get("nom")
        prenom = request.POST.get("prenom")
        email = request.POST.get("email")
        Adresse = request.POST.get("Adresse")
        contact = request.POST.get("contact")
        password = request.POST.get("password")
        
        user = User.objects.create_user(username=pseudo, first_name=prenom, last_name=nom, email=email, password=password)
        client = Client.objects.create(Adresse = Adresse, Contact= contact, user=user)
        return redirect('login')
    return render(request, 'Signup.html')

def deconnexion(request):
    logout(request)
    return redirect('home')
    

def reservation(request):
    if request.method == 'POST':
        ville_depart = request.POST.get('ville_depart')
        ville_arrive = request.POST.get('ville_arrive')
        
        # Recherche du trajet correspondant aux villes de départ et d'arrivée
        try:
            trajet = Trajet.objects.filter(Ville_Depart=ville_depart, Ville_Arrivée=ville_arrive)
        except Trajet.DoesNotExist:
            trajet = None
        
        return render(request, 'Reservation.html', {'trajet': trajet})
    else:
        return render(request, 'Reservation.html')

def destination(request):
    return render(request, 'Destination.html')

def home(request):
    if request.method == 'POST':
        ville_depart = request.POST.get('ville_depart')
        ville_arrive = request.POST.get('ville_arrive')
        date = request.POST.get('date')
        
        # Recherche du trajet correspondant aux villes de départ et d'arrivée
        try:
            trajet = Trajet.objects.filter(Ville_Depart=ville_depart, Ville_Arrivée=ville_arrive, Date=date)
        except Trajet.DoesNotExist:
            trajet = None
        
        return render(request, 'Reservation.html', {'trajet': trajet})
    else:
        return render(request, 'Home.html')


def show_reservation_form(request, trajet_id):
    trajet = get_object_or_404(Trajet, id=trajet_id)
    car = trajet.car
    sieges_disponibles = range(1, car.Capacité - car.sieges_reserves + 1)
    context = {
        'trajet': trajet,
        'car': car,
        'sieges_disponibles': sieges_disponibles,
    }
    return render(request, 'Reserver.html', context)

# def reserver(request, trajet_id):
#     trajet = get_object_or_404(Trajet, id=trajet_id)
#     car = trajet.car
#     sieges_disponibles = range(1, car.Capacité - car.sieges_reserves + 1)
#     context = {
#         'trajet': trajet,
#         'car': car,
#         'sieges_disponibles': sieges_disponibles,
#     }

#     if request.method == 'POST':
#         seat_number = int(request.POST.get('seat_number'))
#         try:
#             client = get_object_or_404(Client, user=request.user)
#         except Client.DoesNotExist:
#             return HttpResponse("Client not found", status=404)

#         try:
#             # Création du billet
#             billet = Billet.objects.create(
#                 Date_Voyage=trajet.Date,
#                 Destination=trajet.Ville_Arrivée,
#                 Depart=trajet.Ville_Depart,
#                 Numéro_Siège=seat_number,
#                 Prix=trajet.Prix
#             )

#             # Création de la réservation
#             reservation = Reservation.objects.create(
#                 client=client,
#                 trajet=trajet,
#                 Statut='Réservé',
#                 Depart=trajet.Ville_Depart,
#                 Destination=trajet.Ville_Arrivée,
#                 Numéro_Siège=seat_number,
#                 Prix=trajet.Prix,
#                 billet=billet
#             )

#             # Mise à jour du nombre de sièges réservés dans la voiture
#             car.sieges_reserves += 1
#             car.save()

#             return redirect('reservation_success')
#         except Exception as e:
#             print(f"Error during reservation: {e}")
#             return HttpResponse("Error during reservation process", status=500)

#     return render(request, 'reserver.html', context)


def confirmation(request):
    return render(request, 'Succes_reservation.html')

def error(request):
    return render(request, 'error.html')
        
def confirmation_page(request):
    return render(request, 'confirmation.html')



def reservation_voyage(request,trajet_id):
    user = request.user
    client = Client.objects.get(user=user)
    trajet = Trajet.objects.get(id = trajet_id)
    car_siege = trajet.car.Capacité
    car_siege_liste = [i for i in range(1, car_siege + 1)]  # Inclure la dernière capacité
    reservation_liste = Billet.objects.filter(Reservation__trajet=trajet)  # Filtrer par trajet spécifique
    car = [siege for siege in car_siege_liste if siege not in [reservation.Numéro_Siège for reservation in reservation_liste]]
            
    # car = range(1, trajet.car.Capacité - trajet.car.sieges_reserves + 1)
    if request.method == 'POST':
        nom = request.POST.get('nom')
        prenom = request.POST.get('prenom')
        contact = request.POST.get('contact')
        siege = request.POST.get('siege')
        try:
            contact = int(contact)
        except Exception as e:
            print(f"Error during reservation: {e}")
        
        reserve = Reservation.objects.create(
            client=client,
            trajet=trajet
        )
        
        billet = Billet.objects.create(
            Destination = trajet.Ville_Arrivée,
            Depart = trajet.Ville_Depart,
            Numéro_Siège = siege,
            Prix = trajet.Prix,
            Nom_Voyageur = nom,
            Prenom_Voyageur = prenom,
            Contact_Voyageur = contact,
            Reservation = reserve
            
        )
        
        # Générer le PDF
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="billet_{billet.id}.pdf"'
        p = canvas.Canvas(response, pagesize=A4)

        # Ajouter du contenu au PDF
        p.drawString(100, 800, "Billet de Voyage")
        p.drawString(100, 780, f"Nom: {billet.Nom_Voyageur}")
        p.drawString(100, 760, f"Prénom: {billet.Prenom_Voyageur}")
        p.drawString(100, 740, f"Contact: {billet.Contact_Voyageur}")
        p.drawString(100, 720, f"Départ: {billet.Depart}")
        p.drawString(100, 700, f"Destination: {billet.Destination}")
        p.drawString(100, 680, f"Numéro de Siège: {billet.Numéro_Siège}")
        p.drawString(100, 660, f"Prix: {billet.Prix}")

        p.showPage()
        p.save()

        return response
        
        
    return render(request, 'Reserver.html', {'place':car})
    

def billet(request):
    return render(request, 'Billet.html')

def profil(request):
    user = request.user
    client = Client.objects.get(user = user)
    reservation = Reservation.objects.filter(client = client)
    context = {
        'reservation':reservation,
        'client':client
    }
    return render(request, 'Profil.html', context)

def about(request):
    return render(request, 'About.html')
