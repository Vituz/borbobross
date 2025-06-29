from django import forms
from .models import Deck, Color, Player

class DeckForm(forms.ModelForm):
    class Meta:
        model = Deck
        fields = ['name', 'player', 'image', 'image_type', 'color']
        widgets = {
            # 'name': forms.TextInput(attrs={
            #     'class': 'w-full px-3 py-2 border border-gray-300 rounded focus:outline-none focus:ring focus:border-blue-300',
            #     'placeholder': 'Enter Deck Name',
            #     'required': True,
            # }),
            # 'image': forms.Textarea(attrs={
            #     'class': 'w-full px-3 py-2 border border-gray-300 rounded focus:outline-none focus:ring focus:border-blue-300',
            #     'placeholder': 'Enter base64 string',
            #     'required': True
            # }),
            # 'image_type': forms.TextInput(attrs={
            #     'class': 'w-full px-3 py-2 border border-gray-300 rounded focus:outline-none focus:ring focus:border-blue-300',
            #     'placeholder': 'Enter image type code: es. data:image/webp;base64',
            #     'required': True
            # })
        }

    name = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'w-full px-3 py-2 border border-gray-300 rounded focus:outline-none focus:ring focus:border-blue-300',
            'required': True
        })
    )

    image = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'w-full px-3 py-2 border border-gray-300 rounded focus:outline-none focus:ring focus:border-blue-300',
            'placeholder': 'Enter base64 string',
            'required': True
        })
    )

    image_type = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'w-full px-3 py-2 border border-gray-300 rounded focus:outline-none focus:ring focus:border-blue-300',
            'placeholder': 'Enter image type code: es. data:image/webp;base64',
            'required': True
        })
    )

    player = forms.ModelChoiceField(
        queryset= Player.objects.none(),
        empty_label=None,
        widget=forms.Select(attrs={
            'class': 'w-full px-3 py-2 border border-gray-300 rounded focus:outline-none focus:ring focus:border-blue-300',
            'required': True
        })
    )

    color = forms.ModelMultipleChoiceField(
        queryset= Color.objects.all(),
        widget= forms.SelectMultiple(attrs={
            'class': 'w-full px-3 py-2 border border-gray-300 rounded focus:outline-none focus:ring focus:border-blue-300'
        })
    )

    def __init__(self, *args, **kwargs):
        user_id = kwargs.pop('user_id', None)
        deck_id = kwargs.pop('deck_id', None)

        print(f'FORM USER ID: {user_id}')
        print(f'FORM DECK ID: {deck_id}')

        super().__init__(*args, **kwargs)
        if user_id:
            self.fields['player'].queryset = Player.objects.filter(id = user_id)
            if deck_id:
                try:
                    deck = Deck.objects.get(id = deck_id)
                    self.initial['name'] = deck.name
                    self.initial['color'] = deck.color.all()
                    self.initial['player'] = deck.player
                    self.initial['image'] = deck.image
                    self.initial['image_type'] = deck.image_type
                except Deck.DoesNotExist:
                    print(f'Il Deck con id: {deck_id} non è stato trovato')
        else:
            self.fields['player'].queryset = Player.objects.all()
