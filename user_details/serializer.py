from rest_framework import serializers

from .models import User, Coach, Player

from teams.serializer import TeamSerializer


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'role']


class CoachSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coach
        fields = ['id', 'user', 'name', 'team']

    def to_representation(self, instance):
        self.fields['user'] = UserSerializer(read_only=True)
        self.fields['team'] = TeamSerializer(read_only=True)
        return super(CoachSerializer, self).to_representation(instance)
    
class PlayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = ['id', 'user', 'name', 'team', 'height', 'age']

    def to_representation(self, instance):
        self.fields['user'] = UserSerializer(read_only=True)
        self.fields['team'] = TeamSerializer(read_only=True)
        return super(PlayerSerializer, self).to_representation(instance)
