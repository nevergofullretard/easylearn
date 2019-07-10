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
    add_unit = f'http://{request.META["HTTP_HOST"]}/media/pictures/add_unit.PNG'
    all_units = f'http://{request.META["HTTP_HOST"]}/media/pictures/all_units.PNG'
    gelernte_woerter = f'http://{request.META["HTTP_HOST"]}/media/pictures/gelernte_woerter.PNG'
    profile = f'http://{request.META["HTTP_HOST"]}/media/pictures/profile.PNG'
    suche = f'http://{request.META["HTTP_HOST"]}/media/pictures/suche.PNG'
    lernweg = f'http://{request.META["HTTP_HOST"]}/media/pictures/lernweg.PNG'
    statistic = f'http://{request.META["HTTP_HOST"]}/media/pictures/statistics2.png'
    context = {'pic_me': pic_me, 'github': my_logo, 'github2': github2, 'stat': stat, 'suche': suche, 'profile': profile,
               'gelernte_woerter': gelernte_woerter, 'all_units': all_units, 'add_unit': add_unit, 'lernweg': lernweg,
               'statistic': statistic}
    return render(request, 'about/home.html', context)