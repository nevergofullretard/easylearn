from django.contrib import admin
from .models import People, Unit_words, Unit_name, Unit_sprache, Unit_schule, Anfrage_words_user, Anfrage_schule, Anfrage_sprache, Anfrage_unit

admin.site.register(People)

admin.site.register(Unit_words)
admin.site.register(Unit_name)
admin.site.register(Unit_schule)
admin.site.register(Unit_sprache)
admin.site.register(Anfrage_words_user)
admin.site.register(Anfrage_schule)
admin.site.register(Anfrage_sprache)
admin.site.register(Anfrage_unit)



