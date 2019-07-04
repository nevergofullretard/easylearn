from datetime import date
from datetime import timedelta


from django.contrib.auth.models import User

from django.utils import timezone   #für startseite Posts filter
from django.shortcuts import render, get_object_or_404, Http404
from django.http import Http404
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from users.models import Units_user, Words_user

from blog.models import Post
from .models import Unit_name, Unit_words, Unit_schule, Unit_sprache, Anfrage_sprache, Anfrage_schule, Anfrage_words_user, Anfrage_unit
from .forms import UploadFileForm, UserNewWordsForm, UserExistingUnitForm, NewSchoolForm, NewLangForm
from users import views as users_views


def schule_sprache_unit(request, schule_pk, sprache_pk):
    schule = ""
    sprache = ""
    schulen = []
    sprachen = []
    units = None

    if int(schule_pk) != 0:
        schule = get_object_or_404(Unit_schule, id=int(schule_pk))
    if int(sprache_pk) != 0:
        sprache = get_object_or_404(Unit_sprache, id=int(sprache_pk))
    if int(sprache_pk) == 0 and int(schule_pk) == 0:
        schulen = Unit_schule.objects.all()
        sprachen = Unit_sprache.objects.all()
    elif int(schule_pk) == 0:
        units = Unit_name.objects.filter(sprache=sprache)
    elif int(sprache_pk) == 0:
        units = Unit_name.objects.filter(schule=schule)


    if schule and sprache:
        units = Unit_name.objects.filter(sprache=sprache, schule=schule)
    if sprache and units:
        for school in [obj.schule for obj in units]:
            if school not in schulen:
                schulen.append(school)
    if schule and units:
        for lang in [obj.sprache for obj in units]:
            if lang not in sprachen:
                sprachen.append(lang)

    print(units)
    print(schulen)
    print(sprachen)
    return render(request, 'units/schule-sprache-unit.html', {'schule': schule, 'sprache':sprache, 'units': units, 'sprachen': sprachen, 'schulen': schulen})


def unit_exists(pk, name_of_unit, user=None , statistics=False):
    obj = None
    unit_ids = []
    if statistics == False:

        obj = get_object_or_404(Unit_name.objects.all(), id=pk)
        if str(obj) != str(name_of_unit):
            raise Http404('help me :(')
        else:
            return obj


    else:

        obj = get_object_or_404(Units_user.objects.filter(user=user), id=pk)


        if str(obj.unit) != str(name_of_unit):
            raise Http404('help me :(')
        else:
            return obj


def schulen_units(schulen):

    schulen_units_all = {}

    for schule in schulen:
        schulen_units = Unit_name.objects.filter(schule=schule)
        schulen_units_all[str(schule)] = {}
        sprachen_schule = []
        sprachen_schule_kurz = []  # ist für die Kurzbezeichnung der Sprache, z.B. IT für Italienisch (wird später für query gebraucht)

        for schule_unit in schulen_units:
            schule_unit_sprache_lang = schule_unit.sprache  # ist die lange Bezeichnung, z.B Italienisch für IT
            sprachen_schule_kurz.append(schule_unit.sprache)
            sprachen_schule.append(schule_unit_sprache_lang)

            if sprachen_schule.count(schule_unit_sprache_lang) > 1:
                sprachen_schule.remove(schule_unit_sprache_lang)

            # for sprache_schule, sprache_kurz in zip(sprachen_schule, sprachen_schule_kurz):
            #     schulen_units_all[str(schule)][str(sprache_schule)] = None
            #     for unit_names in Unit_name.objects.filter(sprache=sprache_kurz, schule=schule):

            # print(sprachen_schule)
            for sprache_schule, sprache_kurz in zip(sprachen_schule, sprachen_schule_kurz):
                schulen_units_all[str(schule)][str(sprache_schule.sprache_lang)] = split_list(
                    [unit_name for unit_name in Unit_name.objects.filter(
                        sprache=sprache_schule, schule=schule
                    )])

                # print(
                #     [unit_name for unit_name in Unit_name.objects.filter(
                #         sprache=sprache_kurz, schule=schule
                #     )])
                    # print(schulen_units_all)

    return schulen_units_all


def split_list(a_list):
    half = int(len(a_list) // 2)
    if half == 0:
        return zip(a_list, [' '])

    first_half = a_list[:half]
    second_half = a_list[half:]
    if len(first_half) < len(second_half):
        first_half.append(' ')
    # print(first_half)
    # print(second_half)
    return zip(first_half, second_half)

def units(request):
    diese_unit = None
    words_today = None
    words_yesterday = None
    posts_diese_woche = None
    post_today = timezone.now()
    post_yesterday = post_today - timezone.timedelta(1)
    post_this_week = post_today - timezone.timedelta(7)
    today = date.today()
    yesterday = today - timedelta(1)
    this_week = today - timedelta(7)

    if request.user.is_authenticated:
        if request.user.profile.current_unit != 0:
            diese_unit = Unit_name.objects.get(id=request.user.profile.current_unit)

        words_today = Words_user.objects.filter(user=request.user, date=today, lernweg_voc=False) #hier dropdown zwischen alle, falsche und richtige
        words_yesterday = Words_user.objects.filter(user=request.user, date=yesterday, lernweg_voc=False) ##hier dropdown zwischen alle, falsche und richtige

    posts_all = {}

    posts_diese_woche = Post.objects.filter(date_posted__lte=post_today, date_posted__gte=post_this_week).order_by('-date_posted')
    print(posts_diese_woche)
    for post in posts_diese_woche:
        posts_all[post.id] = post
    words_diese_woche = Unit_words.objects.filter(date__range=(this_week, today))[::-1]

    units = {}
    for word in words_diese_woche:
        if word.unit_name not in units:
            units[word.unit_name] = [word]
        else:
            if word not in units[word.unit_name]:
                units[word.unit_name].append(word)






    context = {'unit': diese_unit, 'today': words_today, 'yesterday': words_yesterday, 'posts': posts_all, 'words': units, \
               'today_date': today, 'yesterday_date': yesterday}
    return render(request, 'units/units.html', context)


def unitname(request, pk, name_of_unit):

    obj = unit_exists(user=request.user, pk=pk, name_of_unit=name_of_unit)

    # for name in Unit_name.objects.all():
    #     if str(name_of_unit) == str(name):
    #         obj = get_object_or_404(Unit_name, id=name.id)




    context = {'unit_names': Unit_name.objects.all(), 'name': obj,
               'words': Unit_words.objects.filter(unit_name_id=obj.id), 'url': request.META["HTTP_HOST"]}
    return render(request, 'units/unit_content.html', context)




def units_all(request):
    # schulen = Unit_schule.objects.all()

    # schulen_units_all = schulen_units(schulen=schulen)


    # alle_units = Unit_name.objects.all()
    #
    # alle_dict = {}
    # for schule in Unit_schule.objects.all():
    #     units_schule = alle_units.filter(schule=schule)
    #     schule_words = Unit_words.objects.filter(unit_name__in=units_schule)
    #
    #
    #     if units_schule and schule_words:
    #         alle_dict[str(schule)] = {}
    #
    #         for sprache in Unit_sprache.objects.all():
    #             units_schule_sprache = units_schule.filter(sprache=sprache)
    #             units_schule_sprache_all = []
    #             for schule_sprache in units_schule_sprache: # ist mir egal ob da schon Wörter drinnen sind oder noch nicht, hab keine Zeit mehr!
    #                 print(schule_sprache.id)
    #                 if Unit_words.objects.filter(unit_name__id=schule_sprache.id):
    #                     units_schule_sprache_all.append(schule_sprache)
    #                     alle_dict[str(schule)][str(schule_sprache.sprache.sprache_lang)] = units_schule_sprache_all

    if request.user.is_authenticated:
        auswahl = users_views.units_auswahl(request, nur_volle_units=False, nur_alle=False)
    else:
        auswahl = users_views.units_auswahl(request, nur_volle_units=False, nur_alle=True)
    context = {'naechste_unit': auswahl['next'], 'similar': auswahl['similar'], 'alle': auswahl['alle'],
               'units_gemacht': auswahl['dict_units_gemacht'], 'current_unit': auswahl['current_unit']}

    # context = {'alle': alle_dict}
    return render(request, 'units/units_all.html', context)

@staff_member_required
def new_words(request):
    link = None
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)

        if form.is_valid():
            file = form.cleaned_data.get('file')
            print(str(file))
    else:
        form = UploadFileForm()
        link = f'http://{request.META["HTTP_HOST"]}/media/templates/new_words2.csv'

    return render(request, 'units/new-words.html', {'form': form, 'link': link})

@login_required
def new_words_user(request):
    if request.method == 'POST':
        form = UserNewWordsForm(request.POST)

        if form.is_valid():
            unit = form.cleaned_data.get('unit')
            sprache = form.cleaned_data.get('sprache')
            schule = form.clean().get('schule')

            if ',' not in unit and '/' not in unit and '#' not in unit:
                Anfrage_unit.objects.create(user=request.user, sprache_id=sprache, schule=schule, unit=unit)
                messages.success(request, 'Anfrage wurde gesendet')
                anfragen = Anfrage_unit.objects.all()
                max = 20
                if anfragen.count() > max:
                    first = Anfrage_unit.objects.all()[:1].get()
                    first.delete()
            else:
                messages.error(request, 'Sorry, aber "," "/" und "#" ist im Unitnamen nicht erlaubt!')

    else:
        form = UserNewWordsForm()


    return render(request, 'units/new-words-user.html', {'form': form})

@login_required
def new_unit_user(request):
    context = {}
    if request.method == 'POST':

        all_values = []
        for i in range(1, 50):
            values_fremd = request.POST.getlist(str(i) + 'fremd')
            values_deutsch = request.POST.getlist(str(i) + 'deutsch')
            values_sidenote = request.POST.getlist(str(i) + 'sidenote')
            for value1, value2, value3 in zip(values_fremd, values_deutsch, values_sidenote):
                if value1 != '' and value2 != '' and ';' not in value1 and ';' not in value2 and ';' not in value3:
                    all_values.append([value1, value2, value3])
                elif ';' in value1 or ';' in value2 or ';' in value3:
                    messages.error(request, 'Sorry, aber ";" ist nicht erlaubt! Die restlichen Wörter wurden zur Anfrage geschickt.')


        new_unit = request.POST.get('unit')
        unit = Unit_name.objects.get(id=new_unit)

        for value in all_values:
            print(value)

            Anfrage_words_user.objects.create(user=request.user, unit=unit, word_fremdsprache=value[0], word_deutsch=value[1], sidenote=value[2])

            anfragen = Anfrage_words_user.objects.all()
            max = 5000
            if anfragen.count() > max:
                words_delete = Anfrage_words_user.objects.all()[::1][0:anfragen.count()-max]

                for word_delete in words_delete:
                    word_delete.delete()

        messages.success(request, 'Anfrage wurde gesendet')


    else:
        auswahl = users_views.units_auswahl(request, nur_volle_units=False, nur_alle=False)
        context = {'naechste_unit': auswahl['next'], 'similar': auswahl['similar'], 'alle': auswahl['alle'],
                   'units_gemacht': auswahl['dict_units_gemacht'], 'range1': [x for x in range(1,15)], 'range2': [x for x in range(15, 50)]}
    return render(request, 'units/new-unit-user.html', context)
@login_required
def new_words_start(request):
    return render(request, 'units/new-words-start.html')

@staff_member_required
def anfragen(request):
    users = User.objects.all()
    units_alt = Unit_name.objects.all()
    anfragen = Anfrage_words_user.objects.all()
    words_anfragen = {}
    added = []
    deleted = []
    for user in users:
        if user in [anfrage.user for anfrage in anfragen]:
            user_unit_einzeln = []
            for unit in units_alt:
                user_units = Anfrage_words_user.objects.filter(user=user, unit=unit)
                if user_units != []:
                    for user_unit in user_units:
                        if user_unit.unit not in user_unit_einzeln:
                            user_unit_einzeln.append(user_unit.unit)
            # print(user_unit_einzeln)
            words_anfragen[user] = []
            for unit_u in user_unit_einzeln:
                words = Anfrage_words_user.objects.filter(user=user, unit=unit_u)
                # print(words)

                words_anfragen[user].append(
                    {unit_u: zip([anfr for anfr in words], [word.word_fremdsprache for word in words], [word.word_deutsch for word in words], [word.sidenote for word in words])})

    if request.method == 'POST':
        for key, values in words_anfragen.items():
            user = key
            for value in values:
                for key in value:
                    unit = key
                    value_from_user = request.POST.getlist(str(user.id) + '--' + str(unit.id))
                    if value_from_user != []:
                        for value in value_from_user:
                            einzeln = value.split(';')
                            if request.POST.get("add"):

                                try:
                                    delete_anfrage = Anfrage_words_user.objects.get(id=einzeln[2])

                                    if not Unit_words.objects.filter(unit_name=unit, italienisch=einzeln[0], deutsch=einzeln[1]):
                                        Unit_words.objects.create(unit_name=unit, italienisch=einzeln[0], deutsch=einzeln[1], sidenote=einzeln[3])
                                        added.append(str(einzeln[0]) + ' - '+ str(einzeln[1]))
                                    else:
                                        messages.error(request, f'Das Wort {einzeln[0]}--{einzeln[1]} ist in der betreffenden Unit bereits vorhanden! Die Anfrage wird nun gelöscht!')
                                    delete_anfrage.delete()
                                except IndexError:
                                    messages.error(request, 'Bitte den Vorgang nicht versuchen zu wiederholen!!!')
                            elif request.POST.get('delete'):
                                delete_anfrage = Anfrage_words_user.objects.get(id=einzeln[2])
                                delete_anfrage.delete()
                                deleted.append(delete_anfrage)

    else:
        # units_neu = Anfrage_unit.objects.all()
        # schulen = Anfrage_schule.objects.all()


        for key, values in words_anfragen.items():
            print(key)
            for value in values:
                for key in value:
                    print(key)

    return render(request, 'units/anfragen.html', {'anfragen': words_anfragen, 'added': added, 'deleted': deleted})


@login_required
def new_school(request):
    if request.method == 'POST':
        new_school = NewSchoolForm(request.POST)
        if new_school.is_valid():
            schule = new_school.cleaned_data.get('schule')
            if ',' not in schule and '/' not in schule and '#' not in schule:
                Anfrage_schule.objects.create(user=request.user, schule=schule)
                messages.success(request, 'Anfrage wurde gesendet')
                anfragen = Anfrage_schule.objects.all()
                max = 20
                if anfragen.count() > max:
                    first = Anfrage_schule.objects.all()[:1].get()
                    first.delete()
            else:
                messages.error(request, 'Sorry, aber "," "/" und "#" darf nicht enthalten sein')

    else:
        new_school = NewSchoolForm()

    return render(request, 'units/new-school.html', {'new_school': new_school})

@login_required
def new_lang(request):
    if request.method == 'POST':
        new_lang = NewLangForm(request.POST)
        if new_lang.is_valid():
            sprache_lang = new_lang.cleaned_data.get('sprache_lang')
            sprache_kurz = new_lang.cleaned_data.get('sprache_kurz')
            if ',' in sprache_lang or ',' in sprache_kurz or "/" in sprache_lang or "/" in sprache_kurz or "#" in sprache_lang or "#" in sprache_kurz:
                messages.error(request, 'Sorry, aber "," "/" und "#" darf nicht enthalten sein')
            else:
                Anfrage_sprache.objects.create(user=request.user, sprache_lang=sprache_lang, sprache_kurz=sprache_kurz)
                messages.success(request, 'Anfrage wurde gesendet')
                anfragen = Anfrage_sprache.objects.all()
                max = 20
                if anfragen.count() > max:
                    first = Anfrage_sprache.objects.all()[:1].get()
                    first.delete()

    else:
        new_lang = NewLangForm()
    return render(request, 'units/new-lang.html', {'new_lang': new_lang})

@staff_member_required
def dashboard(request):
    return render(request, 'units/dashboard.html')


@staff_member_required
def anfragen_rest(request):
    hinzugefuegt = []
    alle_anfragen = []

    if request.method == 'POST':
        units = request.POST.getlist('units')
        sprachen = request.POST.getlist('sprachen')
        schulen = request.POST.getlist('schulen')
        if request.POST.get("add"):
            for unit in units:
                unit = unit.split(',')
                try:
                    anfrage = Anfrage_unit.objects.get(id=unit[3])
                    if not Unit_name.objects.filter(sprache__id=int(unit[0]), schule__id=int(unit[1]), u_name=unit[2]):
                        Unit_name.objects.create(sprache=Unit_sprache.objects.get(id=int(unit[0])),
                                                 schule=Unit_schule.objects.get(id=int(unit[1])), u_name=unit[2])
                        hinzugefuegt.append(anfrage)
                    else:
                        messages.error(request,
                                       f'Die Unit {unit[2]} existiert bereits! Sie wird jetzt aus den Anfragen gelöscht.')
                    anfrage.delete()
                except:
                    pass

            for sprache in sprachen:
                sprache = sprache.split(',')
                try:
                    anfrage = Anfrage_sprache.objects.get(id=sprache[2])
                    if not Unit_sprache.objects.filter(sprache_lang=sprache[0]) or not Unit_sprache.objects.filter(
                            sprache_kurz=sprache[1]):
                        Unit_sprache.objects.create(sprache_lang=sprache[0], sprache_kurz=sprache[1].upper())
                        hinzugefuegt.append(anfrage)
                    else:
                        messages.error(request,
                                       f'Die Sprache {sprache[0]} existiert bereits! Sie wird jetzt aus den Anfragen gelöscht.')
                    anfrage.delete()
                except:
                    pass

            for schule in schulen:
                schule = schule.split(',')
                try:
                    anfrage = Anfrage_schule.objects.get(id=schule[1])


                    if not Unit_schule.objects.filter(schule=schule[0]):
                        Unit_schule.objects.create(schule=schule[0].upper())
                        hinzugefuegt.append(anfrage)
                    else:
                        messages.error(request, f'Diese Schule {schule[0]} existiert bereits! Sie wird jetzt aus den Anfragen gelöscht.')
                    anfrage.delete()
                except:
                    pass
        elif request.POST.get("delete"):
            alle_anfragen = []
            for unit in units:
                unit = unit.split(',')
                anfrage = Anfrage_unit.objects.get(id=unit[3])
                alle_anfragen.append(anfrage)
                anfrage.delete()
            for sprache in sprachen:
                sprache = sprache.split(',')
                anfrage = Anfrage_sprache.objects.get(id=sprache[2])
                alle_anfragen.append(anfrage)
                anfrage.delete()
            for schule in schulen:
                schule = schule.split(',')
                anfrage = Anfrage_schule.objects.get(id=schule[1])
                alle_anfragen.append(anfrage)
                anfrage.delete()


    else:
        units = Anfrage_unit.objects.all()[::-1]
        sprachen = Anfrage_sprache.objects.all()[::-1]
        schulen = Anfrage_schule.objects.all()[::-1]


    return render(request, 'units/anfragen-rest.html', {'units':units, 'sprachen': sprachen, 'schulen': schulen, 'hinzugefuegt': hinzugefuegt, 'deleted': alle_anfragen})