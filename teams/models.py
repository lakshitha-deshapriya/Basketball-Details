from django.db import models


class Team(models.Model):
    name = models.CharField(max_length=255, unique=True)
    owner = models.CharField(max_length=100, null=True)

    def __str__(self):
        return self.name
