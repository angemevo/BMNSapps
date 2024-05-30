# Generated by Django 5.0.4 on 2024-05-28 11:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reservation_billet', '0003_car_numéro_siège'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='billet',
            name='Date_Voyage',
        ),
        migrations.RemoveField(
            model_name='reservation',
            name='Depart',
        ),
        migrations.RemoveField(
            model_name='reservation',
            name='Destination',
        ),
        migrations.RemoveField(
            model_name='reservation',
            name='Numéro_Siège',
        ),
        migrations.RemoveField(
            model_name='reservation',
            name='Prix',
        ),
        migrations.AddField(
            model_name='billet',
            name='Contact_Voyageur',
            field=models.IntegerField(default=123),
        ),
        migrations.AddField(
            model_name='billet',
            name='Nom_Voyageur',
            field=models.CharField(default='dede', max_length=250),
        ),
        migrations.AddField(
            model_name='billet',
            name='Prenom_Voyageur',
            field=models.CharField(default='dede', max_length=250),
        ),
        migrations.AlterField(
            model_name='reservation',
            name='Statut',
            field=models.CharField(default='accepter', max_length=250),
        ),
    ]