from django.urls import path
from .views import fehlertest, fehlertest_karteikarten, fehlertest_schriftlich, unittest_start, unittest_schriftlich, unittest_karteikarten, unittest_method, \
    fehlertest_start, fehlertest_zwischenschritt


urlpatterns = [
    path('test/<test_art>/<von>/<bis>/<unit_ids>/', view=fehlertest, name='fehlertest-start'),
    path('test/karteikarten/<test_art>/<von>/<bis>/<unit_ids>/', fehlertest_karteikarten, name='fehlertest-karteikarten'),
    path('test/schriftlich/<test_art>/<von>/<bis>/<unit_ids>/', fehlertest_schriftlich, name='fehlertest-schriftlich'),
    path('unittest/start/', unittest_start, name='unittest-start'),
    path('unittest/method/<int:pk>/<name_of_unit>', unittest_method, name='unittest-method'),
    path('unittest/schriftlich/<int:pk>/<name_of_unit>/', unittest_schriftlich, name='unittest-schriftlich'),
    path('unittest/karteikarten/<int:pk>/<name_of_unit>/', unittest_karteikarten, name='unittest-karteikarten'),
    path('test/start/', fehlertest_start, name='fehlertest-start-really'),
    path('test/<test_art>/detection/<von>/<bis>/<unit_ids>/', fehlertest_zwischenschritt, name='test-zwischenschritt'),

]