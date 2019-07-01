import random
from datetime import date

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.shortcuts import redirect

from users.models import Words_user
from units.models import Unit_words

class LernwegGet(LoginRequiredMixin):
    words_right_false = {}
    choices = [True, False]

    def __init__(self, request, words, range=None, lernweg=False):     #bei Words unbedingt Djnago Query einsetzen und bei range int!
        self.request = request
        self.user = request.user
        self.words = words
        self.words_id = [word.id for word in words]
        random.shuffle(self.words_id)
        self.range = range
        self.lernweg = lernweg

        if self.range:
            self.words_id = self.words_id[:self.range]

    def mix_schriftlich(self):
        self.words_right_false = {}

        for word_id in self.words_id:
            word_real = self.words.get(id=word_id)

            if self.user.profile.pruefung_umgekehrt:
                self.words_right_false[word_real.id] = {random.choice(self.choices): word_real}
            else:
                self.words_right_false[word_real.id] = {False: word_real}

        return self.words_right_false

    def mix_karteikarten(self):

        print('Range: {}'.format(self.range))
        print('Wörter: {}'.format(self.words_id))
        self.words_right_false = {}
        # if self.lernweg == True:
        #     words_real_id = [word.word.id for word in Words_user.objects.filter(id__in=self.words_id)]
        #     selection = [word.word.id for word in Words_user.objects.filter(id__in=[word.id for word in self.words])]
        #     self.words_id = Unit_words.objects.filter(id__in=words_real_id)




        for word in self.words_id:
            key = self.words.get(id=word)
            if self.lernweg == True:
                word = Unit_words.objects.get(id=key.word.id).id
                selection = [word.word.id for word in
                             Words_user.objects.filter(id__in=[word.id for word in self.words])]


                # selection.append(word)
                # random.shuffle(selection)
            else:
                selection = [wrd.id for wrd in self.words]


            random.shuffle(selection)
            selection.remove(word)
            selection = selection[:self.user.profile.karteikarten_voc-1]    #damit das richtige Wort auch hinzugefügt werden kann

            selection.append(word)
            random.shuffle(selection)
            if self.lernweg == True:
                if len(selection) < self.user.profile.karteikarten_voc:
                    if self.lernweg == True:
                        other_words = Unit_words.objects.filter(unit_name_id=self.user.profile.current_unit)[
                self.user.profile.first_voc:self.user.profile.last_voc].filter()
                        for wrd in other_words:
                            if wrd.id not in selection:
                                if len(selection) < self.user.profile.karteikarten_voc:
                                    selection.append(wrd.id)

            # print(str(len(selection)) + '--' + str(self.user.profile.karteikarten_voc))

            if len(selection) < self.user.profile.karteikarten_voc:
                if self.lernweg:
                    for wrd in Unit_words.objects.filter(unit_name=key.word.unit_name):
                        if wrd.id not in selection:

                            if len(selection) < self.user.profile.karteikarten_voc:
                                selection.append(wrd.id)
                else:
                    for wrd in Unit_words.objects.filter(unit_name=key.unit_name):
                        if wrd.id not in selection:
                            if len(selection) < self.user.profile.karteikarten_voc:
                                selection.append(wrd.id)



            if self.lernweg == False:
                if self.user.profile.pruefung_umgekehrt:
                    self.words_right_false[key.id] = {key: {random.choice(self.choices): [self.words.get(id=sel_id) for sel_id in selection]}}
                else:
                    self.words_right_false[key.id] = {key: {False: [self.words.get(id=sel_id) for sel_id in selection]}}
            else:
                if self.user.profile.pruefung_umgekehrt:
                    self.words_right_false[key.id] = {key: {random.choice(self.choices): [Unit_words.objects.get(id=sel_id) for sel_id in selection]}}
                else:
                    self.words_right_false[key.id] = {key: {False: [Unit_words.objects.get(id=sel_id) for sel_id in selection]}}

        return self.words_right_false

class LernwegPost(LoginRequiredMixin):
    words_right_false = {}

    def __init__(self, request, words, save=False, redirect_url='users-lernweg'):
        self.request = request
        self.user = request.user
        self.words = words
        self.save = save
        self.redirect_url = redirect_url

        self.values_from_user = {}

        for key, value in self.request.POST.items():
            lst = key.split('-')
            if len(lst) == 2:
                self.values_from_user[lst[1]] = {lst[0]: value}


    def handle_karteikarten(self):
        self.words_right_false = {}
        for keys, values in self.values_from_user.items():
            try:
                word_database = self.words.get(id=keys)
            except: #das ist ein absichtlicher DoesNotExist-Error: wenn der User einen zweiten Tab aufmacht und dort versucht, ein Wort ein zweites Mal zu prüfen
                messages.error(request=self.request, message='Diese Anfrage wurde nicht genehmigt, schummeln funktioniert bei uns nicht ;)')
                return redirect(self.redirect_url)

            for key, value in values.items(): # der zweite key hat nur Bedeutung bei schriftlich, da dort geschaut wird ob auch umgekehrt geprüft wird
                #   (von Fremdsprache auf Deutsch), hier ist er nur zur Vereinheitlichung des Inputs da, weil hier nur die IDs verglichen werden
                if self.save:
                    if str(self.words.get(id=int(keys)).word.id) == value:
                        self.words_right_false[word_database] = {key: 'right'}
                        word_database.right = True
                    else:
                        self.words_right_false[word_database] = {key: 'false'}
                        word_database.right = False

                    word_database.date = date.today()
                    word_database.lernweg_voc = False
                    word_database.save()
                else:   #wenn es nicht gespeichert werden soll, z.B. Unit-Test
                    if keys == value:
                        self.words_right_false[word_database] = {key: 'right'}
                    else:
                        self.words_right_false[word_database] = {key: 'false'}

        return self.words_right_false



    def handle_schriftlich(self):   #wichtig: nur Words_unit - Instances (keine Words_user oderso)
        self.words_right_false = {}
        for keys, values in self.values_from_user.items():
            try:
                word_database = self.words.get(id=keys)
            except: #das ist ein absichtlicher DoesNotExist-Error: wenn der User einen zweiten Tab aufmacht und dort versucht, ein Wort ein zweites Mal zu prüfen
                messages.error(request=self.request, message='Diese Anfrage wurde nicht genehmigt, schummeln funktioniert bei uns nicht ;)')
                return redirect(self.redirect_url)

            print(word_database)
            for key, value in values.items():
                if self.save:
                    if key == 'False':  #wenn key == 'False' bedeutet, dass das Wort nicht umgekehrt ist!
                        if str(word_database.word.italienisch) == value:
                            self.words_right_false[word_database] = {key: 'right'}
                            word_database.right = True
                        else:
                            self.words_right_false[word_database] = {key: 'false'}
                            word_database.right = False
                    else:
                        if str(word_database.word.deutsch) == value:
                            self.words_right_false[word_database] = {key: 'right'}
                            word_database.right = True
                        else:
                            self.words_right_false[word_database] = {key: 'false'}
                            word_database.right = False

                    word_database.date = date.today()
                    word_database.lernweg_voc = False
                    word_database.save()

                else:   #wenn Words nicht gespeichert werden, braucht man nicht Words_user_instance, sondern Words_unit inststance
                    if key == 'False':
                        if str(word_database.italienisch) == value:
                            self.words_right_false[word_database] = {key: 'right'}
                        else:
                            self.words_right_false[word_database] = {key: 'false'}
                    else:
                        if str(word_database.deutsch) == value:
                            self.words_right_false[word_database] = {key: 'right'}
                        else:
                            self.words_right_false[word_database] = {key: 'false'}

        return self.words_right_false
