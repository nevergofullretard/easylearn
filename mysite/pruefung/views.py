from django.shortcuts import render, HttpResponse



def fehlertest(request):
    return HttpResponse('worked!')
