from django_unicorn.components import UnicornView
from models import Player, Deck, Match
from datetime import date

class CreateNewMatchView(UnicornView):
    year = ''
    # winner_player_id: int = None
    # winner_deck_id: int =  None
    # participants: list = [{'player_id': None, 'deck_id': None}]

    # def get_player(self):
    #     return Player.objects.all()

    # def get_deck_for_player(self, player_id):
    #     if player_id:
    #         return Deck.objects.filter(player_id = player_id)
    #     return Deck.objects.none()
    
    # def get_winner_deck(self):
    #     if self.winner_player_id:
    #         return Deck.objects.filter(player_id=self.winner_deck_id)
    #     return Deck.objects.none()

    # def add_participants(self):
    #     self.participants.append({'player_id':None, 'deck_id':None})

    # def remove_participant(self, index):
    #     if len(self.participants) > 1:
    #         self.participants.pop(index)

    # def save(self):
    #     valid_participants = []
    #     for i, p in enumerate(self.participants):
    #         pid = p.get('player_id')
    #         did = p.get('deck_id')
    #         if not pid or not did:
    #             self.add_error(f'participants.{i}.player_id', 'Giocatore non trovato')
    #             return 
    #         if not Player.objects.filter(id=pid).exists():
    #             self.add_error(f'participants.{i}.player_id', 'Giocatore non trovato')
    #             return
    #         if not Deck.objects.filter(id=did, player_id=pid).exists():
    #             self.add_error(f'participants.{i}.deck_id', 'Mazzo non valido per il giocatore selezionato')
    #             return
    #         valid_participants.append((pid, did))

    #     match = Match.objects.create(
    #         year = date.today().year,
    #         winner_player_id = self.winner_player_id,
    #         winner_deck_id = self.winner_player_id
    #     )

    #     match.player.set([pid for pid, _ in valid_participants])
    #     match.deck.set([did for _, did in valid_participants])

    #     if self.winner_player_id:
    #         winner = Player.objects.get(id = self.winner_player_id)
    #         winner.win += 1
    #         winner.save()
    #     if self.winner_deck_id:
    #         winner_deck = Deck.objects.get(id = self.winner_deck_id)
    #         winner_deck.win += 1
    #         winner_deck.save()

    #     for pid, did in valid_participants:
    #         if pid != self.winner_player_id:
    #             player = Player.objects.get(id = pid)
    #             player.defeat += 1
    #             player.save()
    #         if did != self.winner_deck_id:
    #             deck = Deck.objects.get(id = self.did)
    #             deck.defeat += 1
    #             deck.save()

    #     self.reset()

