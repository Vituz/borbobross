from django.shortcuts import render, redirect
from django.urls import reverse
import json
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import random
from .models import Player, Deck, Color, Match
from .api.methods import get_matches_list
from django.core.serializers.json import DjangoJSONEncoder
from .login_form import CustomLoginForm
from .new_deck_form import DeckForm
from django.contrib.auth import login, authenticate
from django.db.models import Count

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


def login_view(request):
    if request.method == 'POST':
        form = CustomLoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect(reverse('dashboard'))
            else:
                form.add_error(None, 'Invalid username or password.')
    else:
        form = CustomLoginForm(request)
    return render(request, 'home/login.html', {'form': form}) 


def dashboard(request):
    if request.user.is_authenticated:
        decks = []
        try:
            decks = Deck.objects.filter(player = request.user.id)
            print(f'DECKS: {decks}')                

        except Deck.DoesNotExist as e:
            print(f'error: {e}')

        return render(request, 'home/dashboard.html', {
            'decks': decks
        })
    else:
        return redirect(reverse('home-page'))
    

def player_decks_list(request, player_id):
    decks = []
    try:
        decks = Deck.objects.filter(player = player_id)
        player = Player.objects.get(id = player_id)
    except Deck.DoesNotExist as e:
        print(f'error: {e}')
    return render(request, 'home/player_decks.html', {
        'decks': decks,
        'player_username': player.username
    })
    

def add_new_deck(request):
    print(request.user.id)
    if request.user.is_authenticated: 
        if request.method == 'POST':
            print(f'REQUEST POST: TRUE')
            form = DeckForm(request.POST, user_id = request.user.id)
            if form.is_valid():
                deck = form.save(commit=False)
                deck.player = request.user
                deck.save()
                form.save_m2m()
                return redirect(reverse('dashboard'))
            else:
                form.add_error(None, 'Errore nel salvataggio mazzo')
        else:
            print(f'REQUEST POST: FALSE')
            form = DeckForm(user_id = request.user.id)
        return render(request, 'home/new_deck.html', {
            'deck_form': form
        })
    else:
        return redirect(reverse('home-page'))
    

def players_view(request):
    players = Player.objects.all()

    return render(request, 'home/player_view.html', {
        'players': players
    })


def stats_page(request):
    try:
        player_most_wins = Player.objects.all().order_by('-win')[:3]
        player_most_loss = Player.objects.all().order_by('-defeat')[:3]
        deck_most_wins = Deck.objects.all().order_by('-win')[:3]
        deck_most_loss = Deck.objects.all().order_by('-defeat')[:3]
        
        match_per_year = Match.objects.all().values('year').annotate(
            match_count = Count('id')
        ).order_by('-year')

        for deck in deck_most_wins:
            print(f'COLORS: {deck.color.all()}')
            for color in deck.color.all():
                print(f'SINGLE COLOR: {color.name} - {color.image}')
        # print(player_most_wins)
        # print(player_most_loss)

    except Exception as e:
        print(e)
    return render(request, 'home/stats_page.html', {
        'match_per_year': match_per_year,
        'player_most_wins': player_most_wins,
        'player_most_loss': player_most_loss,
        'deck_most_wins': deck_most_wins,
        'deck_most_loss': deck_most_loss
    })