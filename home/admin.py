from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin

class PlayerAdmin(admin.ModelAdmin):
    list_display = ('username',)

class ColorAdmin(admin.ModelAdmin):
    list_display = ('name',)

class DeckAdmin(admin.ModelAdmin):
    list_display = ('name', 'player')

class MatchAdmin(admin.ModelAdmin):
    list_display = ('year', 'winner_player', 'winner_deck')

class CardAdmin(admin.ModelAdmin):
    list_display = ('name',)

# Register your models here.
admin.site.register(Player, PlayerAdmin)
admin.site.register(Color, ColorAdmin)
admin.site.register(Deck, DeckAdmin)
admin.site.register(Match, MatchAdmin)
admin.site.register(Card, CardAdmin)
