# Generated by Django 2.2.6 on 2019-11-01 07:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='specialization',
            name='image',
            field=models.ImageField(blank=True, upload_to='uploads/specializations', verbose_name='Изображение специализации'),
        ),
    ]
