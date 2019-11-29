from django.conf.urls import url
from django.urls import path, re_path
from mainapp import views

urlpatterns =[
    re_path(r'^$', views.Index, name='Index'),
    re_path(r'^lawyer/(?P<lawyer_id>\d+)/', views.LawyerPage, name='LawyerPage'),
    path('<str:city>/', views.LawyersByCity, name='LawyersByCity'),
    path('<str:city>/<str:filter_spec>/', views.LawyersBySpecialization, name='LawyersBySpecialization'),
    
]
