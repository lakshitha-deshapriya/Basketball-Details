from django.test import TestCase
from .models import Team


class TeamTestCase(TestCase):

    def setUp(self):
        print('')
        print('Team data setUp started...')
        Team.objects.create(name='test_team',owner='test_owner')
        print('Team data setUp finished...')

    def test_user(self):
        print('Team model test started...')
        team = Team.objects.filter(name='test_team').first()

        self.assertNotEqual(team, None, 'Team creation test failed')
        
        team.name = 'test_team2'
        team.save()
        team = Team.objects.filter(name='test_team2').first()
        
        self.assertNotEqual(team, None, 'Team update test failed')

        team.delete()
        teamDel = Team.objects.filter(name='test_team').first()

        self.assertEqual(teamDel, None, 'Team delete test failed')

        print('Team model test finished...')
