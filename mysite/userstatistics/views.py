from datetime import date, timedelta

from django.contrib import messages

from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.decorators import method_decorator
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from django.views.generic import View
from rest_framework.views import APIView
from rest_framework.response import Response

from users.models import Words_user, Units_user
from units.models import Unit_name, Unit_words
from blog.models import Post
from units.views import split_list, unit_exists

# def split_list(a_list):
#     half = len(a_list) // 2
#     if half == 0:
#         print(a_list)
#         return zip(a_list, [' '])
#     return zip(a_list[:half], a_list[half:])



@login_required
def user_statistics(request):
    if request.user.profile.current_unit2:
        current_unit = request.user.profile.current_unit2
    else:
        current_unit = 0
    # units_gemacht_all = Units_user.objects.filter(user=request.user)[::-1]
    units_gemacht_all = []
    for wrd in Words_user.objects.filter(user=request.user, lernweg_voc=False)[::-1]:
        if wrd.word.unit_name not in units_gemacht_all:
            units_gemacht_all.append(wrd.word.unit_name)

    print(units_gemacht_all)
    #request.user.profile.units_gemacht.all()[::-1]
    # units_gemacht_name = []
    #
    # for unit in units_gemacht_all:
    #     units_gemacht_name.append(unit)
    # units_gemacht = units_gemacht_name[0:4]
    #
    # print(units_gemacht)
    # units_gemacht_list = [unit_gemacht.u_name for unit_gemacht in units_gemacht]
    # print(units_gemacht_list)
    # units_all = Unit_name.objects.all().count()


    posts_user = Post.objects.filter(author=request.user)
    if posts_user:
        posts = ['zum Community-Profil']
        posts.extend(posts_user.order_by('-date_posted'))
    else:
        posts = None
    # print(units_gemacht)
    context = {'units_all': units_all, 'current_unit': current_unit, 'units_gemacht': units_gemacht_all, 'posts': posts}

    return render(request, 'userstatistics/statistics-start.html', context)

@login_required
def units_all(request):
    # units = Units_user.objects.filter(user=request.user)[::-1]
    units = []
    for wrd in Words_user.objects.filter(user=request.user, lernweg_voc=False)[::-1]:
        if wrd.word.unit_name not in units:
            units.append(wrd.word.unit_name)
    print(units)
    # units_names = []
    # for unit in units:
    #     units_names.append(unit.unit)

    # print(split_list(units_names))
    context = {'units_all': units}
    return render(request, 'userstatistics/units-all.html', context)



class GetData(View):
    @method_decorator(staff_member_required)

    def get_data(self, request, *args, **kwargs):
        data = {
            'sales': 100,
            'costumers': 10,
        }
        return JsonResponse(data)



class ChartData1(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]


    def get(self, request, format=None):
        words_right = Words_user.objects.filter(user=self.request.user, lernweg_voc=False, right=True)
        words_false = Words_user.objects.filter(user=self.request.user, lernweg_voc=False, right=False)

        right_list = [wrd_r.word.italienisch for wrd_r in words_right]
        false_list = [wrd_f.word.italienisch for wrd_f in words_false]

        right_id_list = [wrd_r.word.id for wrd_r in words_right]
        false_id_list =[wrd_f.word.id for wrd_f in words_false]

        labels = ["Richtig", "Falsch"]
        default = [len(words_right), len(words_false)]
        data = {
            'labels': labels,
            'default': default,
            'right': right_list,
            'false': false_list,
            'right-id': right_id_list,
            'false-id': false_id_list,
        }
        return Response(data)




class ChartData3(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]


    def get(self, request, format=None):
        print(date.today)
        words_today_right = Words_user.objects.filter(user=self.request.user, lernweg_voc=False, right=True, date=date.today()) #das wird nur in userer Zeitzone gelten
        words_today_false = Words_user.objects.filter(user=self.request.user, lernweg_voc=False, right=False, date=date.today())

        labels = ["Richtig", "Falsch"]
        default = [len(words_today_right), len(words_today_false)]
        data = {
            'labels': labels,
            'default': default,
        }
        return Response(data)

class ChartData4(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        today = date.today()
        range_days = []
        words_week_right = []
        words_week_false = []
        i = 0
        while i < 7:
            range_days.append(today - timedelta(i))
            i += 1


        for day in range_days:
            words_right = Words_user.objects.filter(user=self.request.user, lernweg_voc=False,
                                                      right=True,date=day)
            words_false = Words_user.objects.filter(user=self.request.user, lernweg_voc=False,
                                                      right=False, date=day)
            for wrd_right in words_right:
                words_week_right.append(wrd_right)
            for wrd_false in words_false:
                words_week_false.append(wrd_false)


        labels = ["Richtig", "Falsch"]
        default = [len(words_week_right), len(words_week_false)]
        data = {
            'labels': labels,
            'default': default,
        }
        return Response(data)


class ChartData5(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]


    def get(self, request, format=None):
        print(date.today)
        words_unit_right = Words_user.objects.filter(user=self.request.user, word__unit_name=request.user.profile.current_unit2, lernweg_voc=False, right=True, date=date.today()) #das wird nur in userer Zeitzone gelten
        words_unit_false = Words_user.objects.filter(user=self.request.user, word__unit_name=request.user.profile.current_unit2, lernweg_voc=False, right=False, date=date.today())

        labels = ["Richtig", "Falsch"]
        default = [len(words_unit_right), len(words_unit_false)]
        data = {
            'labels': labels,
            'default': default,
        }
        return Response(data)

@login_required
def statistics_unit(request, pk, name_of_unit):
    obj = unit_exists(pk, name_of_unit, request.user)
    # for name in Unit_name.objects.all():
    #     if str(name_of_unit) == str(name):
    #         obj2 = get_object_or_404(Units_user.objects.filter(user=request.user), unit__id=name.id)
    #         obj = get_object_or_404(Unit_name, id=obj2.unit.id)
    words_unit = Words_user.objects.filter(user=request.user, word__unit_name=obj, lernweg_voc=False).order_by("-date")
    outstanding_words = []

    all_words_unit = Unit_words.objects.filter(unit_name=obj)

    for wrd in all_words_unit:
        if wrd not in [wrd.word for wrd in words_unit]:
            outstanding_words.append(wrd)

    current_unit = ""
    if request.user.profile.current_unit2:
        current_unit = request.user.profile.current_unit2

    context = {'name_of_unit': obj, 'pk': obj.id, 'words': words_unit, 'all_words': all_words_unit, 'outstanding_words': outstanding_words, 'current_unit': current_unit}
    return render(request, 'userstatistics/units-start.html', context)


class ChartData6(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, pk, name_of_unit, format=None):
        obj = unit_exists(pk, name_of_unit, request.user)


        words_unit_right = Words_user.objects.filter(user=self.request.user, word__unit_name=obj, lernweg_voc=False, right=True) #das wird nur in userer Zeitzone gelten
        words_unit_false = Words_user.objects.filter(user=self.request.user, word__unit_name=obj, lernweg_voc=False, right=False)

        labels = ["Richtig", "Falsch"]
        default = [len(words_unit_right), len(words_unit_false)]
        data = {
            'labels': labels,
            'default': default,
        }
        return Response(data)

@login_required
def delete_unit(request, pk, name_of_unit):
    obj = unit_exists(pk, name_of_unit, request.user)
    if request.method == 'POST':
        words = Words_user.objects.filter(user=request.user, word__unit_name=obj)
        # units = Units_user.objects.filter(user=request.user, unit=obj.unit)
        print(words)
        if request.user.profile.current_unit2:
            current_unit = request.user.profile.current_unit2

            if obj == current_unit:
                profile = request.user.profile
                profile.current_unit = 0
                profile.current_unit2 = None
                profile.save()
        if words:
            for word in words:
                word.delete()

        messages.success(request, f'Die Unit {obj} mitsamt Lernfortschritt wurde gelöscht!')
        return redirect('statistics_units_all')

    else:
        pass
    return render(request, 'userstatistics/delete-unit.html', {'unit': obj})
