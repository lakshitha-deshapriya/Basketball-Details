from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser

from teams.models import Team

COACH = 'C'
PLAYER = 'P'
ADMIN = 'A'


class UserManager(BaseUserManager):
    def create_user(self, username, email, role, password=None):
        if not username:
            raise ValueError('Users must have an username')

        if not email:
            raise ValueError('Users must have an email address')

        if not role:
            role = PLAYER

        user = self.model(
            email=self.normalize_email(email),
            username=username,
            role=role,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, role, password):
        if not username:
            raise ValueError('Users must have an username')

        if not email:
            raise ValueError('Users must have an email address')

        user = self.create_user(
            username,
            email,
            role=role,
            password=password,
        )
        user.staff = True
        user.admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    roleTypes = [
        (COACH, 'Coach'),
        (PLAYER, 'Player'),
        (ADMIN, 'Admin'),
    ]

    username = models.CharField(max_length=255, unique=True)
    email = models.EmailField(
        verbose_name='email address', max_length=255, unique=True)
    is_active = models.BooleanField(default=True)
    staff = models.BooleanField(default=False)
    admin = models.BooleanField(default=False)

    role = models.CharField(max_length=1, choices=roleTypes, default=ADMIN)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['role', 'email']

    def get_full_name(self):
        return self.username

    def get_short_name(self):
        return self.username

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.staff

    @property
    def is_admin(self):
        return self.role == ADMIN

    @property
    def is_coach(self):
        return self.role == COACH

    @property
    def is_player(self):
        return self.role == PLAYER

    objects = UserManager()


class Coach(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Player(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    height = models.IntegerField()
    age = models.IntegerField()

    def __str__(self):
        return self.name
