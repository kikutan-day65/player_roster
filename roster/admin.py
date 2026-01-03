from django.contrib import admin

from .models import Comment, Player, Team

admin.site.register(Player)
admin.site.register(Team)
admin.site.register(Comment)
