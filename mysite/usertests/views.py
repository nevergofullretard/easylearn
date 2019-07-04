from datetime import date
from datetime import timedelta
import datetime
from collections import Counter
import random

from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404, reverse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from users.models import Words_user, Units_user
from units.models import Unit_name, Unit_sprache, Unit_schule, Unit_words
from units.views import split_list, unit_exists, schulen_units
# from users.models import Words_user
from usertests.lernweg import LernwegGet, LernwegPost




@login_required
def fehlertest_start(request):
    # fehler_units = []
    # words = Words_user.objects.filter(user=request.user, lernweg_voc=False, right=False)
    # for word in words:
    #     if word.word.unit_name not in fehler_units:
    #         fehler_units.append(word.word.unit_name)

    units_dict = {} #weil sonst die keys als integer bei den links angesehen werden, nicht als strings
    # units = Units_user.objects.filter(user=request.user)

    units_gemacht = []
    for wrd in Words_user.objects.filter(user=request.user, lernweg_voc=False)[::-1]:
        if wrd.word.unit_name not in units_gemacht:
            units_gemacht.append(wrd.word.unit_name)
    units = units_gemacht
    print(units)
    for unit in units:
        units_dict[str(unit.id)] = unit

    today = date.today()
    this_week = today - timedelta(7)
    this_month = today - timedelta(30)
    current_unit = str(request.user.profile.current_unit)
    if current_unit == "0":
        current_unit = None


    if request.method == 'POST':
        print(request.POST)
        date_1 = request.POST.get('date1')
        date_2 = request.POST.get('date2')
        print(date_1)
        print(date_2)
        real_date_1 = datetime.datetime.strptime(date_1, '%m/%d/%Y').strftime('%Y-%m-%d')
        real_date_2 = datetime.datetime.strptime(date_2, '%m/%d/%Y').strftime('%Y-%m-%d')

        # print(Words_user.objects.filter(date=real_date_1)) #funktioniert!
        art = request.POST.get("alle")
        print(art)
        if art == "alle":
            print('alle')
            return HttpResponseRedirect(reverse("test-zwischenschritt", args=['alle', real_date_1, real_date_2, '-']))
        elif art == "falsche":
            return HttpResponseRedirect(reverse("test-zwischenschritt", args=['falsche', real_date_1, real_date_2, '-']))
        elif art == "richtige":
            return HttpResponseRedirect(reverse("test-zwischenschritt", args=['richtige', real_date_1, real_date_2, '-']))
    return render(request, 'usertests/fehlertest-start.html', {'units': units_dict, 'today': str(today), 'this_week': str(this_week),
                                                               'this_month': str(this_month), 'current_unit': current_unit, 'yesterday': today - timedelta(1)} )


@login_required
def fehlertest_zwischenschritt(request, test_art, von, bis, unit_ids):
    user = request.user
    print(user)
    units = []
    units_dict = {}
    if test_art != "alle" and test_art != "falsche" and test_art != "richtige":
        messages.error(request, "Ein Fehler ist aufgetreten. Falsche Anfrage-Art (alle, falsche, richtige)")


    if request.method == 'POST':
        print(request.POST)
        units = request.POST.getlist('units')
        try:
            units_string = str(units[0])
            print(units)
            for unit in units[1:]:
                units_string += '-{}'.format(unit)
            if test_art == "alle":
                return HttpResponseRedirect(reverse('fehlertest-start', args=['alle', von, bis, units_string]))
            elif test_art == "falsche":
                return HttpResponseRedirect(reverse('fehlertest-start', args=['falsche', von, bis, units_string]))
            elif test_art == "richtige":
                return HttpResponseRedirect(reverse('fehlertest-start', args=['richtige', von, bis, units_string]))
        except:
            messages.error(request, "Ein Fehler ist aufgetreten. Du musst mindestens eine Unit auswählen")

    try:
        if test_art == "alle":
            words_unit = Words_user.objects.filter(user=user, date__range=[von, bis], lernweg_voc=False)[::-1]
        elif test_art == "falsche":
            words_unit = Words_user.objects.filter(user=user, date__range=[von, bis], lernweg_voc=False, right=False)[::-1]
        elif test_art == "richtige":
            words_unit = Words_user.objects.filter(user=user, date__range=[von, bis], lernweg_voc=False, right=True)[::-1]

        for word in words_unit:
            if word.word.unit_name not in units:
                units.append(word.word.unit_name)

        if len(units) == 1:
            if test_art == "alle":
                return HttpResponseRedirect(reverse('fehlertest-start', args=['alle', von, bis, str(units[0].id)]))
            elif test_art == "falsche":
                return HttpResponseRedirect(reverse('fehlertest-start', args=['falsche', von, bis, str(units[0].id)]))
            elif test_art == "richtige":
                return HttpResponseRedirect(reverse('fehlertest-start', args=['richtige', von, bis, str(units[0].id)]))
        else:
            for unit in units:
                if test_art == "alle":
                    units_dict[unit] = reversed(Words_user.objects.filter(word__unit_name=unit, user=user, lernweg_voc=False, date__range=[von, bis]))
                elif test_art == "falsche":
                    units_dict[unit] = reversed(Words_user.objects.filter(word__unit_name=unit, user=user, lernweg_voc=False,
                                                                 date__range=[von, bis], right=False))
                elif test_art == "richtige":
                    units_dict[unit] = reversed(Words_user.objects.filter(word__unit_name=unit, user=user, lernweg_voc=False,
                                                                 date__range=[von, bis], right=True))

    except:
        messages.error(request, 'Ein Fehler ist aufgetreten. Bitte versuche es noch mal.')




    return render(request, 'usertests/test-zwischenschritt.html', {'units': units_dict, 'von': datetime.datetime.strptime(von, '%Y-%m-%d').strftime('%d. %b %Y'),
                                                                   'bis':datetime.datetime.strptime(bis, '%Y-%m-%d').strftime('%d. %b %Y'), 'test_art': test_art})

def test_passt(request, test_art, von, bis, unit_ids):
    words_list = []
    words = []
    user = request.user
    if test_art == "alle":
        if von == "0" and bis == "0":
            try:
                int_unit = int(unit_ids)
                unit_gemacht = Units_user.objects.get(user=user, unit__id=int_unit)
                words = Words_user.objects.filter(user=user, word__unit_name=unit_gemacht.unit, lernweg_voc=False)
            except:
                try:    #für jetzige Unit (wo der User jetzt gerade ist)
                    int_unit = int(unit_ids)
                    unit = Unit_name.objects.get(id=int_unit)
                    if int_unit == user.profile.current_unit:
                        words = Words_user.objects.filter(user=user, word__unit_name=unit, lernweg_voc= False)
                    else:
                        messages.error(request, 'Ein Fehler ist aufgetreten.')
                except:
                    messages.error(request, 'Ein Fehler ist aufgetreten.')
        else:
            try:
                for unit in unit_ids.split('-'):
                    unit_real = Unit_name.objects.get(id=int(unit))
                    words_unit = Words_user.objects.filter(user=user, word__unit_name=unit_real, date__range=[von, bis], lernweg_voc=False)
                    for word in words_unit:
                        if word not in words_list:
                            words_list.append(word.id)

                words = Words_user.objects.filter(user=user, id__in=words_list)

            except:
                messages.error(request, 'Ein Fehler ist aufgetreten.')

    elif test_art == "falsche":
        if von == "0" and bis == "0":
            try:
                int_unit = int(unit_ids)
                unit_gemacht = Units_user.objects.get(user=user, unit__id=int_unit)
                words = Words_user.objects.filter(user=user, word__unit_name=unit_gemacht.unit, lernweg_voc=False, right=False)
            except:
                try:    #für jetzige Unit (wo der User jetzt gerade ist)
                    int_unit = int(unit_ids)
                    unit = Unit_name.objects.get(id=int_unit)
                    if int_unit == user.profile.current_unit:
                        words = Words_user.objects.filter(user=user, word__unit_name=unit, lernweg_voc= False, right=False)
                    else:
                        messages.error(request, 'Ein Fehler ist aufgetreten.')
                except:
                    messages.error(request, 'Ein Fehler ist aufgetreten.')
        else:
            try:
                for unit in unit_ids.split('-'):
                    unit_real = Unit_name.objects.get(id=int(unit))
                    words_unit = Words_user.objects.filter(user=user, word__unit_name=unit_real, date__range=[von, bis], lernweg_voc=False, right=False)
                    for word in words_unit:
                        if word not in words:
                            words_list.append(word.id)

                            words = Words_user.objects.filter(user=user, id__in=words_list)
            except:
                messages.error(request, 'Ein Fehler ist aufgetreten.')
    elif test_art == "richtige":
        if von == "0" and bis == "0":
            try:
                int_unit = int(unit_ids)
                unit_gemacht = Units_user.objects.get(user=user, unit__id=int_unit)
                words = Words_user.objects.filter(user=user, word__unit_name=unit_gemacht.unit, lernweg_voc=False, right=True)
            except:
                try:    #für jetzige Unit (wo der User jetzt gerade ist)
                    int_unit = int(unit_ids)
                    unit = Unit_name.objects.get(id=int_unit)
                    if int_unit == user.profile.current_unit:
                        words = Words_user.objects.filter(user=user, word__unit_name=unit, lernweg_voc= False, right=True)
                    else:
                        messages.error(request, 'Ein Fehler ist aufgetreten.')
                except:
                    messages.error(request, 'Ein Fehler ist aufgetreten.')
        else:
            try:
                for unit in unit_ids.split('-'):
                    unit_real = Unit_name.objects.get(id=int(unit))
                    words_unit = Words_user.objects.filter(user=user, word__unit_name=unit_real, date__range=[von, bis], lernweg_voc=False, right=True)
                    for word in words_unit:
                        if word not in words:
                            words_list.append(word.id)

                            words = Words_user.objects.filter(user=user, id__in=words_list)
            except:
                messages.error(request, 'Ein Fehler ist aufgetreten.')
    else:
        messages.error(request, "Ein Fehler ist aufgetreten. Falsche Anfrage-Art (alle, falsche, richige) Versuche es erneut.")

    return words

@login_required
def fehlertest(request, test_art, von, bis, unit_ids):

    words = test_passt(request, test_art, von, bis, unit_ids)



    return render(request, 'usertests/fehlertest-unit.html', {'words': words, 'test_art': test_art, 'von': von, 'bis': bis, 'unit_ids': unit_ids})

@login_required
def fehlertest_karteikarten(request, test_art, von, bis, unit_ids):
    words = test_passt(request, test_art, von, bis, unit_ids)
    pruefung_voc = None
    error = None

    if request.method == "POST":
        lernweg_post = LernwegPost(request, words, save=True)
        words_right_false = lernweg_post.handle_karteikarten()

    else:
        lernweg = LernwegGet(request, words, None, lernweg=True)
        words_right_false = lernweg.mix_karteikarten()


    context = {'words_right_false': words_right_false, 'pruefung_voc': pruefung_voc, 'error': error, 'test_art': test_art, 'von': von, 'bis': bis, 'unit_ids': unit_ids}
    return render(request, 'usertests/test-karteikarten.html', context)

@login_required
def fehlertest_schriftlich(request, test_art, von, bis, unit_ids):
    words = test_passt(request, test_art, von, bis, unit_ids)
    error = None

    if request.method == 'POST':
        lernweg_post = LernwegPost(request, words, save=True)
        words_right_false = lernweg_post.handle_schriftlich()
    else:
        lernweg = LernwegGet(request, words, None, lernweg=True)
        words_right_false = lernweg.mix_schriftlich()



    context = {'words_right_false': words_right_false, 'error': error, 'test_art': test_art, 'von': von, 'bis': bis, 'unit_ids': unit_ids}
    return render(request, 'usertests/test-schriftlich.html', context)

@login_required
def unittest_start(request):
    units = []
    units_gemacht_id = []
    # units_gemacht = Units_user.objects.filter(user=request.user)[::-1]
    # maximum_school = None
    # maximum_language = None
    last_schule = None
    last_sprache = None
    current_unit = None
    if request.user.profile.current_unit != 0:
        current_unit = Unit_name.objects.get(id=request.user.profile.current_unit)

    units_gemacht = []
    for wrd in Words_user.objects.filter(user=request.user, lernweg_voc=False)[::-1]:
        if wrd.word.unit_name not in units_gemacht:
            if wrd.word.unit_name != current_unit:
                units_gemacht.append(wrd.word.unit_name)

    for unit_gemacht in units_gemacht:
        units_gemacht_id.append(unit_gemacht.id)
        units.append(unit_gemacht)

    units_your_school = [u.schule for u in units]
    units_your_language = [s.sprache for s in units]

    units_id = [unit.id for unit in units]
    last_unit = Units_user.objects.filter(user=request.user)[::-1]
    if request.user.profile.current_unit != 0:
        last_schule = Unit_schule.objects.get(id=current_unit.schule.id)
        last_sprache = Unit_sprache.objects.get(id=current_unit.sprache.id)
    else:
        if last_unit:
            last_schule = Unit_schule.objects.get(id=last_unit[0].unit.schule.id)
            last_sprache = Unit_sprache.objects.get(id=last_unit[0].unit.sprache.id)
            print(Unit_name.objects.filter(schule=last_schule, sprache=last_sprache).exclude(id__in=units_id))
        if not Unit_name.objects.filter(schule=last_schule, sprache=last_sprache).exclude(id__in=units_id):
            try:
                units_count = Counter(units_your_school)
                last_schule = max(units_count, key=units_count.get)
                sprache_count = Counter(units_your_language)  # this is a dictionary
                last_sprache = max(sprache_count, key=sprache_count.get)
            except ValueError:  #wenn man noch gar keine Units gemacht hat, soll er das überspringen
                pass
            print(last_schule)
            print(last_sprache)


    similar_units = Unit_name.objects.filter(Q(schule=last_schule, sprache=last_sprache)).exclude(id__in=units_id) #| Q(schule=last_schule) | Q(sprache=last_sprache))

    if similar_units:
        similar_split = split_list(similar_units)
    else:
        similar_split = None

    if units:
        units_split = split_list(units)
    else:
        units_split = None

    andere_units_schule = Unit_name.objects.filter(schule=last_schule).exclude(id__in=units_id)

    if andere_units_schule:
        andere_units_split = split_list(andere_units_schule)
    else:
        andere_units_split = None

    schulen_units_all = schulen_units(Unit_schule.objects.all().exclude(schule=last_schule))

    context = {'current_unit': current_unit, 'units_latest': units_split, 'similar_units': similar_split, 'schulen_units': schulen_units_all, 'andere_units_schule': andere_units_split}
    return render(request, 'usertests/unittest-start.html', context)

@login_required

def unittest_method(request, pk, name_of_unit):
    print(pk)
    print(name_of_unit)
    obj = unit_exists(pk=pk, name_of_unit=name_of_unit)
    users = Words_user.objects.all()
    return render(request, 'usertests/unittest_method.html', {'unit': obj, 'unit_id': obj.id, 'users': users})



def error_message(words_right_false):
    if [key for key in words_right_false.keys()].count('false') > [key for key in words_right_false.keys()].count(
            'right') or \
            [key for key in words_right_false.keys()].count('false') == len(words_right_false) or \
            [key for key in words_right_false.keys()].count('false') > len(words_right_false) * 0.8:
        message = 'yes'  # falls der User zu viel falsch hat, kann das daran liegen, dass er z.B  zwei Unit-Test Tabs offen hat

        return message

@login_required
def unittest_schriftlich(request, pk, name_of_unit, *args):
    message = None
    obj = unit_exists(pk=pk, name_of_unit=name_of_unit)
    words = Unit_words.objects.filter(unit_name=obj)
    if request.method == 'POST':
        lernweg_post = LernwegPost(request, words)
        words_right_false = lernweg_post.handle_schriftlich()
    else:
        lernweg = LernwegGet(request, words)
        words_right_false = lernweg.mix_schriftlich()


    context = {'unit': obj, 'message': message, 'words_right_false': words_right_false}
    return render(request, 'usertests/unittest_schriftlich.html', context)

@login_required
def unittest_karteikarten(request, pk, name_of_unit, *args, **kwargs):
    message = None
    obj = unit_exists(pk, name_of_unit)
    words = Unit_words.objects.filter(unit_name=obj)

    if request.method == 'POST':
        lernweg_post = LernwegPost(request, words)
        words_right_false = lernweg_post.handle_karteikarten()

    else:
        lernweg = LernwegGet(request, words)
        words_right_false = lernweg.mix_karteikarten()

    messages.error(request, 'Aufgepasst: Du musst eine der 4 Optionen auswählen')

    context = {'unit': obj, 'message': message, 'words_right_false': words_right_false}
    return render(request, 'usertests/unittest_karteikarten.html', context)