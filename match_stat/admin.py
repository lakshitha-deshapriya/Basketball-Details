from django.contrib import admin

from .models import Match, MatchStat, PlayerStat

admin.site.register(Match)
admin.site.register(MatchStat)
admin.site.register(PlayerStat)
