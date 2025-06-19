from django.views.decorators.csrf import csrf_exempt
from ..models import Match
from django.http import JsonResponse
import json
from django.shortcuts import render, redirect
from django.urls import reverse
from datetime import datetime


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
            data = json.loads(request.body)
            print(data)
            return JsonResponse({'message': 'Match salvato con successo'}, status=200)

        except Match.DoesNotExist:
            return JsonResponse({'error': 'Match non trovato.'}, status=404)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Corpo della richiesta JSON non valido.'}, status=400)
        except Exception as e:
            return JsonResponse({'error': f'Si è verificato un errore: {str(e)}'}, status=500)
    else:
        return JsonResponse({'error': 'Metodo non consentito'}, status=405)