from django.db import models

from teams.models import Team

from user_details.models import Player

RS = 'RS'
QF = 'QF'
SF = 'SF'
FI = 'FI'


class Match(models.Model):
    ROUNDS = [
        (RS, 'Round 16'),
        (QF, 'Quarter Final'),
        (SF, 'Semi Final'),
        (FI, 'Final')
    ]
    team1 = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='team1')
    team2 = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='team2')
    team1Score = models.IntegerField()
    team2Score = models.IntegerField()
    winner = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='winner')
    round = models.CharField(max_length=2, choices=ROUNDS, default=RS)

    def __str__(self):
        return self.team1.name + ' VS ' + self.team2.name
    
class MatchStat(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    match = models.ForeignKey(Match, on_delete=models.CASCADE)
    score = models.IntegerField()
    
    def __str__(self):
        return self.team.name + ' - ' + str(self.match) + ' - ' + str(self.score)
    
class PlayerStat(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    match = models.ForeignKey(Match, on_delete=models.CASCADE)
    score = models.IntegerField()
    
    def __str__(self):
        return self.player.name + ' - ' + str(self.match) + ' - ' + str(self.score)
