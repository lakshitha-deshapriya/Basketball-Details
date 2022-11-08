# Generated by Django 4.1.3 on 2022-11-07 11:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('teams', '0001_initial'),
        ('match_stat', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='match',
            name='date',
        ),
        migrations.AlterField(
            model_name='match',
            name='winner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='winner', to='teams.team'),
        ),
    ]
