from django.shortcuts import render, redirect
from django.urls import reverse
import json
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import random
from .models import Player, Deck
from .api.methods import get_matches_list
from django.core.serializers.json import DjangoJSONEncoder

# Create your views here.

def home_page(request):
    return render(request, 'home/home.html')


def table_generator(request):
    return render(request, 'home/table_generator.html')

def matches(request):
    
    all_player = Player.objects.all().order_by('username')
    all_deck = Deck.objects.all()
    for deck in all_deck:
        print(f'Deck name: {deck.name} - Player: {deck.player}')
    
    player_data_list = [{'id': p.id, 'username': p.username} for p in all_player]
    deck_data_list = [{'name': d.name, 'player': d.player.username} for d in all_deck]

    matches_list = get_matches_list()
    # matches_list = {
    #     '2025': [
    #         {
    #             'match_id': '1',
    #             'winner': 'Vito',
    #             'winner_deck': 'Deck Name',
    #             'deck_img': 'https://readdy.ai/api/search-image?query=fantasy%20art%20of%20a%20lush%20green%20forest%20with%20majestic%20elves%20and%20mystical%20creatures%2C%20epic%20scene%20with%20magical%20atmosphere%2C%20digital%20art&width=400&height=150&seq=1&orientation=landscape',
    #             'participants': [
    #                 {
    #                     'name': 'Player Name',
    #                     'deck': 'Deck Name'
    #                 },
    #                 {
    #                     'name': 'Player Name',
    #                     'deck': 'Deck Name'
    #                 },
    #                 {
    #                     'name': 'Player Name',
    #                     'deck': 'Deck Name'
    #                 },
    #             ],
    #         },
    #         {
    #             'match_id': '2',       
    #             'winner': 'Player Name',
    #             'winner_deck': 'Deck Name',
    #             'deck_img': 'https://readdy.ai/api/search-image?query=fantasy%20art%20of%20a%20lush%20green%20forest%20with%20majestic%20elves%20and%20mystical%20creatures%2C%20epic%20scene%20with%20magical%20atmosphere%2C%20digital%20art&width=400&height=150&seq=1&orientation=landscape',
    #             'participants': [
    #                 {
    #                     'name': 'Player Name',
    #                     'deck': 'Deck Name'
    #                 },
    #             ],
    #         },
    #         {
    #             'match_id': '3',
    #             'winner': 'Player Name',
    #             'winner_deck': 'Deck Name',
    #             'deck_img': 'https://readdy.ai/api/search-image?query=fantasy%20art%20of%20a%20lush%20green%20forest%20with%20majestic%20elves%20and%20mystical%20creatures%2C%20epic%20scene%20with%20magical%20atmosphere%2C%20digital%20art&width=400&height=150&seq=1&orientation=landscape',
    #             'participants': [
    #                 {
    #                     'name': 'Player Name',
    #                     'deck': 'Deck Name'
    #                 },
    #             ],
    #         },
    #         {
    #             'match_id': '4',       
    #             'winner': 'Player Name',
    #             'winner_deck': 'Deck Name',
    #             'deck_img': 'https://readdy.ai/api/search-image?query=fantasy%20art%20of%20a%20lush%20green%20forest%20with%20majestic%20elves%20and%20mystical%20creatures%2C%20epic%20scene%20with%20magical%20atmosphere%2C%20digital%20art&width=400&height=150&seq=1&orientation=landscape',
    #             'participants': [
    #                 {
    #                     'name': 'Player Name',
    #                     'deck': 'Deck Name'
    #                 },
    #             ],
    #         },
    #     ],
    #     '2024': [
    #         {
    #             'match_id': '1',        
    #             'winner': 'Vito',
    #             'winner_deck': 'Deck Name',
    #             'deck_img': 'https://readdy.ai/api/search-image?query=fantasy%20art%20of%20a%20lush%20green%20forest%20with%20majestic%20elves%20and%20mystical%20creatures%2C%20epic%20scene%20with%20magical%20atmosphere%2C%20digital%20art&width=400&height=150&seq=1&orientation=landscape',
    #             'participants': [
    #                 {
    #                     'name': 'Player Name',
    #                     'deck': 'Deck Name'
    #                 },
    #                 {
    #                     'name': 'Player Name',
    #                     'deck': 'Deck Name'
    #                 },
    #             ],
    #         },
    #         {
    #             'match_id': '2',       
    #             'winner': 'Player Name',
    #             'winner_deck': 'Deck Name',
    #             'deck_img': 'https://readdy.ai/api/search-image?query=fantasy%20art%20of%20a%20lush%20green%20forest%20with%20majestic%20elves%20and%20mystical%20creatures%2C%20epic%20scene%20with%20magical%20atmosphere%2C%20digital%20art&width=400&height=150&seq=1&orientation=landscape',
    #             'participants': [
    #                 {
    #                     'name': 'Player Name',
    #                     'deck': 'Deck Name'
    #                 },
    #             ],
    #         },
    #         {
    #             'match_id': '3',        
    #             'winner': 'Player Name',
    #             'winner_deck': 'Deck Name',
    #             'deck_img': 'https://readdy.ai/api/search-image?query=fantasy%20art%20of%20a%20lush%20green%20forest%20with%20majestic%20elves%20and%20mystical%20creatures%2C%20epic%20scene%20with%20magical%20atmosphere%2C%20digital%20art&width=400&height=150&seq=1&orientation=landscape',
    #             'participants': [
    #                 {
    #                     'name': 'Player Name',
    #                     'deck': 'Deck Name'
    #                 },
    #             ],
    #         },
    #     ],
    # }

    context = {
        'matches_list': matches_list,
        'all_player_data_json': player_data_list,
        'all_decks': json.dumps(deck_data_list)
    }
    return render(request, 'home/matches.html', context)


@csrf_exempt
def generate_tables(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            players = data.get('player_list')
            num_tables = data.get('table_numbers')

            print(f'Tables: {num_tables} - Players: {players}')

            # Raccoglie i nomi
            # names = [request.form.get(f'name_{i}').strip() for i in range(num_players)]
            # names = [name for name in names if name]  # Rimuove vuoti
            random.shuffle(players)

            # Assegna ai tavoli
            tavoli = [[] for _ in range(num_tables)]
            for i, name in enumerate(players):
                tavoli[i % num_tables].append(name.title())

            print(tavoli)

            response_data = {
                'success': True,
                'tables': tavoli,
            }

            return JsonResponse(response_data)
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=400)
    else:
        return JsonResponse({'success': False, 'error': 'Metodo non supportato'}, status=405)
    


def counter(request):
    return render(request, 'home/counter_page.html')