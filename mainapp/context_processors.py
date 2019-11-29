from mainapp.models import *
from django.shortcuts import get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.db.models import Count

def cities(request):
    specializations = Specialization.objects.annotate(num_subspecs=Count(
        'related')).filter(num_subspecs__gt=0).order_by('num_subspecs').reverse()
    all_specializations = Specialization.objects.all()
    cities = City.objects.all()
    city_slug = request.session.get('city', 'msk')
    try:
        main_city = City.objects.get(slug=city_slug)
    except:
        main_city = City.objects.get(slug='msk')
    if request.GET.get('city'):
        print('get');
        city_slug = request.GET.__getitem__('city')
        print(city_slug)
        request.session['city'] = city_slug
        main_city = City.objects.get(slug=city_slug)
    return {
        "all_specializations": all_specializations,
        'city_slug': city_slug,
        'main_city': main_city,
        'cities': cities,
        'specializations': specializations,
    }
