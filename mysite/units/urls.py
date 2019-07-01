from django.urls import path
from . import views
from .models import Unit_name


urlpatterns = [
    path('', views.units, name='units'),
    path('unit/<int:pk>/<name_of_unit>/', views.unitname, name='unit-words', kwargs=None),
    path('units/all', view=views.units_all, name='units-all'),
    path('words/new/', views.new_words, name='new-words'),
    path('words/new/unit', views.new_words_user, name='new-words-user'),
    path('words/new/words/', views.new_unit_user, name='new-unit-user'),
    path('words/new/start', views.new_words_start, name='new-words-start'),
    path('words/new/school', views.new_school, name='new-school'),
    path('words/new/lang', views.new_lang, name='new-lang'),
    path('anfragen/words/', views.anfragen, name='anfragen'),
    path('anfragen/sonstige/', views.anfragen_rest, name='anfragen-sonstige'),
    path('dashboard/', views. dashboard, name='dashboard'),
    path('units/unit/<int:schule_pk>/<int:sprache_pk>/', views.schule_sprache_unit, name='schule_sprache_units'),
]

# for unit in Unit_name.objects.all():
#     urlpatterns.append(path('<name_of_unit>', views.unitname, name=unit))