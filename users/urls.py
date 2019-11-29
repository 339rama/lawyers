from django.conf.urls import url
from django.urls import path, re_path
from users import views, forms

urlpatterns = [
    re_path(r'^register/$', forms.RegisterFormView.as_view(), name='Register'),
    path('confirm/<uuid>' , views.ConfirmEmail, name='ConfirmEmail'),
    re_path(r'^login/$', forms.LoginFormView.as_view(), name='Login'),
]
