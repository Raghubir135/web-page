from django.shortcuts import render
from django.http import HttpResponse


# Create your views here.

def ticketmaster(request):
    context = {'name': 'John'}
    return render(request, 'ticketmaster.html', context)
