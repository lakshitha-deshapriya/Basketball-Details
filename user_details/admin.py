from django.contrib import admin

from .models import User,Coach, Player

admin.site.register(User)
admin.site.register(Coach)
admin.site.register(Player)
