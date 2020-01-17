from django.contrib import admin
from .models import *


class LawyerCommentInlines(admin.TabularInline):
    model = Comment

class LawyerAdmin(admin.ModelAdmin):
    inlines = [LawyerCommentInlines]
    list_display = ['id', 'lawyername', 'city', 'sorting', 'get_specializations']
    list_editable = ['lawyername', 'city', 'sorting']
    list_filter = ['city']
    search_fields = ['lawyername', 'id', 'city', 'get_specializations']


class SpecializationAdmin(admin.ModelAdmin):
    list_display = ['name', 'id']
    prepopulated_fields = {'slug': ('name', )}
    fields = ['name','name_form', 'slug', 'related', 'image_tag', 'image']
    readonly_fields = ['image_tag']


class CityAdmin(admin.ModelAdmin):
    list_display = ['name', 'id']
    prepopulated_fields = {'slug': ('name', )}


class CommentAdmin(admin.ModelAdmin):
    list_display = ['author', 'id']


class QuestionAdmin(admin.ModelAdmin):
    list_display = ['email', 'phone_number']

admin.site.register(Lawyer, LawyerAdmin)
admin.site.register(Specialization, SpecializationAdmin)
admin.site.register(City, CityAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Question, QuestionAdmin)

