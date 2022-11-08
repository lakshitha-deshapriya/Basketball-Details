# Generated by Django 4.1.3 on 2022-11-06 18:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user_details', '0006_player'),
    ]

    operations = [
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
                ('owner', models.CharField(max_length=100, null=True)),
            ],
        ),
        migrations.AlterField(
            model_name='coach',
            name='team',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user_details.team'),
        ),
        migrations.AlterField(
            model_name='player',
            name='team',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user_details.team'),
        ),
    ]