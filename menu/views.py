from django.shortcuts import render

def menu(request):
    context = {
        'pizzas': [
            {'nazwa': 'Margarita', 'cena': '25 zł'},
            {'nazwa': 'Salami', 'cena': '28 zł'},
            {'nazwa': '4 Sery', 'cena': '30 zł'},
        ]
    }
    return render(request, 'menu/menu.html', context)


