from django.contrib import admin
from django.urls import path,  re_path
from django.conf.urls import url, include
from django.conf import settings
from django.conf.urls.static import static

from django.contrib.sitemaps.views import sitemap
from mainapp.sitemaps import *

sitemaps = {
    'statics': StaticSitemap,
	'cities': CitySitemap,
    'specs': SpecializationSitemap,
    'lawyers': LawyersSitemap,
}

urlpatterns = [
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    path('admin/', admin.site.urls),
    path('user/', include(('users.urls', 'users'), namespace='users')),
    path('', include(('mainapp.urls', 'mainapp'), namespace='mainapp')),
    
]


if settings.DEBUG:
    import debug_toolbar
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += path('__debug__/', include(debug_toolbar.urls)),
