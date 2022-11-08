from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Avg

from .models import Team
from .serializer import TeamSerializer

from user_details.models import Player
from user_details.serializer import PlayerSerializer
from user_details.validator import Validator

from match_stat.models import MatchStat, PlayerStat


class TeamControl(APIView):
    def get(self, request):
        authStatus = Validator.validateUser(user=request.user, types=['A'])
        if authStatus != status.HTTP_200_OK:
            return Response('Unauthorized', status=authStatus)

        teams = Team.objects.all()
        serializer = TeamSerializer(teams, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        authStatus = Validator.validateUser(user=request.user, types=['A'])
        if authStatus != status.HTTP_200_OK:
            return Response('Unauthorized', status=authStatus)

        serializer = TeamSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response('Invalid data', status=status.HTTP_400_BAD_REQUEST)


class TeamDetail(APIView):
    def get(self, request, id):
        authStatus = Validator.validateUser(
            user=request.user, types=['A', 'C'])
        if authStatus != status.HTTP_200_OK:
            return Response('Unauthorized', status=authStatus)

        team = Team.objects.filter(id=id).first()
        if not team:
            return Response('Invalid Id', status=status.HTTP_400_BAD_REQUEST)

        #Allow coach to see only his team details
        if request.user.role == 'C':
            coachStatus = Validator.validateTeamOfCoach(request.user, id)
            if coachStatus != status.HTTP_200_OK:
                return Response('Unauthorized', status=coachStatus)

        #90th percentile filter identification query param
        filterResult = request.GET.get('filterPlayers').lower() == 'true'

        players = Player.objects.filter(team=id).all()
        if filterResult:
            #get the 90th percentile avg score players
            players = self._getFilteredPlayers(players=players)

        playerSerializer = PlayerSerializer(players, many=True)

        #Team average score
        avgScore = MatchStat.objects.filter(
            team=team).aggregate(Avg('score')).get('score__avg')

        serializer = TeamSerializer(team)
        context = {
            'teamDetails': serializer.data,
            'players': playerSerializer.data,
            'avgScore': avgScore
        }
        return Response(context, status=status.HTTP_200_OK)
    
    def put(self, request, id):
        authStatus = Validator.validateUser(user=request.user, types=['A'])
        if authStatus != status.HTTP_200_OK:
            return Response('Unauthorized', status=authStatus)

        team = Team.objects.filter(id=id).first()
        if not team:
            return Response('Invalid Id', status=status.HTTP_400_BAD_REQUEST)

        serializer = TeamSerializer(team, request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        authStatus = Validator.validateUser(user=request.user, types=['A'])
        if authStatus != status.HTTP_200_OK:
            return Response('Unauthorized', status=authStatus)

        team = Team.objects.filter(id=id).first()
        if not team:
            return Response('Invalid Id', status=status.HTTP_400_BAD_REQUEST)

        team.delete()
        return Response('Successfully deleted', status=status.HTTP_204_NO_CONTENT)

    def _getFilteredPlayers(self, players):
        playerAvg = {}
        for player in players:
            avgScore = PlayerStat.objects.filter(
                player=player).aggregate(Avg('score')).get('score__avg')
            if not avgScore:
                avgScore = 0
            playerAvg[player.id] = avgScore

        sortedAvgs = sorted(playerAvg.values(), reverse=True)

        percentileAvg = sortedAvgs[1]

        playerList = []
        index = 0
        for key in playerAvg:
            if playerAvg[key] >= percentileAvg:
                playerList.insert(index, key)
                index = index+1

        return players.filter(id__in=playerList).all()
