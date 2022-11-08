# Generated by Django 4.1.3 on 2022-11-06 19:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('teams', '0001_initial'),
        ('user_details', '0007_team_alter_coach_team_alter_player_team'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coach',
            name='team',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='teams.team'),
        ),
        migrations.AlterField(
            model_name='player',
            name='team',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='teams.team'),
        ),
        migrations.DeleteModel(
            name='Team',
        ),
    ]