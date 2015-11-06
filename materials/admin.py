from __future__ import unicode_literals

from django.contrib import admin

from .models import Category, Material, Statistic, Vote


def make_thumbs(modeladmin, request, queryset):
    for obj in queryset:
        obj.make_thumbs()
make_thumbs.short_description = "Make thumbs to selected"


class SlugAdmin(admin.ModelAdmin):
    prepopulated_fields = {
        'slug': ('name',),
    }


class MaterialAdmin(SlugAdmin):
    list_display = ('name', 'pk', 'category', 'engine', 'user', 'storage_name', 'downloads')
    list_filter = ('engine', 'category')
    search_fields = ('name',)
    fieldsets = (
        (None, {
            'fields': (('name', 'slug'), 'description', ('engine', 'category'), ('user'))
        }),
        ('Publish', {
            'classes': ('collapse',),
            'fields': ('date', 'draft', 'downloads')
        }),
        ('Files', {
            'classes': ('collapse',),
            'fields': ('image', 'thumb_big', 'thumb_medium', 'thumb_small', 'storage', 'storage_name'),
        }),
    )
    readonly_fields = ('downloads',)
    actions = [make_thumbs]


class StatisticAdmin(admin.ModelAdmin):
    list_display = ('date', 'material', 'count')
    list_filter = ('date', 'material')
    list_per_page = 25


admin.site.register(Category, SlugAdmin)
admin.site.register(Material, MaterialAdmin)
admin.site.register(Statistic, StatisticAdmin)
admin.site.register(Vote)
