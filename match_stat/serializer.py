from rest_framework import serializers

from .models import Match


class MatchSerializer(serializers.ModelSerializer):
    team1 = serializers.SerializerMethodField(read_only=True)
    team2 = serializers.SerializerMethodField(read_only=True)
    winner = serializers.SerializerMethodField(read_only=True)
    round = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Match
        fields = ['id', 'team1', 'team2', 'team1Score',
                  'team2Score', 'winner', 'round']

    def get_team1(self, obj):
        return obj.team1.name

    def get_team2(self, obj):
        return obj.team2.name

    def get_winner(self, obj):
        return obj.winner.name

    def get_round(self, obj):
        if obj.round == 'RS':
            return 'Round of 16'
        elif obj.round == 'QF':
            return 'Quater Final'
        elif obj.round == 'SF':
            return 'Semi Final'
        else:
            return 'Final'
