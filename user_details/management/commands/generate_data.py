from django.core.management.base import BaseCommand
from user_details.models import User, Coach, Player
from teams.models import Team
from match_stat.models import Match, MatchStat, PlayerStat
from faker import Faker
import random
import traceback


class Command(BaseCommand):
    def superUser(self, faker):
        try:
            User.objects.create_superuser(
                'admin', faker.email(), 'A', 'admin')
            self.stdout.write(self.style.SUCCESS(
                'Superuser created successfully'))
        except:
            self.stdout.write(self.style.WARNING(
                'Superuser with username admin creation failed'))

    def createTeamData(self, faker):
        for x in range(16):
            teamName = 'team_' + str(x+1)
            owner = faker.name_male()
            try:
                team = Team(name=teamName, owner=owner)
                team.save()
                self.stdout.write(self.style.SUCCESS(
                    'Team created: ' + teamName))
            except:
                self.stdout.write(self.style.WARNING(
                    'Team creation failed: ' + teamName))

    def createCoaches(self, teams, faker):
        for team in teams:
            try:
                username = team.name + '_coach'
                user = User.objects.create_user(
                    username, faker.email(), 'C', 'coach')
                coach = Coach(user=user, team=team, name=faker.name_male())
                coach.save()
                self.stdout.write(self.style.SUCCESS(
                    'Coach created: ' + username))
            except:
                self.stdout.write(self.style.WARNING(
                    'Coach creation failed: ' + username))

    def createPlayers(self, teams, faker):
        for team in teams:
            for x in range(10):
                username = team.name + '_player' + str(x+1)
                self.createPlayerForTeam(team, faker, username)

    def createPlayerForTeam(self, team, faker, username):
        try:
            user = User.objects.create_user(
                username, faker.email(), 'P', 'player')

            player = Player(user=user, team=team, name=faker.name_male(
            ), height=random.randrange(150, 170), age=random.randrange(20, 33))
            player.save()
            self.stdout.write(self.style.SUCCESS(
                'Player created: ' + username))
        except:
            self.stdout.write(self.style.WARNING(
                'player creation failed: ' + username))

    def createMatchStats(self, teams):
        winners = self.createLevelmatchStat(teams, 'RS')

        winners = self.createLevelmatchStat(winners, 'QF')

        winners = self.createLevelmatchStat(winners, 'SF')

        self.createLevelmatchStat(winners, 'FI')

    def getRandomPlayerScore(self, count):
        scoreArr = []
        for x in range(count):
            scoreArr.insert(x, random.randrange(3, 25))

        return scoreArr

    def createLevelmatchStat(self, teams, round):
        winners = []
        firstTeam = None
        for team in teams:
            if firstTeam:
                try:
                    firstScoreArr = self.getRandomPlayerScore(5)
                    firstTotal = sum(firstScoreArr)

                    secondScoreArr = self.getRandomPlayerScore(5)
                    secondTotal = sum(secondScoreArr)

                    if firstTotal > secondTotal:
                        winner = firstTeam
                    elif firstTotal == secondTotal:
                        winner = firstTeam
                        firstTotal = firstTotal + 1
                        firstScoreArr[0] = firstScoreArr[0]+1
                    else:
                        winner = team

                    match = Match(team1=firstTeam, team2=team, team1Score=firstTotal,
                                  team2Score=secondTotal, winner=winner, round=round)
                    match.save()

                    matchStat1 = MatchStat(
                        team=firstTeam, match=match, score=firstTotal)
                    matchStat1.save()

                    matchStat2 = MatchStat(
                        team=team, match=match, score=secondTotal)
                    matchStat2.save()

                    self.createPlayerStats(
                        match=match, playerTeam=firstTeam, scoreArr=firstScoreArr)
                    self.createPlayerStats(
                        match=match, playerTeam=team, scoreArr=secondScoreArr)

                    winners.insert(len(winners), winner)
                    firstTeam = None
                    self.stdout.write(self.style.SUCCESS(
                        'Match Stat created: ' + match.team1.name))
                except Exception:
                    traceback.print_exc()
                    self.stdout.write(self.style.WARNING(
                        'Match Stat failed: ' + match.team1.name))
                    firstTeam = None
            else:
                firstTeam = team
        return winners

    def createPlayerStats(self, match, playerTeam, scoreArr):
        try:
            players = Player.objects.filter(team=playerTeam).order_by('?')[:5]

            index = 0
            for player in players:
                try:
                    playerStat = PlayerStat(
                        player=player, match=match, score=scoreArr[index])
                    playerStat.save()
                    index = index+1

                    self.stdout.write(self.style.SUCCESS(
                        'Player Stat created: ' + player.name + ' - ' + playerTeam.name))
                except Exception:
                    traceback.print_exc()
                    self.stdout.write(self.style.WARNING(
                        'Player Stat failed: ' + player.name + ' - ' + playerTeam.name))
        except Exception:
            traceback.print_exc()
            self.stdout.write(self.style.WARNING(
                'Player Stat failed for team: ' + playerTeam.name))

    def handle(self, *args, **kwargs):
        faker = Faker()

        # Create superuser with admin role
        self.superUser(faker)

        # Create team data
        self.createTeamData(faker)

        teams = Team.objects.all()

        # Create coaches
        self.createCoaches(teams, faker)

        # Create players
        self.createPlayers(teams, faker) 

        # Create match stat
        self.createMatchStats(teams)
