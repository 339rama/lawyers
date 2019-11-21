from django.contrib import admin
from .models import *

class LawyerAdmin(admin.ModelAdmin):
    list_display = ['lawyername', 'id', 'city']


class SpecializationAdmin(admin.ModelAdmin):
    list_display = ['name', 'id']
    prepopulated_fields = {'slug': ('name', )}
    fields = ['name', 'slug', 'related', 'image_tag', 'image']
    readonly_fields = ['image_tag']


class CityAdmin(admin.ModelAdmin):
    list_display = ['name', 'id']
    prepopulated_fields = {'slug': ('name', )}


class CommentAdmin(admin.ModelAdmin):
    list_display = ['author', 'id']

admin.site.register(Lawyer, LawyerAdmin)
admin.site.register(Specialization, SpecializationAdmin)
admin.site.register(City, CityAdmin)
admin.site.register(Comment, CommentAdmin)

