from datetime import date
from collections import Counter
import random

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from users.models import Words_user, Units_user
from units.models import Unit_name, Unit_sprache, Unit_schule, Unit_words
# from users.models import Words_user


def split_list(a_list):
    half = int(len(a_list) // 2)
    if half == 0:
        return zip(a_list, [' '])

    first_half = a_list[:half]
    second_half = a_list[half:]
    if len(first_half) < len(second_half):
        first_half.append(' ')
    else:
        pass
    return zip(first_half, second_half)



@login_required
def fehlertest(request):
    words = Words_user.objects.filter(user=request.user, fuer_pruefung=True, lernweg_voc=False, right=False)[0: request.user.profile.voc_bits]

    context = {'words': words}
    return render(request, 'usertests/fehlertest-start.html', context)

@login_required
def fehlertest_karteikarten(request):
    words = []
    pruefung_voc = None
    error = None

    if request.method == 'POST':
        values_from_user = request.POST.getlist('choices')[0]
        try:
            word_for_user = Words_user.objects.filter(user=request.user, fehlertest=True)[0]
        except IndexError:
            return redirect('fehlertest-start')

        if str(values_from_user) == str(word_for_user.word.italienisch):
            word_for_user.right = True
            word_for_user.fehlertest = False
            word_for_user.save()

        else:
            word_for_user.right = False
            word_for_user.fehlertest = False
            word_for_user.save()
        words.append(word_for_user)

    else:
        try:
            words_alle = Words_user.objects.filter(user=request.user, fuer_pruefung=True, lernweg_voc=False, right=False)[
                    0: request.user.profile.voc_bits]

            for word in words_alle:
                word.fehlertest = False
                word.save()

            pruefung_voc = random.choice(words_alle)
            pruefung_voc.fehlertest = True
            pruefung_voc.save()

            x = 0
            x_error = 0
            while x < 3:
                word_unit = random.choice(words_alle)
                words.append(word_unit)
                if words.count(word_unit) > 1 or word_unit == pruefung_voc:
                    words.remove(word_unit)
                    x -= 1
                x += 1
                x_error += 1
                if x_error > 30:
                    break

            reihung_pruefung_voc = random.choice([0, 1, 2, 3])
            words.insert(reihung_pruefung_voc, pruefung_voc)

        except IndexError:
            error = 'Es scheint als hättest du keine Fehler gemacht'


    context = {'words': words, 'pruefung_voc': pruefung_voc, 'error': error}
    return render(request, 'usertests/fehlertest-karteikarten.html', context)

@login_required
def fehlertest_schriftlich(request):
    words = []
    error = None
    if request.method == 'POST':
        values_from_user = request.POST.getlist('my_list') # was der user im template in <input> eingegeben hat
        words_for_user = Words_user.objects.filter(user=request.user, fehlertest=True)

        words_for_user_gereiht = []
        x = 1
        for wrd in words_for_user:
            word = Words_user.objects.get(user=request.user, fehlertest=True,  pruefung_reihung=x)
            words_for_user_gereiht.append(word)
            x += 1

        for wrd_user, wrd_data in zip(values_from_user, words_for_user_gereiht):
            wrd_data.date = date.today()

            print(str(wrd_data) +  '   ' + str(wrd_user))
            if wrd_user == wrd_data.word.italienisch:
                wrd_data.right = True
                wrd_data.fehlertest = False
                wrd_data.save()
            else:
                wrd_data.right = False
                wrd_data.fehlertest = False
                wrd_data.save()

            wrd_data.pruefung_reihung = 0
            wrd_data.save()
            words.append(wrd_data)

    else:
        words_all = Words_user.objects.filter(user=request.user, fuer_pruefung=True, lernweg_voc=False, right=False)[
                    0: request.user.profile.pruefung_voc]

        if not words_all:
            error = 'Keine falschen Wörter da, weiter gehts im Template'

        else:
            for wrd in words_all:
                wrd.fehlertest = False
                wrd.pruefung_reihung = 0
                wrd.save()

            durchgaenge = 0
            pruefungslaenge = request.user.profile.pruefung_voc
            durchgaenge_error = 0

            while durchgaenge < pruefungslaenge:
                try:
                    word_d = random.choice(words_all)
                    words.append(word_d)

                    if words.count(word_d) > 1:
                        words.remove(word_d)
                        durchgaenge -= 1

                    durchgaenge += 1
                    durchgaenge_error += 1
                    if durchgaenge_error > 30:
                        break

                except IndexError:
                    error = 'Keine falschen Wörter da, weiter gehts im Template'



            reihung = 1
            for word in words:
                word.fehlertest = True
                word.pruefung_reihung = reihung
                word.save()
                reihung += 1


    context = {'words': words, 'error': error}
    return render(request, 'usertests/fehlertest-schriftlich.html', context)


@login_required
def unittest_start(request):
    units = []
    units_gemacht_id = []
    units_gemacht = Units_user.objects.filter(user=request.user)[::-1]
    maximum_school = None
    maximum_language = None


    for unit_gemacht in units_gemacht:
        unit_real = Unit_name.objects.get(id=unit_gemacht.unit.id)
        units_gemacht_id.append(unit_real.id)
        units.append(unit_real)


    units_your_school = [u.schule for u in units]
    units_your_language = [s.sprache for s in units]
    try:
        units_count = Counter(units_your_school)
        maximum_school = max(units_count, key=units_count.get)
        # print(units_count[maximum_school])

        sprache_count = Counter(units_your_language) # this is a dictionary
        maximum_language = max(sprache_count, key=sprache_count.get)
        # print(sprache_count[maximum_language])
    except ValueError:
        pass


    units_id = [unit.id for unit in units]
    similar_units = Unit_name.objects.filter(schule=maximum_school, sprache=maximum_language).exclude(id__in=units_id)


    if similar_units:
        similar_split = split_list(similar_units)
    else:
        similar_split = None

    if units:
        units_split = split_list(units)
    else:
        units_split = None

    andere_units_schule = Unit_name.objects.filter(schule=maximum_school).exclude(id__in=units_id)
    print(andere_units_schule)

    if andere_units_schule:
        andere_units_split = split_list(andere_units_schule)
    else:
        andere_units_split = None

    schulen = Unit_schule.objects.all().exclude(schule=maximum_school)

    schulen_units_all = {}

    for schule in schulen:
        schulen_units = Unit_name.objects.filter(schule=schule)
        schulen_units_all[str(schule)] = {}
        sprachen_schule = []
        sprachen_schule_kurz = [] # ist für die Kurzbezeichnung der Sprache, z.B. IT für Italienisch (wird später für query gebraucht)

        for schule_unit in schulen_units:

            schule_unit_sprache_lang = schule_unit.sprache.get_sprache_display() # ist die lange Bezeichnung, z.B Italienisch für IT
            sprachen_schule_kurz.append(schule_unit.sprache)
            sprachen_schule.append(schule_unit_sprache_lang)

            if sprachen_schule.count(schule_unit_sprache_lang) > 1:
                sprachen_schule.remove(schule_unit_sprache_lang)
            else:
                pass

            for sprache_schule, sprache_kurz in zip(sprachen_schule, sprachen_schule_kurz):
                schulen_units_all[str(schule)][str(sprache_schule)] = split_list([unit_name for unit_name in Unit_name.objects.filter(
                    sprache=sprache_kurz, schule=schule
                )])



    # print(schulen_units_all)

    context = {'units_latest': units_split, 'similar_units': similar_split, 'schulen_units': schulen_units_all, 'andere_units_schule': andere_units_split}
    return render(request, 'usertests/unittest-start.html', context)

@login_required

def unittest_method(request, name_of_unit):
    for name in Unit_name.objects.all():
        if str(name_of_unit) == str(name):
            obj = get_object_or_404(Unit_name, id=name.id)

    return render(request, 'usertests/unittest_method.html', {'unit': obj})



def error_message(words_right_false):
    if [key for key in words_right_false.keys()].count('false') > [key for key in words_right_false.keys()].count(
            'right') or \
            [key for key in words_right_false.keys()].count('false') == len(words_right_false) or \
            [key for key in words_right_false.keys()].count('false') > len(words_right_false) * 0.8:
        message = 'yes'  # falls der User zu viel falsch hat, kann das daran liegen, dass er z.B  zwei Unit-Test Tabs offen hat

        return message

def test(request, schriftlich, name_of_unit):
    for name in Unit_name.objects.all():
        if str(name_of_unit) == str(name):
            obj = get_object_or_404(Unit_name, id=name.id)

    words_right_false = {}

    if request.method == 'POST':
        database_ids = request.user.profile.unittest.split(',')
        words_for_user = [Unit_words.objects.get(id=db_id) for db_id in database_ids]
        values_from_user = []

        if schriftlich == True:
            values_from_user = request.POST.getlist('my_list')  # was der user im template in <input> eingegeben hat


        else:
            for word_for_user in words_for_user:
                words_list = request.POST.getlist(
                    str(word_for_user))  # hoffentlich sind hier keine zwei gleichen Wörter, sonst bin ich im Arsch
                values_from_user.extend(words_list)


        for value, data in zip(values_from_user, words_for_user):
            if str(value) == str(data):
                words_right_false[data] = 'right'
            else:
                words_right_false[data] = 'false'



    else:
        if schriftlich == True:
            words = Unit_words.objects.filter(unit_name=obj)

            words_id = [word.id for word in words]
            random.shuffle(words_id)
            words_right_false['words'] = [Unit_words.objects.get(id=random_word) for random_word in words_id]



            profile_update = request.user.profile
            words_id_str = str(words_id)
            profile_update.unittest = words_id_str[1:len(
                words_id_str) - 1]  # hier wird die liste in einen str verwandelt die Klammern [] fallen weg, danach wird nach ',' gesplitted
            profile_update.save()

        else:
            words = Unit_words.objects.filter(unit_name=obj)
            words_id = [word.id for word in words]
            random.shuffle(words_id)
            random_words = [Unit_words.objects.get(id=random_word) for random_word in words_id]

            profile_update = request.user.profile
            words_id_str = str(words_id)
            profile_update.unittest = words_id_str[1:len(
                words_id_str) - 1]  # hier wird die liste in einen str verwandelt die Klammern [] fallen weg, danach wird nach ',' gesplitted
            profile_update.save()

            for wrd in words_id:
                wrd_full = Unit_words.objects.get(id=wrd)
                wrd_selection_ids = []
                wrd_selection_ids.append(wrd)

                words_unit = [word_id.id for word_id in
                              Unit_words.objects.filter(unit_name=wrd_full.unit_name).exclude(id=wrd)]
                random.shuffle(words_unit)
                words_unit = words_unit[0:3]

                wrd_selection_ids.extend(words_unit)

                random.shuffle(wrd_selection_ids)
                words_right_false[wrd_full] = [Unit_words.objects.get(id=wrd_real) for wrd_real in wrd_selection_ids]

    return words_right_false

def unit_exists(name_of_unit):
    for name in Unit_name.objects.all():
        if str(name_of_unit) == str(name):
            obj = get_object_or_404(Unit_name, id=name.id)
            return obj

@login_required
def unittest_schriftlich(request, name_of_unit, *args):
    random_words = []
    obj = None
    words_right_false = {}
    message = None

    for name in Unit_name.objects.all():
        if str(name_of_unit) == str(name):
            get_object_or_404(Unit_name, id=name.id)
            obj = get_object_or_404(Unit_name, id=name.id)
            obj
    if request.method == 'POST':
        values_from_user = request.POST.getlist('my_list')  # was der user im template in <input> eingegeben hat
        database_ids = request.user.profile.unittest.split(',')
        words_for_user = [Unit_words.objects.get(id=db_id) for db_id in database_ids]

        for value, data in zip(values_from_user, words_for_user):
            if str(value) == str(data):
                words_right_false[data] = 'right'
            else:
                words_right_false[data] = 'false'


        if [key for key in words_right_false.keys()].count('false') > [key for key in words_right_false.keys()].count('right') or \
            [key for key in words_right_false.keys()].count('false') == len(words_right_false) or \
            [key for key in words_right_false.keys()].count('false') > len(words_right_false) * 0.8:
            message = 'yes' # falls der User zu viel falsch hat, kann das daran liegen, dass er z.B  zwei Unit-Test Tabs offen hat

    else:


        words = Unit_words.objects.filter(unit_name=obj)

        words_id = [word.id for word in words]
        random.shuffle(words_id)
        words_right_false['words'] = [Unit_words.objects.get(id=random_word) for random_word in words_id]

        profile_update = request.user.profile
        words_id_str = str(words_id)
        profile_update.unittest = words_id_str[1:len(words_id_str)-1] # hier wird die liste in einen str verwandelt die Klammern [] fallen weg, danach wird nach ',' gesplitted
        profile_update.save()


    context = {'unit': obj, 'words': words, 'message': message, 'words_right_false': words_right_false}
    return render(request, 'usertests/unittest_schriftlich.html', context)


@login_required
def unittest_karteikarten(request, name_of_unit, *args):
    random_words = []
    obj = None
    message = None
    words_right_false = {}

    for name in Unit_name.objects.all():
        if str(name_of_unit) == str(name):
            obj = get_object_or_404(Unit_name, id=name.id)

    if request.method == 'POST':
        values_from_user = []
        database_ids = request.user.profile.unittest.split(',')
        words_for_user = [Unit_words.objects.get(id=db_id) for db_id in database_ids]

        for word_for_user in words_for_user:
            words_list = request.POST.getlist(str(word_for_user)) # hoffentlich sind hier keine zwei gleichen Wörter, sonst bin ich im Arsch
            values_from_user.extend(words_list)



        for data, value in zip(words_for_user, values_from_user):
            print(data)
            print(value)
            print('')

            if str(data) == str(value):
                words_right_false[data] = 'right'
            else:
                words_right_false[data] = 'false'


        # print(words_right_false)

        if [key for key in words_right_false.keys()].count('false') > [key for key in words_right_false.keys()].count('right') or \
            [key for key in words_right_false.keys()].count('false') == len(words_right_false) or \
            [key for key in words_right_false.keys()].count('false') > len(words_right_false) * 0.8:
            message = 'yes' # falls der User zu viel falsch hat, kann das daran liegen, dass er z.B  zwei Unit-Test Tabs offen hat

    else:

        words = Unit_words.objects.filter(unit_name=obj)
        words_id = [word.id for word in words]
        random.shuffle(words_id)
        random_words = [Unit_words.objects.get(id=random_word) for random_word in words_id]

        profile_update = request.user.profile
        words_id_str = str(words_id)
        profile_update.unittest = words_id_str[1:len(
            words_id_str) - 1]  # hier wird die liste in einen str verwandelt die Klammern [] fallen weg, danach wird nach ',' gesplitted
        profile_update.save()

        for wrd in words_id:
            wrd_full = Unit_words.objects.get(id=wrd)
            wrd_selection_ids = []
            wrd_selection_ids.append(wrd)

            words_unit = [word_id.id for word_id in Unit_words.objects.filter(unit_name=wrd_full.unit_name).exclude(id=wrd)]
            random.shuffle(words_unit)
            words_unit = words_unit[0:3]

            wrd_selection_ids.extend(words_unit)

            random.shuffle(wrd_selection_ids)
            words_right_false[wrd_full] = [Unit_words.objects.get(id=wrd_real) for wrd_real in wrd_selection_ids]

        messages.error(request, 'Aufgepasst: Du musst eine der 4 Optionen auswählen')

    context = {'unit': obj, 'words': random_words, 'message': message, 'words_right_false': words_right_false}
    return render(request, 'usertests/unittest_karteikarten.html', context)