from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()


@register.filter
@stringfilter
def feedbacks_count(value):
    value = int(value)
    if value == 1 or (value > 20 and int(list(str(value))[-1]) == 1):
        value = 'отзыв'
    elif 1 < value < 5 or (value > 20 and 1 < int(list(str(value))[-1]) < 5):
        value = 'отзыва'
    else:
        value = 'отзывов'
    return value


def result_count(value):
    value = int(value)
    if value == 1 or (value > 20 and int(list(str(value))[-1]) == 1):
        value = 'результат'
    elif 1 < value < 5 or (value > 20 and 1 < int(list(str(value))[-1]) < 5):
        value = 'результата'
    else:
        value = 'результатов'
    return value

def my_random(values, number):
    import random
    output = list()
    for x in range(0,int(number)):
        output.append(random.choice(values))
    return output
    

register.filter('feedbacks_count', feedbacks_count)
register.filter('result_count', result_count)
register.filter('my_random', my_random)
