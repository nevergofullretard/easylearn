from django.urls import path
from .views import ChartData1, GetData, user_statistics, ChartData3, ChartData4, ChartData5, ChartData6, statistics_unit, units_all, delete_unit

urlpatterns = [
    path('', view=user_statistics, name='statistics-home'),
    path('api/data/', GetData.as_view(), name='api-data'),   # api-data
    path('api/chart1/data/', ChartData1.as_view()),
    # path('api/chart2/data/', ChartData2.as_view()),
    path('api/chart3/data/', ChartData3.as_view()),
    path('api/chart4/data/', ChartData4.as_view()),
    path('api/chart5/data/', ChartData5.as_view()),
    path('api/<int:pk>/<name_of_unit>/data/', ChartData6.as_view()),
    path('unit/<int:pk>/<name_of_unit>/', view=statistics_unit, name='statistic-units'),
    # path('units/<name_of_unit>/right'),
    path('units/all/', view=units_all,  name='statistics_units_all'),
    path('reset/unit/<int:pk>/<name_of_unit>/', delete_unit, name='delete-unit'),
]