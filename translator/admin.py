# -*- coding: utf-8 -*-
from django.conf import settings
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from modeltranslation.admin import TranslationAdmin

from translator.models import Translation

TAGS_SEPARATOR = getattr(settings, 'DJANGO_TRANSLATOR_CATEGORY_SEPARATOR', '___')
CATEGORY_SEPARATOR = getattr(settings, 'DJANGO_TRANSLATOR_CATEGORY_SEPARATOR', '__')


class KeyFilter(admin.SimpleListFilter):
    title = _('Categories')
    parameter_name = 'keys'

    def lookups(self, request, model_admin):
        queryset = model_admin.model.objects.filter(key__contains=CATEGORY_SEPARATOR).values_list('key', flat=True)
        clean_keys = [key[key.find(TAGS_SEPARATOR) + len(TAGS_SEPARATOR):] for key in queryset if TAGS_SEPARATOR in key]

        unique_categories = {key.split(CATEGORY_SEPARATOR)[0] for key in clean_keys}
        categories = sorted([key for key in unique_categories])
        return (
            (category, category) for category in categories
        )

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(key__startswith=self.value())
        else:
            return queryset


class TranslationAdministration(TranslationAdmin):
    list_filter = (KeyFilter, 'tags',)
    search_fields = ['key', 'description', 'tags']
    ordering = ('key',)
    list_display = ('key', 'description', 'tags')
    list_editable = ('description', 'tags')


admin.site.register(Translation, TranslationAdministration)
