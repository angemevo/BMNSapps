# Generated by Django 5.0.4 on 2024-05-30 22:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reservation_billet', '0008_alter_billet_prix_alter_trajet_prix'),
    ]

    operations = [
        migrations.AlterField(
            model_name='billet',
            name='Contact_Voyageur',
            field=models.CharField(max_length=15),
        ),
        migrations.AlterField(
            model_name='client',
            name='Contact',
            field=models.CharField(max_length=15),
        ),
    ]
