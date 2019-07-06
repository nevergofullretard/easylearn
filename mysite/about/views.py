from django.shortcuts import render
from django.http import HttpResponse

# C:\Users\maxij\OneDrive - BHAK Schaerding\github\easylearn\mysite\media\pictures

def about(request):
    pic_me = f'http://{request.META["HTTP_HOST"]}/media/pictures/me.png'
    my_logo = f'http://{request.META["HTTP_HOST"]}/media/pictures/github-scientist.png'
    # github_logo = f'http://{request.META["HTTP_HOST"]}/media/pictures/me.png'
    # my_logo = f'http://{request.META["HTTP_HOST"]}/media/pictures/me.png'
    # my_logo = f'http://{request.META["HTTP_HOST"]}/media/pictures/me.png'
    github2 = f'http://{request.META["HTTP_HOST"]}/media/pictures/github2.jpg'
    stat = f'http://{request.META["HTTP_HOST"]}/media/pictures/statistics2.png'

    context = {'pic_me': pic_me, 'github': my_logo, 'github2': github2, 'stat': stat}
    return render(request, 'about/home.html', context)