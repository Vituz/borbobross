from django.views.decorators.csrf import csrf_exempt
from ..models import Match, Player, Deck
from django.http import JsonResponse
import json
from django.shortcuts import render, redirect
from django.urls import reverse
from datetime import date
from django.db.models import Count

def delete_match(request):
    if request.method == 'DELETE':
        try:
            data = json.loads(request.body)

            match = Match.objects.get(id = data.get('id'))
            match.delete()
            return JsonResponse({'message':'Match eliminato con successo'}, status= 200)
        except Match.DoesNotExist:
            return JsonResponse({'error': 'Match non trovato.'}, status=404)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Corpo della richiesta JSON non valido.'}, status=400)
        except Exception as e:
            return JsonResponse({'error': f'Si è verificato un errore: {str(e)}'}, status=500)
    else:
        return JsonResponse({'error': 'Metodo non consentito'}, status=405)
            

# current_year = datetime.now().year

def save_match(request):
    if request.method == 'POST':
        try:
            year = str(date.today().year)
            print(year)
            data = json.loads(request.body)
            new_match = Match()
            print(data)
            winner_player = data.get('winner_name').title()
            winner_deck = data.get('winner_deck').title()
            participants = data.get('participants')
            print(f'Winner: {winner_player} - Deck: {winner_deck}')

            new_match.year = str(year)
            try:
                player = Player.objects.get(username = winner_player)
                print(f'Player: {player}')

                deck = Deck.objects.get(name__iexact = winner_deck)
                print(f'Deck: {deck}')

                player.win += 1
                deck.win += 1
                new_match.winner_player = player
                new_match.winner_deck = deck
                new_match.save()
                print(participants)
                for pl in participants:
                    print(f'PL: {pl}')
                    try:
                        print(f'Participants Player: {pl.get('playerName')}')
                        print(f'Participants Deck: {pl.get('deckName')}')
                        p = Player.objects.get(username__iexact = pl.get('playerName'))
                        new_match.player.add(p)
                        p.defeat += 1

                        d = Deck.objects.get(name__iexact = pl.get('deckName'))
                        new_match.deck.add(d)
                        d.defeat += 1
                    except Exception as e:
                        return JsonResponse({'error': f'Si è verificato un errore: {str(e)}'}, status=500)
                    
            except Exception as e:
                return JsonResponse({'error': f'Si è verificato un errore: {str(e)}'}, status=500)
                

            return JsonResponse({'message': 'Match salvato con successo'}, status=200)

        except Match.DoesNotExist:
            return JsonResponse({'error': 'Match non trovato.'}, status=404)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Corpo della richiesta JSON non valido.'}, status=400)
        except Exception as e:
            return JsonResponse({'error': f'Si è verificato un errore: {str(e)}'}, status=500)
    else:
        return JsonResponse({'error': 'Metodo non consentito'}, status=405)
    



def get_matches_list():
    matches_list = {}

    try:
        query_list = Match.objects.all()
        
        for year in query_list:
            if year.year not in matches_list:
                matches_list[str(year.year)] = []

        # print(f'MATCHES LIST: {matches_list}')
        # print(f'GET MATCHES LIST: {query_list}')
        
        for match in query_list:
            participants = []
            # print(f'Player: {match.player.all()}')
            # print(f'Deck: {match.deck.all()}')

            query_deck = match.deck.all()

            for deck in query_deck:
                participants.append({'name': deck.player.username, 'deck': deck.name})

            match_data = {
                'match_id': str(match.id),
                'winner': match.winner_player.username,
                'winner_deck': match.winner_deck.name,
                'deck_img': match.winner_deck.image,
                'deck_img_type': match.winner_deck.image_type,
                'participants': participants
            }
            # print(f'MATCH DATA: {match_data}')
            
            
            matches_list[str(match.year)].append(match_data)
           
            # print(f'MATCH: {match.winner_player}')

        print(f'MATCHES LIST: {matches_list}')
    except KeyError as e:
        print(f'error: {str(e)}')
    
    return matches_list