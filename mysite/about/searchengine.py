from collections import OrderedDict
from operator import itemgetter
from difflib import SequenceMatcher

from django.shortcuts import render, HttpResponse
from units.models import Unit_words, Unit_name, Unit_schule, Unit_sprache

from users.models import Profile, Words_user, Unit_words, Units_user
from blog.models import Post


def suchen(request, input):
    words = []
    words_user = []
    units_user = []
    units = []
    sprache = []
    schule = []
    posts = []

    all_dict = {'words': {}, 'units': {}, 'posts': {}, 'schule': {}, 'sprache': {}}
    full_dict_as_list = []
    # print(all_dict['words'])


    # '''ganze Wörter filtern'''
    # words = Unit_words.objects.filter(italienisch=input)
    # if not words:
    #     words = Unit_words.objects.filter(deutsch=input)
    # if words:
    #     for val in words:
    #         all_dict['words'][val] = 100
    # ''' '''
    #
    # '''ganze Units filtern'''
    # input_fuer_unit_getrennt = input.split(
    #     '-')  # wenn jemand ganze Unit von autocomplete-Feld eingibt, z.B. Unit1-HAK-IT
    # try:
    #     units = Unit_name.objects.filter(u_name=input_fuer_unit_getrennt[0], schule__schule=input_fuer_unit_getrennt[1],
    #                                      sprache__sprache_kurz=input_fuer_unit_getrennt[2])
    # except IndexError:
    #     pass
    #
    # if not units:
    #     units = Unit_name.objects.filter(u_name=input)
    #     if not units:
    #         units = Unit_name.objects.filter(schule__schule=input.upper()) # das geliche wie bei sprache_kurz
    #         if not units:
    #             units = Unit_name.objects.filter(sprache__sprache_kurz=input.upper())   #wenn man z.B. "it" eingibt, das man trd zu zB Unit1-HAK-IT kommt
    #             if not units:
    #                 units = Unit_name.objects.filter(sprache__sprache_lang=input)
    # if units:
    #     for val in units:
    #         all_dict['units'][val] = 100
    # ''' '''
    #
    # '''ganze Schulen und Sprachen filtern'''
    # schule = Unit_schule.objects.filter(schule=input)
    # sprache = Unit_sprache.objects.filter(sprache_lang=input)
    # if not sprache:
    #     sprache = Unit_sprache.objects.filter(sprache_kurz=input)
    # if sprache:
    #     for val in sprache:
    #         all_dict['sprache'][val] = 100
    # if schule:
    #     for val in schule:
    #         all_dict['schule'][val] = 100
    # ''' '''
    #
    # '''ganze Posts filtern'''
    # posts = Post.objects.filter(title=input)
    # if not posts:
    #     posts = Post.objects.filter(author__username=input)
    #     if not posts:
    #         posts = Post.objects.filter(linked__username=input)
    #         if not posts:
    #             posts = Post.objects.filter(content=input)
    # if posts:
    #     for val in posts:
    #         all_dict['posts'][val] = 100
    #
    # ''' ''' ''' ''' ''' '''

    max_dict = {}  # enthält nur die dict_keys (words, units,...) und den größten Wert (bis zu 100%)

    for key, val in all_dict.items():
        maximum_prob = 0
        ausgangs_key = None
        max_value_in_dict = []
        if key == 'words':
            ausgangs_key = 'words'
            suchen_in = Unit_words.objects.all()
        elif key == 'units':
            ausgangs_key = 'units'
            suchen_in = Unit_name.objects.all()
        elif key == 'posts':
            ausgangs_key = 'posts'
            suchen_in = Post.objects.all()  #title

        elif key == 'sprache':
            ausgangs_key = 'sprache'
            suchen_in = Unit_sprache.objects.all() #sprache_kurz

        elif key == 'schule':
            ausgangs_key = 'schule'
            suchen_in = Unit_schule.objects.all()
        else:
            print('falscher key in Dictionary für Suche')
            return 'falscher Schlüssel' # würde wahrscheinlich in production für probleme sorgen aber ist mir jetzt egal


        for value in suchen_in:
            lst = all_dict[ausgangs_key]

            # print(input.upper() + ' --- ' + str(value).upper())

            prob = SequenceMatcher(None, input.upper(), str(value).upper()).ratio()
            if key == 'units':
                prob2 = SequenceMatcher(None, input.upper(), str(value.u_name).upper()).ratio()
                maximum_prob = max(prob, prob2)
            elif key == 'words':
                prob2 = SequenceMatcher(None, input.upper(), str(value.deutsch).upper()).ratio()
                maximum_prob = max(prob, prob2)

            elif key == 'sprache':
                prob2 = SequenceMatcher(None, input.upper(), str(value.sprache_lang).upper()).ratio()
                maximum_prob = max(prob, prob2)
            elif key == 'posts':
                prob2 = SequenceMatcher(None, input.upper(), str(value.author).upper()).ratio()
                prob3 = SequenceMatcher(None, input.upper(), str(value.content).upper()).ratio()

                for user in value.linked.all():
                    prob4 = SequenceMatcher(None, input, str(user)).ratio()
                maximum_prob = max(prob, prob2, prob3, prob4)


            else: # für alle anderen Bezeichnungen z.B: eigentlich eh nur noch für Schulen, ACHTUNG FEHLERANFÄLLIG!!
                maximum_prob = prob

            if maximum_prob > 0.0:
                # print('{} - {}'.format(value, maximum_prob))
                all_dict[ausgangs_key][value] = maximum_prob * 100
                max_value_in_dict.append(maximum_prob * 100)

        all_dict[ausgangs_key] = OrderedDict(sorted(all_dict[ausgangs_key].items(), key=itemgetter(1), reverse=True))
        try:
            max_dict[ausgangs_key] = max(max_value_in_dict) # z.B: {'words': 100, 'units': 90}, also nur die höchsten Werte
        except ValueError:  #EmptySequence, wenn keine Lösungen mit über 0.0 % Übereinstimmung
            max_dict[ausgangs_key] = 0

    max_dict = OrderedDict(sorted(max_dict.items(), key=itemgetter(1), reverse=True))
    new_dict = {}
    for key1, value1 in max_dict.items():
        # einbauen: if key1 == 'words' nach words_user suchen, wenn user angemeldet usw!
        # if user.is_authenticated():
        #     pass
        # else:
        new_dict[key1] = all_dict[key1]
    if request.user.is_authenticated:
        for category, dict2 in new_dict.items():
            if category == 'words':
                for word, probability in dict2.items():
                    new_dict[category][word] = {probability: Words_user.objects.filter(user=request.user, lernweg_voc=False, word=word)}
            elif category == 'units':
                for unit, probability in dict2.items():
                    new_dict[category][unit] = {probability: Words_user.objects.filter(user=request.user, lernweg_voc=False, word__unit_name=unit)}


    return (new_dict)

    #
    # lst = [1,2,4]
    # for index, value in enumerate(lst):
    #     if not value < 3:
    #         lst.insert(index,3)
    #         break
    # print(lst)



                    # try:
                        #     lst[prob4*100].append(value)
                        # except KeyError:
                        #     lst[prob4*100] = [value]
                        # # print(user)

    #             try:
    #                 if request.user.is_authenticated:
    #                     if key == 'words':
    #                         lst[prob*100].append({value: Words_user.objects.filter(user=request.user, lernweg_voc=False, word=value)})
    #                     elif key == 'units':
    #                         units_all = [wrd.word.unit_name for wrd in Words_user.objects.filter(user=request.user, lernweg_voc=False)[::-1]]
    #                         for wrd in units_all:
    #                             maximum = max(prob, prob2)
    #                             if value == wrd:
    #                                 lst[maximum * 100].append({value: [value]})
    #                                 break
    #                         if value not in units_all:
    #                             lst[maximum * 100].append({value: []})
    #
    #
    #                     else:
    #                         lst[prob * 100].append(value)
    #                         if key == 'sprache' or key == 'posts':
    #                             lst[prob2 * 100].append(value)
    #                         if key == 'posts':
    #                             lst[prob3 * 100].append(value)
    #                 else:
    #                     lst[prob*100].append(value)
    #                     if key == 'sprache' or key == 'posts':
    #                         lst[prob2*100].append(value)
    #                     if key == 'posts':
    #                         lst[prob3*100].append(value)
    #
    #             except KeyError:
    #                 if request.user.is_authenticated:
    #                     if key == 'words':
    #                         lst[prob*100] = [{value: Words_user.objects.filter(user=request.user, lernweg_voc=False, word=value)}]
    #                     elif key == 'units':
    #                         # lst[prob * 100] = [{value: Units_user.objects.filter(user=request.user, unit=value)}]
    #                         units_all = [wrd.word.unit_name for wrd in
    #                                      Words_user.objects.filter(user=request.user, lernweg_voc=False)[::-1]]
    #                         for wrd in units_all:
    #                             maximum = max(prob, prob2)
    #                             if value == wrd:
    #                                 lst[maximum*100] = [{value: [value]}]
    #                         if value not in units_all:
    #                             lst[maximum*100] = [{value: []}]
    #
    #                     else:
    #                         lst[prob * 100] = [value]
    #                         if key == 'sprache' or key == 'posts':
    #                             lst[prob2 * 100] = [value]
    #                         if key == 'posts':
    #                             lst[prob3 * 100] = [value]
    #
    #                 else:
    #                     lst[prob * 100] = [value]
    #                     if key == 'sprache' or key == 'posts':
    #                         lst[prob2*100] = [value]
    #                     if key == 'posts':
    #                         lst[prob3*100] = [value]
    #
    #         all_dict[ausgangs_key] = OrderedDict(sorted(all_dict[ausgangs_key].items(), reverse=True))
    #     else:
    #         print('schon Wörter drinnen (ganze Suche)')
    #         if request.user.is_authenticated:
    #             for key2, value in val.items():  #key=zB 100%, value = [[hello], [ok cool],...]
    #                 print('Value: ' + str(value))
    #                 for index, vall in enumerate(value):
    #                     if key == 'words':
    #                         value[index] = {vall: Words_user.objects.filter(user=request.user, lernweg_voc=False, word=vall)}
    #                     if key == 'units':
    #                         units_all = [wrd.word.unit_name for wrd in
    #                                      Words_user.objects.filter(user=request.user, lernweg_voc=False)[::-1]]
    #                         for wrd in units_all:
    #                             if vall == wrd:
    #                                 value[index] = {vall: [vall]}
    #                         if vall not in units_all:
    #                             value[index] = {vall: []}
    #
    #
    #
    # new_dict = {}
    # stats = {}
    # for key, values in all_dict.items():
    #     stats[key] = None
    #
    #     # for key2, value in values.items():
    #     #     new_dict[key][key2] = value
    #
    #     try:
    #         lst_prob = [val for val in values][0]    #prob: probability
    #         stats[key] = lst_prob
    #     except IndexError:
    #         pass
    #
    #
    # geordnet_max = sorted_x = sorted(stats.items(), key=itemgetter(1), reverse=True)
    # for heading in geordnet_max:
    #     try:
    #         new_dict[heading[0]] = all_dict[heading[0]]
    #     except IndexError:
    #         pass




def search(request):
    values_from_user = request.GET.getlist('name')

    searchengine = suchen(request, values_from_user[0])


    return render(request, 'about/searchengine2.html', {'results': searchengine, 'input': values_from_user[0]})