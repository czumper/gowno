from django.shortcuts import render

def home(request):
    context = {
        'description': 'Siemanko na stronie Pitcerni.',
        'pizze': [
            {'nazwa': 'Margarita', 'image': 'margarita.jpg'},
            {'nazwa': 'Salami', 'image': 'salami.jpg'},
            {'nazwa': '4 sery', 'image': '4sery.jpg'},
        ]
    }
    return render(request, 'home/home.html', context)

from rest_framework.response import Response
from rest_framework.decorators import api_view

@api_view(['GET'])
def example_view(request):
    return Response({"message": "Hello from Django API!"})
