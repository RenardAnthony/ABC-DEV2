# Generated by Django 4.2.14 on 2024-09-29 08:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('evenement', '0002_inscription_amis_repliques_inscription_replique_ami'),
    ]

    operations = [
        migrations.AddField(
            model_name='inscription',
            name='montant_total',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=6),
        ),
    ]