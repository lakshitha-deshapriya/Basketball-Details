from django.test import TestCase
from .models import User


class UserTestCase(TestCase):
    adminDetails = ['test_admin_user', 'test_admin@test.com']
    coachDetails = ['test_coach', 'coach@test.com']
    playerDetails = ['test_player', 'player@test.com']

    def setUp(self):
        print('')
        print('User data setUp started...')
        User.objects.create_user(
            username=self.adminDetails[0], email=self.adminDetails[1], role='A', password='admin')
        User.objects.create_user(
            username=self.coachDetails[0], email=self.coachDetails[1], role='C', password='coach')
        User.objects.create_user(
            username=self.playerDetails[0], email=self.playerDetails[1], role='P', password='player')
        print('User data setUp finished...')

    def test_user(self):
        print('User model test started...')
        adminUser = User.objects.filter(
            username=self.adminDetails[0]).first()
        coachUser = User.objects.filter(
            username=self.coachDetails[0]).first()
        playerUser = User.objects.filter(
            username=self.playerDetails[0]).first()

        self.assertEqual(adminUser.role, 'A', 'Admin user test failed')
        self.assertEqual(coachUser.role, 'C', 'Coach user test failed')
        self.assertEqual(playerUser.role, 'P', 'Player user test failed')

        adminUser.delete()
        coachUser.delete()
        playerUser.delete()

        adminUserDel = User.objects.filter(
            username=self.adminDetails[0]).first()
        coachUserDel = User.objects.filter(
            username=self.coachDetails[0]).first()
        playerUserDel = User.objects.filter(
            username=self.playerDetails[0]).first()

        self.assertEqual(adminUserDel, None, 'Admin user test delete failed')
        self.assertEqual(coachUserDel, None, 'Coach user test delete failed')
        self.assertEqual(playerUserDel, None, 'Player user test delete failed')

        print('User model test finished...')
