from mainapp.models import *
from django.shortcuts import get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.db.models import Count
from mainapp.forms import QuestionForm

def cities(request):
    specializations = Specialization.objects.annotate(num_subspecs=Count(
        'related')).filter(num_subspecs__gt=0).order_by('num_subspecs').reverse()
    all_specializations = Specialization.objects.all()
    cities = City.objects.all()
    city_slug = request.session.get('city', 'msk')
    if request.method == 'POST':
        question = QuestionForm(request.POST)
        if question.is_valid():
            new_question = question.save(commit=False)
            new_question.question = question.cleaned_data['question']
            new_question.phone_number = question.cleaned_data['phone_number']
            new_question.email = question.cleaned_data['email']
            new_question.save()
            # gainnet api start
            from django.conf import settings
            import requests
            gainnet_id = settings.GAINNET_API_ID
            gainnet_cities = {
                'msk': 'msk',
                'spb': 'spb',
                'kazan': 'kzn',
                'voronezh': 'vrj',
                'perm': 'prm',
                'stavropol': 'str',
                'belgorod': 'blg',
                'kemerovo': 'kemer',
                'samara': 'smr',
                'nsk':'novosib',
                'krasnodar': 'krs',
                'chel': 'chelyabinsk'
                }
            gainnet_url = 'https://gainnet.ru/api/v1/addlead'
            gainnet_data = {
                'id': gainnet_id,
                'phone': question.cleaned_data['phone_number'],
                'name': question.cleaned_data['email'],
                'text': question.cleaned_data['question'],
            }
            if city_slug in gainnet_cities.keys():
                gainnet_data['region'] = gainnet_cities[city_slug]
            try:
                gainnet_response = requests.post(gainnet_url, data=gainnet_data)
            except:
                pass
            # gainnet api end
        after_receive_message = 'Спасибо за ваш вопрос! Скоро юрист вам ответит по email или телефону'
    else:
        question = QuestionForm()
        after_receive_message = None
    try:
        main_city = City.objects.get(slug=city_slug)
    except:
        main_city = City.objects.get(slug='msk')
    if request.GET.get('city'):
        city_slug = request.GET.__getitem__('city')
        request.session['city'] = city_slug
        main_city = City.objects.get(slug=city_slug)
    return {
        "all_specializations": all_specializations,
        'city_slug': city_slug,
        'main_city': main_city,
        'cities': cities,
        'specializations': specializations,
        'question': question,
        'after_receive_message': after_receive_message,
    }
