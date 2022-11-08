from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model
from django.db.models import Avg

from .validator import Validator
from .serializer import UserSerializer, CoachSerializer, PlayerSerializer
from .forms import UserForm
from .models import User, Coach, Player

from match_stat.models import PlayerStat


class UserControl(APIView):
    def get(self, request):
        authStatus = Validator.validateUser(user=request.user, types=['A'])
        if authStatus != status.HTTP_200_OK:
            return Response('Unauthorized', status=authStatus)

        users = get_user_model().objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        authStatus = Validator.validateUser(user=request.user, types=['A'])
        if authStatus != status.HTTP_200_OK:
            return Response('Unauthorized', status=authStatus)

        form = UserForm(request.POST)
        if form.is_valid():
            cleaned_data = form.cleaned_data
            username = cleaned_data.get('username')
            password = cleaned_data.get('password')
            email = cleaned_data.get('email')
            role = cleaned_data.get('role')

        user = User.objects.create_user(username, email, role, password)
        user.admin = (role == 'A')
        user.staff = (role == 'A')

        user.save()
        return Response('Done', status=status.HTTP_200_OK)


class UserDetail(APIView):
    def get(self, request, username):
        authStatus = Validator.validateUser(user=request.user, types=['A'])
        if authStatus != status.HTTP_200_OK:
            return Response('Unauthorized', status=authStatus)

        user = get_user_model().objects.filter(username=username).first()
        if not user:
            return Response('Invalid username', status=status.HTTP_400_BAD_REQUEST)

        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, username):
        authStatus = Validator.validateUser(user=request.user, types=['A'])
        if authStatus != status.HTTP_200_OK:
            return Response('Unauthorized', status=authStatus)

        user = get_user_model().objects.filter(username=username).first()
        if not user:
            return Response('Invalid username', status=status.HTTP_400_BAD_REQUEST)

        serializer = UserSerializer(user, request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response('Invalid data', status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, username):
        authStatus = Validator.validateUser(user=request.user, types=['A'])
        if authStatus != status.HTTP_200_OK:
            return Response('Unauthorized', status=authStatus)

        user = get_user_model().objects.filter(username=username).first()
        if not user:
            return Response('Invalid username', status=status.HTTP_400_BAD_REQUEST)

        user.delete()
        return Response('Successfully deleted', status=status.HTTP_204_NO_CONTENT)


class CoachControl(APIView):
    def get(self, request):
        authStatus = Validator.validateUser(user=request.user, types=['A'])
        if authStatus != status.HTTP_200_OK:
            return Response('Unauthorized', status=authStatus)

        coaches = Coach.objects.all()
        serializer = CoachSerializer(coaches, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        authStatus = Validator.validateUser(user=request.user, types=['A'])
        if authStatus != status.HTTP_200_OK:
            return Response('Unauthorized', status=authStatus)

        serializer = CoachSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CoachDetail(APIView):
    def get(self, request, id):
        authStatus = Validator.validateUser(user=request.user, types=['A'])
        if authStatus != status.HTTP_200_OK:
            return Response('Unauthorized', status=authStatus)

        coach = Coach.objects.filter(id=id).first()
        if not coach:
            return Response('Invalid Id', status=status.HTTP_400_BAD_REQUEST)

        serializer = CoachSerializer(coach)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, id):
        authStatus = Validator.validateUser(user=request.user, types=['A'])
        if authStatus != status.HTTP_200_OK:
            return Response('Unauthorized', status=authStatus)

        coach = Coach.objects.filter(id=id).first()
        if not coach:
            return Response('Invalid Id', status=status.HTTP_400_BAD_REQUEST)

        serializer = CoachSerializer(coach, request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        authStatus = Validator.validateUser(user=request.user, types=['A'])
        if authStatus != status.HTTP_200_OK:
            return Response('Unauthorized', status=authStatus)

        coach = Coach.objects.filter(id=id).first()
        if not coach:
            return Response('Invalid Id', status=status.HTTP_400_BAD_REQUEST)

        coach.delete()
        return Response('Successfully deleted', status=status.HTTP_204_NO_CONTENT)


class PlayerControl(APIView):
    def get(self, request):
        authStatus = Validator.validateUser(user=request.user, types=['A'])
        if authStatus != status.HTTP_200_OK:
            return Response('Unauthorized', status=authStatus)

        player = Player.objects.all()
        serializer = PlayerSerializer(player, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        authStatus = Validator.validateUser(user=request.user, types=['A'])
        if authStatus != status.HTTP_200_OK:
            return Response('Unauthorized', status=authStatus)

        serializer = PlayerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PlayerDetail(APIView):
    def get(self, request, id):
        authStatus = Validator.validateUser(user=request.user, types=['A','C'])
        if authStatus != status.HTTP_200_OK:
            return Response('Unauthorized', status=authStatus)

        player_prof = Player.objects.filter(id=id).first()
        if not player_prof:
            return Response('Invalid Id', status=status.HTTP_400_BAD_REQUEST)
        
        # Allow coach to see only his team player details
        if request.user.role == 'C':
            coachStatus = Validator.validateTeamOfCoach(request.user, player_prof.team.id)
            if coachStatus != status.HTTP_200_OK:
                return Response('Unauthorized', status=coachStatus)

        stats = PlayerStat.objects.filter(player=player_prof).all()
        avgScore = stats.aggregate(Avg('score')).get('score__avg')
        if not avgScore:
            avgScore = 0

        serializer = PlayerSerializer(player_prof)

        context = {
            'playerDetails': serializer.data,
            'avgScore': avgScore,
            'playedGames':len(stats)
        }
        return Response(context, status=status.HTTP_200_OK)

    def put(self, request, id):
        authStatus = Validator.validateUser(user=request.user, types=['A'])
        if authStatus != status.HTTP_200_OK:
            return Response('Unauthorized', status=authStatus)

        player = Player.objects.filter(id=id).first()
        if not player:
            return Response('Invalid Id', status=status.HTTP_400_BAD_REQUEST)

        serializer = PlayerSerializer(player, request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        authStatus = Validator.validateUser(user=request.user, types=['A'])
        if authStatus != status.HTTP_200_OK:
            return Response('Unauthorized', status=authStatus)

        player = Player.objects.filter(id=id).first()
        if not player:
            return Response('Invalid Id', status=status.HTTP_400_BAD_REQUEST)

        player.delete()
        return Response('Successfully deleted', status=status.HTTP_204_NO_CONTENT)
