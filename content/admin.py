from django.contrib import admin

from mptt.admin import DraggableMPTTAdmin

from .models import CImages, Menu, Content
# Register your models here.


class ContentImageInline(admin.TabularInline):
    model = CImages
    extra = 3


class MenuContentInline(admin.TabularInline):
    model = Content
    extra = 3


class ContentAdmin(admin.ModelAdmin):
    list_display = ['title', 'kind', 'image_tag', 'status', 'created_at']
    list_filter = ['status', 'kind']
    inlines = [ContentImageInline]
    prepopulated_fields = {'slug': ('title',)}
    list_editable = ['status']


class MenuAdmin(DraggableMPTTAdmin):
    mptt_indent_field = "title"
    list_display = ('tree_actions', 'indented_title', 'status')
    inlines = [MenuContentInline]
    list_editable = ['status']


admin.site.register(Menu, MenuAdmin)
admin.site.register(Content, ContentAdmin)
