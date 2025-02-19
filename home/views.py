from django.shortcuts import render
from django.core.mail import send_mail
from django.http import HttpResponse
# Create your views here.

def home(request):
    return render(request, 'home/index.html')

def test_maila(request):
    send_mail(
        'SIEMA',
        'TESTOWY MAIL',
        'czumpi@pitcernia.ninja',
        ['kfranek44@gmail.com'],
        fail_silently=False,
    )
    return HttpResponse('MAIL WYSLANY')