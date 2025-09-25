from django.contrib import admin

from .models import Comment, Favorite, Player, Team

admin.site.register(Player)
admin.site.register(Team)
admin.site.register(Comment)
admin.site.register(Favorite)
