# Generated by Django 4.2.14 on 2024-09-28 19:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('gun', '0001_initial'),
        ('evenement', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='inscription',
            name='amis_repliques',
            field=models.ManyToManyField(blank=True, related_name='repliques_inscriptions_ami', to='gun.gun'),
        ),
        migrations.AddField(
            model_name='inscription',
            name='replique_ami',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='repliques_ami', to='gun.gun'),
        ),
    ]
