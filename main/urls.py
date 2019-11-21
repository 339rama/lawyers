from django.contrib import admin
from django.urls import path,  re_path
from django.conf.urls import url, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(('mainapp.urls', 'mainapp'), namespace='mainapp')),
    path('user/', include(('users.urls', 'users'), namespace='users')),
]


if settings.DEBUG:
    import debug_toolbar
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += path('__debug__/', include(debug_toolbar.urls)),
