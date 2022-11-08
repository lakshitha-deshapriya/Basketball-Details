from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import Match
from .serializer import MatchSerializer

from user_details.validator import Validator

class MatchControl(APIView):
    def get(self, request):
        authStatus = Validator.validateUser(user=request.user, types=['A','C','P'])
        if authStatus != status.HTTP_200_OK:
            return Response('Unauthorized', status=authStatus)

        matches = Match.objects.all()
        serializer = MatchSerializer(matches, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class MatchDetail(APIView):
    def get(self, request, id):
        authStatus = Validator.validateUser(user=request.user, types=['A','C','P'])
        if authStatus != status.HTTP_200_OK:
            return Response('Unauthorized', status=authStatus)

        match = Match.objects.filter(id=id).first()
        if not match:
            return Response('Invalid Id', status=status.HTTP_400_BAD_REQUEST)

        serializer = MatchSerializer(match)
        return Response(serializer.data, status=status.HTTP_200_OK)
