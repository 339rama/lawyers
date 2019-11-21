from django.conf.urls import url
from django.urls import path
from users import views

urlpatterns = [
    path('confirm/<uuid>' , views.ConfirmEmail, name='ConfirmEmail'),
]
