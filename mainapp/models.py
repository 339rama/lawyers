from django.db import models
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.contrib.sessions.backends.db import SessionStore


class City(models.Model):
    name = models.CharField(max_length=128, verbose_name='Название города')
    slug = models.SlugField(max_length=128, db_index=True, unique=True, verbose_name='ЧПУ название города')
    city_names = models.TextField(blank=True, verbose_name='Падежи города')
    coords = models.CharField(max_length=128, blank=True, verbose_name='Координаты')

    class Meta:
        ordering = ['name']
        verbose_name = 'Город'
        verbose_name_plural = 'Города'
    
    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('mainapp:LawyersByCiy', args=[self.slug])

    def get_new_name(self):
        if self.name[-1] == 'ь':
            end = 'и'
        elif self.name[-1] == 'о':
            end = ''
        else:
            end = 'е'
        new_name = self.name[:-1] + end
        return new_name

class Specialization(models.Model):
    name = models.CharField(
        max_length=255, verbose_name='Название специализации')
    slug = models.SlugField(max_length=255, db_index=True,
                            unique=True, verbose_name='ЧПУ')
    related = models.ManyToManyField('self', symmetrical=False, related_name='related_specs', blank=True, verbose_name="Подспециализации")
    image = models.ImageField(upload_to='uploads/specializations', blank=True, verbose_name='Изображение специализации')

    class Meta:
        ordering = ['name']
        verbose_name = 'Специализация'
        verbose_name_plural = 'Специализации'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        city=None
        return reverse('mainapp:LawyersBySpecialization', args=[city, self.slug])

    def get_new_name(self):
        new_name = str()
        n = self.name.split(' ')
        if len(n) == 2:
            if n[0][-2:] =='ое':
                new_name += n[0][:-2] + 'ому '
                new_name += n[1][:-1] + 'y'
            elif n[0][-2:] == 'ий':
                new_name += n[0][:-2] + 'ому '
                new_name += n[1] + 'y'
            elif n[0][-2:] == 'ая':
                new_name += n[0][:-2] + 'ой '
                new_name += n[1][0:-1] + 'и'
            elif n[0][-1:] == 'л':
                new_name += n[0] + 'у ' + n[1]
        elif len(n) == 1:
            if n[0][-2:] == 'ие':
                new_name = n[0][:-2] + 'ию'
            elif n[0][-2:] == 'ия':
                new_name = n[0][:-2] + 'ии'
            elif n[0][-1:] == 'ы':
                new_name = n[0][:-1] + 'ам'
            elif n[0][-1:] == 'а':
                new_name = n[0][:-1] + 'е'
            elif n[0][-1:] == 'о':
                new_name = n[0][:-1] + 'у'
            else:
                new_name = self.name
        elif len(n) == 3:
            if n[0][-1:] == 'а':
                new_name += n[0][:-1] + 'е ' + n[1] + ' ' + n[2]
            if n[0][-2:] == 'ия':
                new_name += n[0][:-2] + 'ии ' + n[1] + ' ' + n[2]
            if n[0][-2:] == 'ие':
                new_name += n[0][:-2] + 'ию ' + n[1] + ' ' + n[2]
            if n[0][-1:] == 'ы':
                new_name = n[0][:-1] + 'ам ' + n[1] + ' ' +n[2][:-1] + 'ам' 
        else:
            new_name = self.name
        return new_name

    def image_tag(self):
        return mark_safe('<img src="/media/%s" width="150" height="150" style="object-fit: cover;"/>' % (self.image))

    image_tag.short_description = 'Изображение специализации'


class Lawyer(models.Model):
    lawyername = models.CharField(max_length=255, verbose_name='ФИО')
    major = models.CharField(max_length=128, blank=True, verbose_name='Специальность')
    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True)
    aboutself = models.TextField(blank=True, verbose_name='О себе')
    exp_year = models.CharField(max_length=5, verbose_name='Стаж/Опыт')
    image = models.ImageField(upload_to='uploads/lawyers/', blank=True, verbose_name='Изображение')
    rating = models.DecimalField(max_digits=3, decimal_places=1, blank=True, verbose_name='Рейтинг')
    education = models.TextField(blank=True, verbose_name='Образование')
    address = models.CharField(max_length=255, blank=True, verbose_name='Адрес')
    specializations = models.ManyToManyField(Specialization, related_name='specializations', blank=True, verbose_name='Специализации')

    class Meta:
        ordering = ['lawyername']
        verbose_name = 'Юрист'
        verbose_name_plural = 'Юристы'
    
    def __str__(self):
        return self.lawyername

    def get_absolute_url(self):
        return reverse('mainapp:LawyerPage', args=[self.id])


class Comment(models.Model):
    lawyer = models.ForeignKey(Lawyer, on_delete=models.CASCADE, related_name='comments', verbose_name='Юрист')
    author = models.CharField(max_length=255, verbose_name="Автор комментария")
    text = models.TextField(blank=True, verbose_name='Текст')

    class Meta:
        ordering = ['id']
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return self.author

