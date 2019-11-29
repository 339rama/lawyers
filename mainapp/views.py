from django.shortcuts import render, get_object_or_404, get_list_or_404, redirect
from .models import *
import json
from django.db.models import Count

def Index(request):
    if request.GET.get('lat'):
        from django.conf import settings
        from geopy.geocoders import Yandex
        from django.http import HttpResponse, JsonResponse
        import json
        geo = Yandex(api_key=settings.YANDEX_MAP_TOKEN)
        lat = request.GET.__getitem__('lat')
        lng = request.GET.__getitem__('lng')
        city_name = geo.reverse(
            (lat, lng), exactly_one=True, timeout=5, kind="locality").address.split(', ')[0]
        try:
            city_slug = City.objects.get(name=city_name).slug
            request.session['city'] = city_slug
        except:
            pass
        return HttpResponse(json.dumps({'city_slug': city_slug, 'city_name': city_name}, ensure_ascii=False), content_type='application/json')
    else:
        # specializations = Specialization.objects.annotate(num_subspecs = Count('related')).filter(num_subspecs__gt=0).order_by('num_subspecs').reverse()
        return render(request, 'index.html')

def LawyersByCity(request, city):
    # request.session['city'] = city
    show_num = 5
    city = get_object_or_404(City, slug=city)
    results_count = Lawyer.objects.filter(city=city).count()
    try:
        city_where = json.loads(city.city_names.replace("'",'"'))['city7']
    except:
        city_where = json.loads(city.city_names.replace("'", '"'))['city1']
    if request.GET.get('show'):
        show_num = request.GET.__getitem__('show')
        lawyers = Lawyer.objects.filter(city=city)[(int(show_num)-5):int(show_num)].annotate(num_comments=Count('comments'))
        return render(request, 'lawyers_shown.html', {'lawyers': lawyers,})
    else:
        lawyers = Lawyer.objects.filter(city=city)[:show_num].annotate(num_comments=Count('comments'))
        cities = City.objects.all()

        title = "Адвокаты и юристы в городе " + city.name
        meta = "Ищите юристов и адвокатов в " + city_where + "? На странице собраны все юристы и компании, которые оказывают услуги в городе " + \
            city_where + ". В базе собрано 1000 юристов. Вы можете получить бесплатную консультацию по своему вопросу от юриста и адвоката."
        h1 = "Адвокаты и юристы в " + city_where
        h1text = "На сайте собраны контакты юристов, их условия работы и специализация. Выбирайте нужного специалиста и начинайте работу!"

        return render(request, 'city.html', {
            'city': city,
            'lawyers': lawyers,
            'cities': cities,
            'results_count': results_count,
            'title': title,
            "meta": meta,
            "h1": h1,
            "h1text": h1text,
            'spec_new_name': specialization.get_new_name().lower(),
        })


def LawyersBySpecialization(request, city, filter_spec):
    # city = request.session.get('city', 'msk')
    specialization = get_object_or_404(Specialization, slug=filter_spec)
    lawyers = Lawyer.objects.filter(specializations=specialization, city__slug=city)[:5].annotate(num_comments=Count('comments'))
    city = get_object_or_404(City, slug=city)
    results_count = Lawyer.objects.filter(specializations=specialization, city=city).count()
    try:
        city_where = json.loads(city.city_names.replace("'", '"'))['city7']
    except:
        city_where = json.loads(city.city_names.replace("'", '"'))['city1']
    if request.GET.get('show'):
        show_num = request.GET.__getitem__('show')
        lawyers = Lawyer.objects.filter(city=city)[(int(show_num)-5):int(show_num)].annotate(num_comments=Count('comments'))
        return render(request, 'lawyers_shown.html', {'lawyers': lawyers,})
    else:
        title = "Адвокаты и юристы по "+ specialization.get_new_name().lower() + " в городе " + city.name + " : отзывы, рейтинг, каталог, бесплатно и платно"
        meta = "Ищите адвокатов по " + specialization.get_new_name().lower() + " в " + city_where + " ? На странице собраны все юристы и компании, которые оказывают услуги в городе " + \
            city.name + " . В базе собрано 1000 юристов. На сайте можно получить бесплатную консультацию."
        h1 = "Адвокаты и юристы по " + specialization.get_new_name().lower() + " в " + city_where
        h1text = "Здесь вы можете найти юриста для решения своей задачи, получить консультацию, получить ответ на вопрос."

        return render(request, 'city.html', {
            'city': city,
            'specialization': specialization,
            'lawyers': lawyers,
            'results_count': results_count,
            'title': title,
            "meta": meta,
            "h1": h1,
            "h1text": h1text,
            'spec_new_name': specialization.get_new_name().lower(),
        })

def LawyerPage(request, lawyer_id):
    lawyer = get_object_or_404(Lawyer, id=lawyer_id)
    comments = Comment.objects.filter(lawyer=lawyer_id)
    return render(request, 'lawyer_page.html', {
        'lawyer': lawyer,
        'comments': comments,
    })
