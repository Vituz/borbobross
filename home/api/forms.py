# from django import forms
# from home.models import *

# class AddMatchForm(forms.ModelForm):
#     class Meta:
#         model = Match
#         fields = ['winner_player', 'winner_deck', 'player', 'deck']
    
#     winner_player = forms.ModelChoiceField(
#         queryset= Player.objects.all(),
#         empty_label='Select Player',
#         widget= forms.Select(attrs={
#             'class': 'w-full px-4 py-2 border border-gray-300 rounded-sm focus:outline-none focus:ring-2 focus:ring-primary focus:border-primary',
#             'id': 'winnerName'
#         })
#     )

#     winner_deck = forms.ModelChoiceField(
#         queryset= Deck.objects.filter(player = winner_player
#     )

    