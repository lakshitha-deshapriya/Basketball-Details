from django.contrib.auth import get_user_model
from rest_framework import status

from .models import Coach


class Validator():
    def validateUser(user, types):
        if not user.is_authenticated:
            return status.HTTP_401_UNAUTHORIZED
        user = get_user_model().objects.filter(username=user).first()
        for type in types:
            if type == user.role:
                return status.HTTP_200_OK
        return status.HTTP_403_FORBIDDEN

    def validateTeamOfCoach(user, teamId):
        coach = Coach.objects.filter(user=user.id).first()
        if not coach:
            return status.HTTP_400_BAD_REQUEST
        elif coach.team.id != teamId:
            return status.HTTP_403_FORBIDDEN
        return status.HTTP_200_OK