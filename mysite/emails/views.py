import random

from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import render, HttpResponse, reverse, redirect
from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import get_template, render_to_string
from django.contrib.auth.decorators import login_required
from django.utils.html import strip_tags
from django.conf import settings

from .models import Confirm_email, Password_reset
from .forms import PasswordResetForm, PasswordForgotFrom, OldPasswordForm

def random_confirm():
    x = 0
    random_numbers = []
    while x < 100000:
        random_numbers.append(str(x))
        x += 1
    random_letters_lower = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r',
                            's',
                            't', 'u', 'v', 'w', 'x', 'y', 'z']
    random_letters_upper = [letter.upper() for letter in random_letters_lower]
    random_gesamt = []
    for a, b, c in zip(random_numbers, random_letters_lower, random_letters_upper):
        random_gesamt.append(a)
        random_gesamt.append(b)
        random_gesamt.append(c)
    random.shuffle(random_gesamt)
    confirm = ''
    rounds = 0
    while rounds < 1000:
        choice = random.choice(random_gesamt)
        confirm += choice
        rounds += 1
    return confirm

@login_required
def feedback(request):
    subject = 'First mail!'
    from_email = settings.EMAIL_HOST_USER
    recipient_list = ['maximilian-esternberg@gmx.at']

    html_message = render_to_string('emails/newsletter-start.html', {'request': request, 'link': 'https://www.youtube.com/watch?v=A-7vGF_pEss'})
    plain_message = strip_tags(html_message)
    send_mail(subject=subject, message=plain_message, from_email=from_email, recipient_list=recipient_list, html_message=html_message)
    # print(request.get_host)

    return HttpResponse('i hope it worked')

@login_required
def newsletter_unsubscribe(request, pk):
    pass


def newsletter_subscribe(reqest):
    pass






def register_success(subject, to, image, header, zeilen=[], body_bold=None, body_small=None, links={}, footers=['Freundliche Grüße', 'dein EasyLearn-Team'], body_bgcolor='#ffffff', text_color='#000000',
                     plain_message='Diese E-Mail ist kein Spam, du kannst sie aus dem Spam-Ornder herausziehen :)'):

    from_email = settings.EMAIL_HOST_USER

    # signup_message = 'hello my friends'
    # message = EmailMultiAlternatives(subject=subject, body=signup_message, from_email=from_email, to=recipient_list)
    # html_template = get_template('emails/register_success.html').render()
    # message.attach_alternative(html_template, 'text/html')
    # message.send()
    image_2 = 'https://nationalcareersweek.com/wp-content/uploads/2018/05/career-3386334_1920.jpg'



    html_message = render_to_string('emails/register_success.html',
                                    {'image': image, 'header': header, 'zeilen:': zeilen, 'body_bold': body_bold, 'body_small':body_small ,
                                     'links': links, 'footers': footers, 'body_background': body_bgcolor, 'text_color': text_color})


    send_mail(subject=subject, message=plain_message, from_email=from_email, recipient_list=to, html_message=html_message)

@login_required
def confirm_email(request, pk, random_confirm):
    if request.user.id != pk:
        messages.error(request, f'Das hat nicht geklappt. Du musst dich mit deinem eigenen Account anmelden <a href="{reverse("logout")}">Zum LogOut</a>')
    else:
        try:
            confirm_db = Confirm_email.objects.get(user=request.user)
        except:
            return redirect('units')

        if random_confirm != confirm_db.code:
            messages.error(request, f'Das ist nicht mehr der aktuelle Link. Verwende bitte den aktuellen oder <a href="{reverse("confirm-start")}">Erneut versuchen </a>')
        else:
            confirm_db.delete()
            messages.success(request, f'Danke fürs Bestätigen der E-Mail, {request.user}!')

    return redirect('units')

@login_required
def send_confirmation(request):
    user = request.user
    try:
        confirm_db = Confirm_email.objects.get(user=user)
    except:
        return redirect('/')

    confirm_db.delete()
    code = random_confirm()
    Confirm_email.objects.create(user=user, code=code)

    subject = 'Step By Step, ' + str(user) + '!'
    recipient_list = [user.email]
    image = 'https://workingnation.com/wp-content/uploads/2018/08/shutterstock_1046505673-1.jpg'
    header = 'Hey ' + str(user) + '!'
    zeilen = ['Du stehst am Anfang deiner Leiter', 'Bleib dran!']
    body_bold = 'Klicke'
    body_small = 'und bestätige deine E-Mail-Adresse!'
    # confirm_code = Confirm_email.objects.get(user=request.user)
    link1 = f'http://{request.META["HTTP_HOST"]}{reverse("confirm-email", args=[user.id, code])}'
    links = {link1: 'E-Mail bestätigen'}
    # print(request.get_path())
    register_success(subject, recipient_list, image, header, zeilen, body_bold, body_small, links, body_bgcolor='#72bdc2', text_color='#ffffff',
                     plain_message=f'Zum Bestätigen deiner E-Mail, klicke auf diesen Link: {link1}, oder schiebe diese E-Mail aus dem Spam-Ordner in den Posteingang')

    messages.success(request,
                     f'Die Bestätigungs-Email wurde versandt! <small class="text-muted">Email nicht erhalten? <a href="{reverse("confirm-start")}">Erneut versuchen </a></small>')
    return redirect('/')

def password_forgot(request):
    if request.user.is_authenticated:
        user = request.user
        print(user)
        reset_mail = Password_reset.objects.filter(user=user)
        print(reset_mail)
        if reset_mail:
            for mail in reset_mail:
                mail.delete()
        confirm_code = random_confirm()
        Password_reset.objects.create(user=user, code=confirm_code)

        subject = 'Dein Code fürs Passwort-Zurücksetzen'
        recipient_list = [user.email]
        image = 'https://png.pngtree.com/svg/20170512/1dfe28799c.png'
        header = 'Passwort zurücksetzen'
        zeilen = ['Hier ist dein Code', 'zum Zurücksetzen deines Passwortes']
        body_bold = 'Der Button'
        body_small = 'ist der Schlüssel zu deinem Glück! ;)'
        link1 = f'http://{request.META["HTTP_HOST"]}{reverse("password-reset", args=[user.id, confirm_code])}'
        links = {link1: 'Passwort zurücksetzen'}
        register_success(subject, recipient_list, image, header, zeilen, body_bold, body_small, links,
                         plain_message=f'Dein Code fürs Passwort Zurücksetzen bei EasyLearn (Schreck dich nicht, er ist ziemlich lang): {link1}.Falls diese E-Mail in deinem Spam-Ornder ist, kannst du sie in das normale Postfach verschieben.')

        messages.success(request,
                        f'Die E-Mail wurde versandt. <a href="{reverse("password-forgot")}">Nicht erhalten? </a>')
        return redirect('/')

    else: # wenn User nicht angemeldet
        if request.method == 'POST':
            form = PasswordResetForm(request.POST)
            if form.is_valid():
                email = form.cleaned_data.get('email')
                for found_user in User.objects.all():
                    if found_user.email == email:
                        print(found_user)
                        reset_mail = Password_reset.objects.filter(user=found_user)
                        if reset_mail:
                            for mail in reset_mail:
                                mail.delete()
                        confirm_code = random_confirm()
                        Password_reset.objects.create(user=found_user, code=confirm_code)

                        subject = 'Dein Code fürs Passwort-Zurücksetzen'
                        recipient_list = [found_user.email]
                        image = 'https://png.pngtree.com/svg/20170512/1dfe28799c.png'
                        header = 'Passwort zurücksetzen'
                        zeilen = ['Hier ist dein Code', 'zum Zurücksetzen deines Passwortes']
                        body_bold = 'Der Button'
                        body_small = 'ist der Schlüssel zu deinem Glück! ;)'
                        link1 = f'http://{request.META["HTTP_HOST"]}{reverse("password-reset", args=[found_user.id, confirm_code])}'
                        links = {link1: 'Passwort zurücksetzen'}
                        register_success(subject, recipient_list, image, header, zeilen, body_bold, body_small, links,
                                         plain_message=f'Dein Code fürs Passwort Zurücksetzen bei EasyLearn (Schreck dich nicht, er ist ziemlich lang): {link1}.Falls diese E-Mail in deinem Spam-Ornder ist, kannst du sie in das normale Postfach verschieben.')

                        messages.success(request, f'Die E-Mail wurde versandt. <a href="{reverse("password-forgot")}">Nicht erhalten? </a>')


            return redirect('/')
        else:
            form = PasswordResetForm()

            return render(request, 'emails/password-reset.html', {'form': form})

def password_reset(request, pk, random_confirm):
    if request.user.is_authenticated:
        user = request.user
        if request.user.pk != pk:
            messages.error(request,
                            f'Das hat nicht geklappt. Du musst dich mit deinem eigenen Account anmelden <a href="{reverse("logout")}">Zum Logout </a>')
            return redirect('/')

    else:
        user = User.objects.get(id=pk)

    try:
        code_db = Password_reset.objects.get(user=user)
    except:
        messages.error(request,
                       f'Dies ist nicht mehr der aktuelle link <a href="{reverse("password-forgot")}">Erneut versuchen</a>')
        return redirect('/')

    if code_db.code != random_confirm:
        messages.error(request, f'Dies ist nicht mehr der aktuelle link <a href="{reverse("password-forgot")}">Erneut versuchen</a>')
        return redirect('/')

    else:
        login(request, user)

        if request.method == 'POST':
            form = PasswordForgotFrom(request.POST, instance=user)
            if form.is_valid():
                password = form.cleaned_data.get('password1')
                user.set_password(password)
                user.save()
                code_db.delete()
                messages.success(request, 'Dein Passwort wurde erfolgreich geändert!')
                login(request, user)
                return redirect('units')
        else:
            form = PasswordForgotFrom()
        return render(request, 'emails/passwort-forgot.html', {'form': form})


@login_required
def new_password(request):
    user = request.user
    if request.method == 'POST':
        form = PasswordChangeForm(data=request.POST, user=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Dein Passwort wurde erfolgreich geändert!')
            return redirect('units')
    else:
        form = PasswordChangeForm(user=user)

    return render(request, 'emails/new-password.html', {'form': form})
