from django.contrib import admin

from .models import Upload, Scene


def publish(modeladmin, request, queryset):
    for obj in queryset:
        obj.publish()
publish.short_description = "Publish selected Uploads"


class UploadAdmin(admin.ModelAdmin):
    list_display = ('name', 'engine', 'scene', 'date', 'author', 'status', 'category', 'user_approved', 'admin_approved')
    list_filter = ('status', 'engine')
    fieldsets = (
        ('Upload', {
            'fields': ('name', 'description', ('engine', 'scene'), ('uploaded_file', 'name_in_file'), ('date', 'author')),
        }),
        ('Render', {
            'classes': ('collapse',),
            'fields': ('status', ('render_started', 'render_finished'), 'error', 'storage', 'image')
        }),
        ('Publishing', {
            'classes': ('collapse',),
            'fields': ('category', 'user_approved', 'admin_approved'),
        }),
    )
    actions = [publish]


admin.site.register(Upload, UploadAdmin)
admin.site.register(Scene)