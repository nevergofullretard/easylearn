from datetime import date # für Statistik, damit ich weiß wann das Vocabel geprüft wurde
from collections import Counter
import random


from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import DeleteView
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login # für automatischen Login nach Register und beim Login
from django.shortcuts import render, redirect, HttpResponse, reverse
from django.contrib import messages
from django.core.exceptions import ValidationError

from usertests.lernweg import LernwegGet, LernwegPost
from blog.models import Post
from units.models import Unit_words, Unit_name, Unit_schule, Unit_sprache # ich weiß nicht warum es mir das anzeigt, aber alles funktioniert anscheinend normal
from usertests.models import Unit_pruefung
from emails.views import register_success, random_confirm
from units.views import split_list
from emails.models import Confirm_email

from .forms import UserRegisterForm, UserUpdateForm, SchriftlichPruefungItForm,\
    SchriftlichePruefungDeuForm, PruefungForm, LoginForm, ImageForm, ToleranzForm
from .models import Pruefung_voc
from .models import Profile, Words_user, Units_user


''' Der nächste import ist für den User zum auswählen welche Unit er als nächstes machen möchte'''
from django import forms


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
                return HttpResponseRedirect(request.META.get('HTTP_REFERER','/'))

            except AttributeError:
                messages.error(request, f"Sorry {username}, aber diese Daten stimmen nicht, versuche es nochmal!")
                return redirect('login')


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


            user = request.user


            confirm_emails = Confirm_email.objects.filter(user=user)
            if confirm_emails.count() > 0:
                for email in confirm_emails:
                    email.remove()

            user = request.user
            subject = 'Willkommen im Club, ' + str(user) + '!'
            recipient_list = [user.email]
            image = 'https://pngimage.net/wp-content/uploads/2018/06/step-by-step-png-2.png'
            header = 'Hey ' + str(user) + '!'
            zeilen = ['Danke dass du dich registriert hast!', 'Sei gespannt auf kommende Neuigkeiten!']
            body_bold = 'Starte durch'
            body_small = 'und besuche die Website!'
            confirm_code = random_confirm()
            link1 = f'http://{request.META["HTTP_HOST"]}{reverse("confirm-email", args=[user.id, confirm_code])}'
            links = {link1: 'E-Mail bestätigen'}
            # print(request.get_path())
            register_success(subject, recipient_list, image, header, zeilen, body_bold, body_small, links, plain_message=f'Hallo {user}! Danke dass du dich registriert hast! Zum Bestätigen deiner E-Mail, klicke auf diesen Link: {link1}, '
                             f'oder schiebe diese E-Mail aus dem Spam-Ordner in den Posteingang')


            post_title = f'Hallo @{user} ! Klick auf mich! - Dein Admin'
            post_content = 'Das ist der Community-Sektor. Hier kannst du Posts schreiben und bearbeiten, Freunde markieren, den Feed durchlesen und vieles mehr! Schau dich um!'
            welcome_post = Post.objects.create(title=post_title, content=post_content, author=User.objects.get(id=1))
            welcome_post.linked.set([user])



            Confirm_email.objects.create(user=user, code=confirm_code)


            return redirect('users-start')
    else:
        form = UserRegisterForm()

    return render(request, 'users/register.html', {'form': form})



@login_required
def profile(request):
    if request.method == 'POST':
        # profile_form = UserProfileForm(request.POST, instance=request.user.profile)
        pruefung_form = PruefungForm(request.POST, instance=request.user.profile)
        image_form = ImageForm(request.POST, request.FILES, instance=request.user.profile)
        toleranz_form = ToleranzForm(request.POST, instance=request.user.profile)

        if pruefung_form.is_valid() and image_form.is_valid() and toleranz_form.is_valid():
            pruefung_form.save()
            image_form.save()
            toleranz_form.save()

            messages.success(request, f'Dein Profil wurde erfolgreich geändert!')

        return redirect('profile')

    else:
        # u_form = UserUpdateForm(instance=request.user)
        # profile_form = UserProfileForm(instance=request.user)
        pruefung_form = PruefungForm(instance=request.user.profile)
        image_form = ImageForm(instance=request.user.profile)
        toleranz_form = ToleranzForm(instance=request.user.profile)
    context = {
        'pruefung_form': pruefung_form, 'image_form': image_form, 'toleranz_form': toleranz_form,
    }

    return render(request, 'users/profile.html', context)


def start(request):
    if request.user.is_authenticated:
        context = {'username': request.user}
        return render(request, 'users/users-start.html', context)
    else:
        return redirect('about')



def units_auswahl(request, nur_volle_units=True, nur_alle=False):
    current_unit = None
    next = None
    similar = None
    alle_dict = {}
    units_gemacht = []
    dict_units_gemacht = {}

    if not nur_alle:
        if request.user.profile.current_unit2:
            current_unit = request.user.profile.current_unit2



        for wrd in Words_user.objects.filter(user=request.user, lernweg_voc=False)[::-1]:
            if wrd.word.unit_name not in units_gemacht:
                units_gemacht.append(wrd.word.unit_name)
        # units_gemacht = Units_user.objects.filter(user=request.user)[::-1]

        if units_gemacht and not current_unit:
            letzte_unit = units_gemacht[0]
        elif units_gemacht and current_unit:
            letzte_unit = current_unit

        if units_gemacht:
            real_units_gemacht = [unit.id for unit in units_gemacht]
            naechste_untit = \
                Unit_name.objects.filter(sprache=letzte_unit.sprache, schule=letzte_unit.schule).exclude(
                    id__in=real_units_gemacht)
            if naechste_untit:
                lst_naechste_unit = []
                # print('nächste Units')
                # print(lst_naechste_unit)
                if nur_volle_units:
                    for naechste in naechste_untit:
                        words_naechste_unit = Unit_words.objects.filter(unit_name=naechste)
                        if words_naechste_unit:
                            lst_naechste_unit.append(naechste)
                else:
                    lst_naechste_unit = [unit for unit in naechste_untit]
                print('nächste Units')
                print(lst_naechste_unit)

                if not current_unit:
                    next = naechste_untit[0]
                    # if nur_volle_units == False:
                    #     lst_naechste_unit.append(naechste_untit[1])
                else:
                    next = None
                    # if nur_volle_units == False:
                    #     lst_naechste_unit.append(naechste_untit[1])


                print('next: ' + str(next))

                # similar = naechste_untit.exclude(id=next.id)
                if next in lst_naechste_unit:
                    lst_naechste_unit.remove(next)
                if current_unit in lst_naechste_unit:
                    lst_naechste_unit.remove(current_unit)


                # print(lst_naechste_unit)
                # if lst_naechste_unit:

                similar = lst_naechste_unit
                if next:
                    real_units_gemacht.append(next.id)

                if nur_volle_units == True:
                    if not Unit_words.objects.filter(unit_name=next):
                        next = None
            if similar and current_unit:
                alle_units = Unit_name.objects.all().exclude(id__in=real_units_gemacht).exclude(id__in=[unit.id for unit in similar]).exclude(id=current_unit.id)
            elif similar:
                alle_units = Unit_name.objects.all().exclude(id__in=real_units_gemacht).exclude(
                    id__in=[unit.id for unit in similar])
            elif current_unit:
                alle_units = Unit_name.objects.all().exclude(id__in=real_units_gemacht).exclude(id=current_unit.id)
            else:
                alle_units = Unit_name.objects.all().exclude(id__in=real_units_gemacht)


        else:
            alle_units = Unit_name.objects.all()

        print(alle_units)


        for schule in Unit_schule.objects.all():
            units_schule = alle_units.filter(schule=schule)
            schule_words = Unit_words.objects.filter(unit_name__in=units_schule)
            if nur_volle_units:
                if units_schule and schule_words:
                    alle_dict[schule] = {}

                    for sprache in Unit_sprache.objects.all():
                        units_schule_sprache = units_schule.filter(sprache=sprache)
                        units_schule_sprache_all = []
                        for schule_sprache in units_schule_sprache:

                            if Unit_words.objects.filter(unit_name__id=schule_sprache.id):
                                units_schule_sprache_all.append(schule_sprache)

                                alle_dict[schule][schule_sprache.sprache] = split_list(units_schule_sprache_all)

            else:
                if units_schule:
                    alle_dict[schule] = {}
                    for sprache in Unit_sprache.objects.all():
                        units_schule_sprache = units_schule.filter(sprache=sprache)
                        units_schule_sprache_all = []
                        for schule_sprache in units_schule_sprache:
                            print('auch leere Units erlaubt')
                            units_schule_sprache_all.append(schule_sprache)
                            alle_dict[schule][schule_sprache.sprache] = split_list(units_schule_sprache_all)


        if current_unit in units_gemacht:
            units_gemacht.remove(current_unit)

        for unit in units_gemacht:
            words_unit = Words_user.objects.filter(user=request.user, word__unit_name=unit, lernweg_voc=False).order_by(
                "-date")
            outstanding_words = []
            all_words_unit = Unit_words.objects.filter(unit_name=unit)
            for wrd in all_words_unit:
                if wrd not in [wrd.word for wrd in words_unit]:
                    outstanding_words.append(wrd)
            if outstanding_words:
                dict_units_gemacht[unit] = outstanding_words
            else:
                dict_units_gemacht[unit] = None


    else:
        alle_units = Unit_name.objects.all()

        for schule in Unit_schule.objects.all():
            units_schule = alle_units.filter(schule=schule)
            schule_words = Unit_words.objects.filter(unit_name__in=units_schule)

            if units_schule and schule_words:
                alle_dict[schule] = {}

                for sprache in Unit_sprache.objects.all():
                    units_schule_sprache = units_schule.filter(sprache=sprache)
                    units_schule_sprache_all = []
                    for schule_sprache in units_schule_sprache:
                        if nur_volle_units:
                            if Unit_words.objects.filter(unit_name__id=schule_sprache.id):
                                units_schule_sprache_all.append(schule_sprache)

                                alle_dict[schule][schule_sprache.sprache] = split_list(units_schule_sprache_all)
                        else:
                            units_schule_sprache_all.append(schule_sprache)
                            alle_dict[schule][schule_sprache.sprache] = split_list(units_schule_sprache_all)

    # if nur_volle_units == False:
        # if similar:
        #     similar = split_list(similar)


    # if dict_units_gemacht:
    #     dict_units_gemacht = split_list(dict_units_gemacht)


    # if similar:
        #     print(similar)
        # similar = split_list(similar)
    print(alle_units)

    return {'current_unit': current_unit, 'next': next, 'similar': similar, 'alle': alle_dict, 'dict_units_gemacht': dict_units_gemacht}


@login_required
def lernweg(request):
    current_u = request.user.profile.current_unit2

    if not current_u:
        if request.method == 'POST':
            new_unit = request.POST.get('unit')
            real_new_unit = Unit_name.objects.get(id=new_unit)


            words_unit = Words_user.objects.filter(user=request.user, word__unit_name=real_new_unit,
                                                   lernweg_voc=False).order_by(
                "-date")
            if words_unit:
                outstanding_words = []
                all_words_unit = Unit_words.objects.filter(unit_name=real_new_unit)
                for wrd in all_words_unit:
                    if wrd not in [wrd.word for wrd in words_unit]:
                        outstanding_words.append(wrd)
                if not outstanding_words:
                    Words_user.objects.filter(user=request.user, word__unit_name=real_new_unit).delete()


            unit_update = request.user.profile
            unit_update.current_unit = new_unit
            unit_update.current_unit2 = real_new_unit
            unit_update.save()



            return redirect('users-lernweg')

        else:
            auswahl = units_auswahl(request=request, nur_volle_units=True)
        context = {'naechste_unit': auswahl['next'], 'similar': auswahl['similar'], 'alle': auswahl['alle'], 'units_gemacht': auswahl['dict_units_gemacht']}
        return render(request, 'users/users-neuer-lernweg.html', context)

    else:
        current_unit = current_u

        voc_bits = request.user.profile.voc_bits
        first_voc = request.user.profile.first_voc
        last_voc = request.user.profile.last_voc


        #z.B.: <QuerySet [<Unit_words: la casa>]>
        qry = Words_user.objects.filter(user=request.user, lernweg_voc=True, word__unit_name=current_unit)

        new_words_or_unit_finished(request, qry, current_u)



        words = [word.word for word in qry]


        context = {'info': current_unit, 'words': words,
                   'voc_bits': voc_bits}
    return render(request, 'users/users-lernweg-start.html', context)


def new_words_or_unit_finished(request, words_user, current_u):
    voc_bits = request.user.profile.voc_bits
    first_voc = request.user.profile.first_voc
    last_voc = request.user.profile.last_voc
    group_number = request.user.profile.group_number
    print(group_number)
    try:
        current_unit = current_u
    except:  # wenn current_u beim profile = 0
        return redirect('users-lernweg')


    #.exclude(id__in=[word_user.id for word_user in Words_user.objects.filter(user=request.user, word__unit_name=current_unit)])
    # print('hier kommen die Wörter:')
    # print(words)
    words = Unit_words.objects.filter(unit_name=current_u)

    words_now = Words_user.objects.filter(user=request.user, word__unit_name=current_unit)
    if not words_now:   #wenn noch gar keine Voc von Unit in Words_user sind
        user_profile = request.user.profile
        user_profile.group_number = group_number + 1
        user_profile.save()
        for wrd in words[:voc_bits]:
            Words_user.objects.create(user=request.user, word=wrd, group=group_number +1)


    if not words_user:  #=lernweg_voc=True
        print('keine Wörter')
        # if first_voc == 0 and last_voc == 0:
        words_neu = Unit_words.objects.filter(unit_name=current_u).exclude(id__in=[word.word.id for word in words_now])[:voc_bits]
        # print(words_new)
        # print(len(words_new))
        # print(len(Unit_words.objects.filter(unit_name_id=current_u)))
        # words_neu = Unit_words.objects.filter(unit_name_id=current_u)[last_voc: last_voc+voc_bits]
        # else:
        #     words_neu = Unit_words.objects.filter(unit_name_id=current_u)[first_voc+voc_bits:last_voc+voc_bits]

        print(words_neu)
        # unit_update = request.user.profile
        # unit_update.last_voc = voc_bits
        # unit_update.save()
        if not words_neu: #Wörter des nächsten Durchgangs im Lernweg
            print('unit fertig')
            # if not Units_user.objects.filter(user=request.user, unit=current_unit): #nur zur Sicherheit Filter
            # Units_user.objects.create(user=request.user, unit=current_unit)

            messages.success(request,
                             f'Du bist fertig mit {current_unit}! <a href="{reverse("statistic-units", args=[current_unit.id, current_unit])}">Zur Statistik</a>')
            unit_update = request.user.profile
            unit_update.current_unit = 0
            unit_update.current_unit2 = None
            unit_update.first_voc = 0
            unit_update.last_voc = 0
            unit_update.save()
        else: # wenn schon noch Wörter in der betreffenden Unit drin sind
            print('neue Wörter')

            profile_update = request.user.profile
            profile_update.first_voc = last_voc
            profile_update.last_voc = last_voc + voc_bits
            profile_update.group_number = group_number + 1
            profile_update.save()
            # if not Words_user.objects.filter(user=request.user, word__in=words):
            for wrd in words_neu:
                Words_user.objects.create(user=request.user, word=wrd, group=group_number+1)

        all_words = []

        # for word in words: # negative indexing not supported
        #     print(word)
        #     print(request.user.profile.group_number)
        #     print(group_number)
        #     real = Words_user.objects.get(user=request.user, word=word, group=group_number)
        #     all_words.append(real)

        all_words = Words_user.objects.filter(user=request.user, word__in=words, group=group_number)
        print('all words: ' + str(all_words))


        return all_words

@login_required
def method_karteikarten(request):
    current_u = request.user.profile.current_unit2
    words = Words_user.objects.filter(user=request.user, lernweg_voc=True, word__unit_name=current_u)

    if not current_u:  # das soll feststellen, dass wir von vorne anfangen
        return redirect('users-lernweg')
    else:
        words_right_false = None


        if request.method == "POST":
            lernweg_post = LernwegPost(request,words, save=True)
            words_right_false = lernweg_post.handle_karteikarten()


        else:
            lernweg = LernwegGet(request, words, request.user.profile.pruefung_voc, lernweg=True)
            words_right_false = lernweg.mix_karteikarten()

        to_learnweg_start = new_words_or_unit_finished(request, words, current_u)
        print('to lernweg-start')
        print(to_learnweg_start)

        context = {'words_right_false': words_right_false, 'to_learnweg_start': to_learnweg_start}
        return render(request, 'users/users-method-karteikarten.html', context)


@login_required
def method_schriftlich(request):
    current_u = request.user.profile.current_unit2
    words_right_false = None

    words = Words_user.objects.filter(user=request.user, lernweg_voc=True, word__unit_name=current_u)


    if request.method == 'POST':
        lernweg_post = LernwegPost(request, Words_user.objects.filter(user=request.user, lernweg_voc=True), save=True)
        words_right_false = lernweg_post.handle_schriftlich()
        print(words_right_false)

        words = Words_user.objects.filter(user=request.user, lernweg_voc=True)
        print(words)


    else:
        if not current_u:  # hier konnte man ein redirect einbauen
            return redirect('users-lernweg')
        else:
            lernweg = LernwegGet(request, words, request.user.profile.pruefung_voc)
            words_right_false = lernweg.mix_schriftlich()

    to_learnweg_start = new_words_or_unit_finished(request, words, current_u)
    print(to_learnweg_start)

    context = {'words_right_false': words_right_false, 'to_learnweg_start': to_learnweg_start}

    return render(request, 'users/users-method-schriftlich.html', context)




class AccountDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = User
    template_name = 'users/delete_account.html'

    def get_success_url(self):
        return reverse('units')

    def test_func(self):
        user = self.get_object()
        print(user.id)
        if self.request.user == user:
            return True
        return False

@login_required
def cancel_unit(request):
    current_unit = request.user.profile.current_unit2
    if not current_unit:  # dont know if this is necessary
        return redirect('users-lernweg')
    else:
        current_unit_real = current_unit

        if request.method == 'POST':
            # for word in Words_user.objects.filter(user=request.user, word__unit_name=current_unit_real):
            #     word.delete()
            user_profile = request.user.profile
            user_profile.current_unit = 0
            user_profile.first_voc = 0
            user_profile.current_unit2 = None
            user_profile.last_voc = 0
            user_profile.save()
            messages.error(request, f'Unit {current_unit_real} wurde abgebrochen. Du kannst sie später wieder weitermachen')
            return redirect('users-lernweg')


    return render(request, 'users/cancel-unit.html', {'unit': current_unit_real})

