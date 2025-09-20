from django.contrib import admin

from .models import Comment, Favorite, Player, Sport, Team

admin.site.register(Player)
admin.site.register(Sport)
admin.site.register(Team)
admin.site.register(Comment)
admin.site.register(Favorite)
