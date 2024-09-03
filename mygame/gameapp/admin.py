from django.contrib import admin
from .models import Player, Boost, Level, Prize, PlayerLevel, LevelPrize

admin.site.register(Player)
admin.site.register(Boost)
admin.site.register(Level)
admin.site.register(Prize)
admin.site.register(PlayerLevel)
admin.site.register(LevelPrize)