from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages

from units.models import Unit_words # ich weiß nicht warum es mir das anzeigt, aber alles funktioniert anscheinend normal
from users.models import Profile, Words_user

from django.contrib.auth.decorators import login_required

from .forms import UserRegisterForm, UserUpdateForm, CurrentUnitForm, SchriftlichPruefungItForm,\
    SchriftlichePruefungDeuForm, PruefungForm, LoginForm

from django.contrib.auth import authenticate, login # für automatischen Login nach Register und beim Login


import random

from django.contrib.auth.models import User
from .models import Pruefung_voc

from datetime import date # für Statistik, damit ich weiß wann das Vocabel geprüft wurde




'''Das ist die genailste Login Methode die ich jemals selbst geschrieben habe'''

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            print(username)
            print(password)

            if '@' in username:
                try:
                    user = User.objects.filter(email=username)[0]
                    username = user.username
                except IndexError:
                    username

            try:
                new_user = authenticate(username=username, password=password, )
                login(request, new_user)
            except AttributeError:
                messages.error(request, f"Sorry {username}, but your account doesn't exist!")

            return redirect('users-lernweg')

    else:
        form = LoginForm()

    context = {'form': form}
    return render(request, 'users/login.html', context)


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            messages.success(request, f'Danke {username}, dass du dich angemeldet hast! Du kannst nun alle Premium-Features nutzen!')

            new_user = authenticate(username=username, password=password,) # für Login nach Registrierung
            login(request, new_user)


            return redirect('users-start')
    else:
        form = UserRegisterForm()

    return render(request, 'users/register.html', {'form': form})



@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        # profile_form = UserProfileForm(request.POST, instance=request.user.profile)
        pruefung_form = PruefungForm(request.POST, instance=request.user.profile)

        if u_form.is_valid() and pruefung_form.is_valid():
            u_form.save()
            pruefung_form.save()
        #
        #     print(type(int(pruefung_form.data['pruefung_voc'])))
        #
        #
        #     if int(pruefung_form.data['pruefung_voc']) > request.user.profile.voc_bits:
        #         messages.error(request, f'Sorry {request.user}, deine Prüfungslänge kann nicht länger als deine Lernlänge sein')
        #
        #     if int(pruefung_form.data['pruefung_voc']) < request.user.profile.voc_bits:
        #         # pruefung_form.save()
        #         pass
        #
        messages.success(request, f'Nice {request.user}, your account has been updated!')
        return redirect('profile')

    else:
        u_form = UserUpdateForm(instance=request.user)
        # profile_form = UserProfileForm(instance=request.user)
        pruefung_form = PruefungForm(instance=request.user.profile)

    context = {
        'u_form': u_form, 'pruefung_form': pruefung_form
    }

    return render(request, 'users/profile.html', context)

@login_required
def start(request):
    context = {'username': request.user}
    return render(request, 'users/users-start.html', context)


@login_required
def lernweg(request):
    info = Profile.objects.filter(user_id=request.user.id)
    current_u = request.user.profile.current_unit


    if current_u == 0:
        if request.method == 'POST':
            unit_form = CurrentUnitForm(request.POST, instance=request.user.profile)
            if unit_form.is_valid():
                unit_form.save()
                return redirect('users-lernweg')

        else:
            unit_form = CurrentUnitForm(instance=request.user)

        context = {'unit_form': unit_form}
        return render(request, 'users/users-neuer-lernweg.html', context)


    voc_bits = request.user.profile.voc_bits
    first_voc = request.user.profile.first_voc
    last_voc = request.user.profile.last_voc

    if first_voc == 0:
        first = Unit_words.objects.get(unit_name_id=current_u) 
        first_id = first.id
        print('First ID: ' + str(first_id))
        print('Voc_bits: ' + str(voc_bits))



        words = Unit_words.objects.filter(unit_name_id=current_u)[first_voc:voc_bits].filter()  #die range, wie weit er Vocabeln zählt

        qry = Words_user.objects.filter(user=request.user, lernweg_voc=True)
        if not qry:
            for wrd in words:
                Words_user.objects.create(user=request.user, word=wrd)

        else:
            pass
        # [word.delete for word in Words_user.objects.filter(user=request.user, lernweg_voc=True)]


        # first_field = request.user.profile  # speichern Vocabel zum Beginnen ab
        # first_field.first_voc = voc_bits
        # first_field.save()
        #
        # last_field = request.user.profile   # speichern Vocabel zum Beenden ab
        # last_field.last_voc = voc_bits * 2
        # last_field.save()

    if first_voc != 0:
        words = Unit_words.objects.filter(unit_name_id=current_u)[first_voc:last_voc].filter()

        qry = Words_user.objects.filter(user=request.user, lernweg_voc=True)
        if not qry:
            for wrd in words:
                Words_user.objects.create(user=request.user, word=wrd)

        else:
            pass
        # [word.delete for word in Words_user.objects.filter(user=request.user, lernweg_voc=True)]


        # first_field = request.user.profile  # speichern Vocabel zum Beginnen ab
        # first_field.first_voc = first_voc + voc_bits
        # first_field.save()
        #
        # last_field = request.user.profile  # speichern Vocabel zum Beenden ab
        # last_field.last_voc = last_voc + voc_bits
        # last_field.save()


    context = {'info': current_u, 'words': words,
               'voc_bits': voc_bits}

    return render(request, 'users/users-lernweg-start.html', context)


@login_required
def lernweg_method(request):
    current_u = request.user.profile.current_unit
    if current_u == 0:  # das soll feststellen, dass wir von vorne anfangen
        return HttpResponse(":( Sorry, your site wasn't found. "
                            "Please try it at 'Lernweg'.")
    if current_u != 0:
        return render(request, 'users/users-lernweg-method.html', {})

    # if reqest.user.profile.user_zurueck == 1:
    #     return HttpResponse('Funktioniert, nun addieren')
    #
    # if reqest.user.profile.user_zurueck != 1:
    #     return HttpResponse('Reloaded! Nicht addieren!')


@login_required
def method_karteikarten(request):
    current_u = request.user.profile.current_unit
    if current_u == 0:  # das soll feststellen, dass wir von vorne anfangen
        return HttpResponse(":( Sorry, your site wasn't found. "
                            "Please try it at 'Lernweg'.")
    if current_u != 0:
        return render(request, 'users/users-method-karteikarten.html', {})


@login_required
def method_schriftlich(request):



        if request.method == 'POST':
            values_from_user = request.POST.getlist('my_list') # was der user im template in <input> eingegeben hat
            words_for_user = Words_user.objects.filter(user=request.user, fuer_pruefung=True, lernweg_voc=True)
            words_for_user_gereiht = []
            x = 1
            for wrd in words_for_user:
                word = Words_user.objects.get(user=request.user, pruefung_reihung=x)
                words_for_user_gereiht.append(word)
                x += 1

            for wrd_ital, wrd_user_eingabe in zip(words_for_user_gereiht, values_from_user):
                print(str(wrd_ital.word.italienisch) + ' soll das gleiche sein wie ' + wrd_user_eingabe)
                wrd_ital.date = date.today()
                wrd_ital.lernweg_voc = False
                # wrd_ital.fuer_pruefung = False
                wrd_ital.save()

                # print('für prüfung= ' + str(wrd_ital.fuer_pruefung))

                if str(wrd_ital.word.italienisch) == wrd_user_eingabe:
                    wrd_ital.right = True
                    wrd_ital.save()
                    print(wrd_ital.right)
                else:
                    wrd_ital.right = False
                    wrd_ital.save()
                    print(wrd_ital.right)

            print(Words_user.objects.filter(user=request.user, fuer_pruefung=True))

            range_it_words = words_for_user_gereiht

            for wrd_reihung in words_for_user_gereiht:
                wrd_reihung.pruefung_reihung = 0
                wrd_reihung.save()


        else:
            range_it_words = []  # für die Wörter, die angezeigt werden bei der Prüfung
            current_u = request.user.profile.current_unit
            first_voc = request.user.profile.first_voc
            last_voc = request.user.profile.last_voc
            voc_bits = request.user.profile.voc_bits
            pruefung_voc = request.user.profile.pruefung_voc

            if current_u == 0:  # das soll feststellen, dass wir von vorne anfangen
                return HttpResponse(":( Sorry, your site wasn't found. "
                                    "Please try it at 'Lernweg'.")
            if current_u != 0:
                if first_voc == 0:
                    # words = Unit_words.objects.filter(unit_name_id=current_u)[first_voc:voc_bits].filter()
                    words = Words_user.objects.filter(user=request.user, lernweg_voc=True)

                if first_voc != 0:
                    # words = Unit_words.objects.filter(unit_name_id=current_u)[first_voc:last_voc].filter()
                    words = Words_user.objects.filter(user=request.user, lernweg_voc=True)

            # words_for_user = Unit_words.objects.filter(words_user__user_id=request.user.id)[:pruefung_voc]

            if not words:
                if first_voc == 0:
                    profile_update = request.user.profile
                    profile_update.first_voc = voc_bits
                    profile_update.last_voc = voc_bits * 2
                    profile_update.save()
                if first_voc != 0:
                    profile_update = request.user.profile
                    profile_update.first_voc = first_voc + voc_bits
                    profile_update.last_voc = last_voc + voc_bits
                    profile_update.save()
                return redirect('users-lernweg')



            durchgaenge = 0
            pruefungslaenge = request.user.profile.pruefung_voc
            durchgaenge_error = 0

            while durchgaenge < pruefungslaenge:
                word_d = random.choice(words)
                range_it_words.append(word_d)

                if range_it_words.count(word_d) > 1:
                    # print(f'{word_d.deutsch} x {range_it_words.count(word.deutsch)}')
                    range_it_words.remove(word_d)
                    durchgaenge -= 1

                durchgaenge += 1
                durchgaenge_error += 1
                print(durchgaenge_error)
                if durchgaenge_error > 30:
                    # messages.error(request, f'Sorry {request.user}, dass das jetzt so lange gedauert hat! Das könnte unter anderem daran liegen, dass deine '
                    #                f'Prüfungslänge länger als die Länge der Unit ist. Setze eventuell die Prüfungslänge etwas kürzer.')
                    break


            x = 1
            for voc in range_it_words:
                voc.fuer_pruefung = True
                voc.pruefung_reihung = x
                voc.save()
                x += 1

            for vc in words:
                if vc.id not in [obj.id for obj in range_it_words]:
                    vc.fuer_pruefung = False
                    vc.save()

        context = {'words_italienisch': range_it_words}

        return render(request, 'users/users-method-schriftlich.html', context)


