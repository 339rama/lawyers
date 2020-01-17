from django.shortcuts import render, get_object_or_404, get_list_or_404, redirect
from .models import *
import json
from django.db.models import Count

def Index(request):
    # # 
    # from django.contrib.sites.shortcuts import get_current_site
    # current_site = get_current_site(request)
    # for city in City.objects.all():
    #     with open('links.txt', 'a', encoding='utf-8') as file:
    #         file.write('https://'+current_site.domain+city.get_absolute_url()+'\n')

    # for city in City.objects.all():
    #         for spec in Specialization.objects.all():
    #             with open('links.txt', 'a', encoding='utf-8') as file:
    #                 file.write('https://'+current_site.domain+reverse('mainapp:LawyersBySpecialization', args=[city.slug, spec.slug])+'\n')

    # for lawyer in Lawyer.objects.all().order_by('id'):
    #     with open('links.txt', 'a', encoding='utf-8') as file:
    #         file.write('https://'+current_site.domain+lawyer.get_absolute_url()+'\n')
    # # 
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
    show_num = 10
    city = get_object_or_404(City, slug=city)
    results_count = Lawyer.objects.filter(city=city).count()
    import math
    pages = math.ceil(results_count/show_num)
    page = 1
    try:
        city_where = json.loads(city.city_names.replace("'",'"'))['city7']
    except:
        city_where = json.loads(city.city_names.replace("'", '"'))['city1']
    title = "Адвокаты и юристы в городе " + city.name
    meta = "Ищите юристов и адвокатов в " + city_where + "? На странице собраны все юристы и компании, которые оказывают услуги в городе " + \
        city_where + ". В базе собрано " + str(results_count) + " юристов. Вы можете получить бесплатную консультацию по своему вопросу от юриста и адвоката."
    h1 = "Адвокаты и юристы в " + city_where
    h1text = "На сайте собраны контакты юристов, их условия работы и специализация. Выбирайте нужного специалиста и начинайте работу!"
    if request.GET.get('show'):
        show_num = int(request.GET.__getitem__('show')) + 1
        lawyers = Lawyer.objects.filter(city=city).annotate(
            num_comments=Count('comments')).order_by('-sorting', 'num_comments').reverse()[(int(show_num)-10):int(show_num)]
        return render(request, 'lawyers_shown.html', {'lawyers': lawyers,})
    elif request.GET.get('page'):
        page = int(request.GET.__getitem__('page'))
        lawyers = Lawyer.objects.filter(city=city).annotate(
            num_comments=Count('comments')).order_by('-sorting', 'num_comments').reverse()[show_num*page-show_num:show_num*page]
        return render(request, 'city.html', {
            'city': city,
            'lawyers': lawyers,
            'results_count': results_count,
            'title': title,
            "meta": meta,
            "h1": h1,
            "h1text": h1text,
            "pages": pages,
            "page":page,
        })
    else:
        lawyers = Lawyer.objects.filter(city=city).annotate(
            num_comments=Count('comments')).order_by('-sorting', 'num_comments').reverse()[:show_num]

        return render(request, 'city.html', {
            'city': city,
            'lawyers': lawyers,
            'results_count': results_count,
            'title': title,
            "meta": meta,
            "h1": h1,
            "h1text": h1text,
            "pages": pages,
            "page": page,
        })


def LawyersBySpecialization(request, city, filter_spec):
    # city = request.session.get('city', 'msk')
    show_num = 10
    specialization = get_object_or_404(Specialization, slug=filter_spec)
    lawyers = Lawyer.objects.filter(specializations=specialization, city__slug=city).annotate(
        num_comments=Count('comments')).order_by('-sorting', 'num_comments').reverse()[:show_num]
    city = get_object_or_404(City, slug=city)
    results_count = Lawyer.objects.filter(specializations=specialization, city=city).count()
    import math
    pages = math.ceil(results_count/show_num)
    page = 1
    try:
        city_where = json.loads(city.city_names.replace("'", '"'))['city7']
    except:
        city_where = json.loads(city.city_names.replace("'", '"'))['city1']
    title = "Адвокаты и юристы по "+ specialization.name_form.lower() + " в городе " + city.name + ": отзывы, рейтинг, каталог, бесплатно и платно"
    meta = "Ищите адвокатов по " + specialization.name_form.lower() + " в " + city_where + "? На странице собраны все юристы и компании, которые оказывают услуги в городе " + \
        city.name + ". В базе собрано " + str(results_count) + " юристов. На сайте можно получить бесплатную консультацию."
    h1 = "Адвокаты и юристы по " + specialization.name_form.lower() + " в " + city_where
    h1text = "Здесь вы можете найти юриста для решения своей задачи, получить консультацию, получить ответ на вопрос."
    if request.GET.get('show'):
        show_num = int(request.GET.__getitem__('show')) + 1
        lawyers = Lawyer.objects.filter(specializations=specialization, city=city).annotate(
            num_comments=Count('comments')).order_by('-sorting', 'num_comments').reverse()[(int(show_num)-10):int(show_num)]
        return render(request, 'lawyers_shown.html', {'lawyers': lawyers,})
    elif request.GET.get('page'):
        page = int(request.GET.__getitem__('page'))
        lawyers = Lawyer.objects.filter(specializations=specialization, city=city).annotate(
            num_comments=Count('comments')).order_by('-sorting', 'num_comments').reverse()[show_num*page-show_num:show_num*page]
        return render(request, 'city.html', {
            'city': city,
            'specialization': specialization,
            'lawyers': lawyers,
            'results_count': results_count,
            'title': title,
            "meta": meta,
            "h1": h1,
            "h1text": h1text,
            'spec_new_name': specialization.name_form.lower(),
            "pages": pages,
            "page": page,
        })
    else:
        return render(request, 'city.html', {
            'city': city,
            'specialization': specialization,
            'lawyers': lawyers,
            'results_count': results_count,
            'title': title,
            "meta": meta,
            "h1": h1,
            "h1text": h1text,
            'spec_new_name': specialization.name_form.lower(),
            "pages": pages,
            "page": page,
        })

def LawyerPage(request, lawyer_id):
    lawyer = get_object_or_404(Lawyer, id=lawyer_id)
    comments = Comment.objects.filter(lawyer=lawyer_id)
    lawyer_specs = Specialization.objects.filter(specializations=lawyer)
    lawyers = Lawyer.objects.filter(specializations__in=lawyer_specs, city__slug=lawyer.city.slug).exclude(id=lawyer_id).annotate(
        num_comments=Count('comments')).order_by('num_comments').reverse()[:4]
    return render(request, 'lawyer_page.html', {
        'lawyer': lawyer,
        'comments': comments,
        'lawyers': lawyers,
    })

