# Generated by Django 5.0.4 on 2024-05-16 07:34

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Billet',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Date_Voyage', models.DateField()),
                ('Destination', models.CharField(max_length=250)),
                ('Depart', models.CharField(max_length=250)),
                ('Numéro_Siège', models.IntegerField()),
                ('Prix', models.DecimalField(decimal_places=2, max_digits=10)),
            ],
        ),
        migrations.CreateModel(
            name='Car',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Numero_Car', models.IntegerField()),
                ('Capacité', models.IntegerField()),
                ('Disponibilité', models.BooleanField()),
            ],
        ),
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Adresse', models.CharField(max_length=250)),
                ('Contact', models.IntegerField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Trajet',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Ville_Depart', models.CharField(max_length=250)),
                ('Ville_Arrivée', models.CharField(max_length=250)),
                ('Prix', models.FloatField()),
                ('Date', models.DateField()),
                ('Heure_Depart', models.TimeField()),
                ('Heure_Arrivée', models.TimeField()),
                ('car', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='reservation_billet.car')),
            ],
        ),
        migrations.CreateModel(
            name='Reservation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Date_Reservation', models.DateField(auto_now_add=True)),
                ('Statut', models.CharField(max_length=250)),
                ('Depart', models.CharField(max_length=250)),
                ('Destination', models.CharField(max_length=250)),
                ('Numéro_Siège', models.IntegerField()),
                ('Prix', models.DecimalField(decimal_places=2, max_digits=10)),
                ('billet', models.OneToOneField(on_delete=django.db.models.deletion.DO_NOTHING, to='reservation_billet.billet')),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='reservation_billet.client')),
                ('trajet', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='reservation_billet.trajet')),
            ],
        ),
    ]