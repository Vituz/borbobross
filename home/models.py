from django.db import models
from django.contrib.auth.models import AbstractUser
import re
from django.db import transaction

class Player(AbstractUser):
    image = models.ImageField(upload_to='img/', verbose_name='Player Image')
    win = models.IntegerField(default=0, verbose_name='Win Counter')
    defeat = models.IntegerField(default=0, verbose_name='Defeat Counter')

    def __str__(self):
        return self.username   


class Color(models.Model):
    name = models.CharField(max_length=20, unique=True, verbose_name='Color Name')
    image = models.ImageField(upload_to='img/color/', verbose_name='Color Image')

    def __str__(self):
        return self.name

class Deck(models.Model):
    name = models.CharField(max_length=200, verbose_name='Deck Name')
    player = models.ForeignKey(Player, on_delete=models.CASCADE, blank=True, null=True, related_name='decks', verbose_name='Player')
    image = models.ImageField(upload_to='img/')
    color = models.ManyToManyField('Color', related_name='decks', verbose_name='Deck Colors')
    card_list = models.TextField(blank=True, verbose_name='Card List', help_text="Inserisci la lista delle carte, una per riga, es: '4 Lightning Bolt'")
    cards = models.ManyToManyField('Card', through='DeckCard', related_name='decks')
    win = models.IntegerField(default=0, verbose_name='Win Counter')
    defeat = models.IntegerField(default=0, verbose_name='Defeat Counter')

    def __str__(self):
        return self.name
    
    def update_deck_cards_from_list(self):
        if not self.card_list:
            return
        self.deck_cards.all().delete()

        lines = self.card_list.strip().splitlines()
        card_pattern = re.compile(r'^\s*(\d+)\s+(.+?)\s*$')
        with transaction.atomic():
            for line in lines:
                match = card_pattern.match(line)
                if not match:
                    continue

                quantity, name = int(match.group(1)), match.group(2).strip()

                card, _ = Card.objects.get_or_create(name=name)
                DeckCard.objects.create(deck=self, card=card, quantity=quantity)

class Match(models.Model):
    year = models.CharField(max_length=10, verbose_name='Year')
    winner_player = models.ForeignKey('Player', on_delete=models.SET_NULL, related_name='match_winners', verbose_name='Winner Player', null=True)
    player = models.ManyToManyField('Player', related_name='match_players', verbose_name='Paticipants')
    winner_deck = models.ForeignKey('Deck', on_delete=models.SET_NULL, related_name='matches', verbose_name='Winner Deck', null=True)
    deck = models.ManyToManyField('Deck', related_name='match_deck', verbose_name='Decks')

    def __str__(self):
        return self.date

# class MatchPlayer(models.Model):
#     match = models.ForeignKey('Match', on_delete=models.CASCADE, related_name='match_players', verbose_name='Match Id')
#     player = models.ManyToManyField('Player', related_name='player_matchs', verbose_name='Players')
#     def __str__(self):
#         return self.match

class Card(models.Model):
    name = models.CharField(max_length=200, verbose_name='Card Name')
    mana_cost = models.CharField(max_length=50, blank=True, verbose_name='Mana Cost')
    type_line = models.CharField(max_length=100, blank=True, verbose_name='Type Line')
    text = models.TextField(blank=True, verbose_name='Card Text')
    image = models.ImageField(upload_to='cards/', blank=True, null=True)
    color = models.ManyToManyField('Color', related_name='cards', verbose_name='Card Colors')

    def __str__(self):
        return self.name
    

class DeckCard(models.Model):
    deck = models.ForeignKey('Deck', on_delete=models.CASCADE, related_name='deck_cards')
    card = models.ForeignKey('Card', on_delete=models.CASCADE, related_name='card_decks')
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        unique_together = ('deck', 'card')

    def __str__(self):
        return f'{self.quantity}x {self.card.name} in {self.deck.name}'
    