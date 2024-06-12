from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from weasyprint import HTML
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
    villes_depart = Trajet.objects.values_list('Ville_Depart', flat=True).distinct()
    villes_arrivee = Trajet.objects.values_list('Ville_Arrivée', flat=True).distinct()

    print("Villes de départ:", villes_depart)
    print("Villes d'arrivée:", villes_arrivee)
    
    if request.method == 'POST':
        ville_depart = request.POST.get('ville_depart')
        ville_arrive = request.POST.get('ville_arrive')
        date = request.POST.get('date')
        
        trajets = Trajet.objects.filter(Ville_Depart=ville_depart, Ville_Arrivée=ville_arrive, Date=date)
        
        return render(request, 'Reservation.html', {'trajets': trajets})
    else:
        return render(request, 'Home.html', {'villes_depart': villes_depart, 'villes_arrivee': villes_arrivee})


def singin(request):
    if request.method == "POST":
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            pseudo = form.cleaned_data["username"]
            password = form.cleaned_data["password"]

            # Vérifier si le mot de passe est trop court
            if len(password) < 8:
                messages.error(request, 'Le mot de passe doit contenir au moins 8 caractères.')
            else:
                user = authenticate(request, username=pseudo, password=password)

                if user is not None:
                    login(request, user)
                    messages.success(request, 'Vous êtes connecté')
                    return redirect("home")
                else:
                    messages.error(request, "Nom d'utilisateur ou mot de passe incorrect")
        else:
            messages.error(request, "Nom d'utilisateur ou mot de passe incorrect")
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
    villes_depart = Trajet.objects.values_list('Ville_Depart', flat=True).distinct()
    villes_arrivee = Trajet.objects.values_list('Ville_Arrivée', flat=True).distinct()

    print("Villes de départ:", villes_depart)
    print("Villes d'arrivée:", villes_arrivee)

    trajets = []
    ville_depart = ''
    ville_arrive = ''

    if request.method == 'POST':
        ville_depart = request.POST.get('ville_depart')
        ville_arrive = request.POST.get('ville_arrive')
        
        trajets = Trajet.objects.filter(Ville_Depart=ville_depart, Ville_Arrivée=ville_arrive)

    return render(request, 'Reservation.html', {
        'villes_depart': villes_depart,
        'villes_arrivee': villes_arrivee,
        'trajets': trajets,
        'selected_ville_depart': ville_depart,
        'selected_ville_arrive': ville_arrive,
    })

def destination(request):
    return render(request, 'Destination.html')

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

def reservation_voyage(request, trajet_id):
    user = request.user
    client = Client.objects.get(user=user)
    trajet = Trajet.objects.get(id=trajet_id)
    car_siege = trajet.car.Capacité
    car_siege_liste = [i for i in range(1, car_siege + 1)]
    
    reservation_liste = Billet.objects.filter(Reservation__trajet=trajet)
    car = [siege for siege in car_siege_liste if siege not in [reservation.Numéro_Siège for reservation in reservation_liste]]

    if request.method == 'POST':
        # Récupérer les données du formulaire
        seat_number = request.POST.get('siege')
        nom = request.POST.get('nom')
        prenom = request.POST.get('prenom')
        contact = request.POST.get('contact')

        # Déterminer le prix du billet
        prix = trajet.Prix  # Assumant que le prix du trajet est stocké dans l'objet `trajet`

        # Créer une nouvelle réservation et billet
        reservation = Reservation.objects.create(trajet=trajet, client=client)
        billet = Billet.objects.create(Reservation=reservation, Nom_Voyageur=nom, Prenom_Voyageur=prenom, Numéro_Siège=seat_number, Prix=prix)

        # Contexte pour le template
        context = {
            'billet': billet,
            'trajet': trajet,
            'client': client,
        }

        # Générer le PDF
        html_string = render_to_string('print_ticket.html', context)
        html = HTML(string=html_string)
        pdf_file = html.write_pdf()

        # Retourner le PDF comme réponse
        response = HttpResponse(pdf_file, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="billet_{billet.id}.pdf"'
        return response

    return render(request, 'Reserver.html', {'place': car})



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

def generate_ticket(request):
    if request.method == 'POST':
        # Récupérer les données du formulaire
        car_id = request.POST.get('car_id')
        seat_number = request.POST.get('siege')
        nom = request.POST.get('nom')
        prenom = request.POST.get('prenom')
        contact = request.POST.get('contact')
        
        # Créer ou récupérer le trajet
        trajet = get_object_or_404(Trajet, id=car_id)
        
        # Créer une nouvelle réservation et billet
        reservation = Reservation.objects.create(trajet=trajet, client=request.user)
        billet = Billet.objects.create(Reservation=reservation, Nom_Voyageur=nom, Prenom_Voyageur=prenom, Numéro_Siège=seat_number)
        
        # Contexte pour le template
        context = {
            'billet': billet,
            'trajet': trajet,
            'client': request.user,
        }

        # Générer le PDF
        html_string = render_to_string('print_ticket.html', context)
        html = HTML(string=html_string)
        pdf_file = html.write_pdf()

        # Retourner le PDF comme réponse
        response = HttpResponse(pdf_file, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="billet_{billet.id}.pdf"'
        return response
    return redirect('reservation')  # Rediriger en cas de méthode GET ou erreur
