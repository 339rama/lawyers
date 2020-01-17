from django.contrib.sitemaps import Sitemap
from .models import City, Specialization, Lawyer
from django.urls import reverse

class StaticSitemap(Sitemap):
    priority = 0.6
    changefreq = 'never'

    def items(self):
        return ['mainapp:Index',]

    def location(self, item):
        return reverse(item)

class CitySitemap(Sitemap):
    changefreq = "never"
    priority = 0.5

    def items(self):
        return City.objects.all()


class SpecializationSitemap(Sitemap):
    changefreq = "never"
    priority = 0.5

    def items(self):
        spec_list = list()
        for city in City.objects.all():
            for spec in Specialization.objects.all():
                spec_list.append([city.slug, spec.slug])
        return spec_list
        

    def location(self, item):
        return reverse('mainapp:LawyersBySpecialization', args=item)


class LawyersSitemap(Sitemap):
    changefreq = "never"
    priority = 0.5

    def items(self):
        return Lawyer.objects.all().order_by('id')

