from django.contrib import admin
from .models import Category, Hotel, Room, User, ImageHotel, ImageRoom
from mptt.admin import DraggableMPTTAdmin


class ImageRoomInline(admin.TabularInline):
    model = ImageRoom
    extra = 5


class ImageHotelInline(admin.TabularInline):
    model = ImageHotel
    extra = 5


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'description', 'image_tag', 'status']
    list_filter = ['status']
    list_editable = ['status']
    list_display_links = ['title']
    readonly_fields = ['image_tag']


class CategoryAdmin2(DraggableMPTTAdmin):
    mptt_indent_field = "title"
    list_display = ('tree_actions', 'indented_title',
                    'related_products_count', 'related_products_cumulative_count')
    list_display_links = ('indented_title',)

    def get_queryset(self, request):
        qs = super().get_queryset(request)

        # Add cumulative product count
        qs = Category.objects.add_related_count(
            qs,
            Hotel,
            'category',
            'products_cumulative_count',
            cumulative=True)

        # Add non cumulative product count
        qs = Category.objects.add_related_count(qs,
                                                Hotel,
                                                'category',
                                                'products_count',
                                                cumulative=False)
        return qs

    def related_products_count(self, instance):
        return instance.products_count
    related_products_count.short_description = 'Related products (for this specific category)'

    def related_products_cumulative_count(self, instance):
        return instance.products_cumulative_count
    related_products_cumulative_count.short_description = 'Related products (in tree)'


class HotelAdmin(admin.ModelAdmin):
    list_display = ['title', 'category',
                    'country', 'city', 'user_id', 'image_tag', 'status']
    list_filter = ['category', 'country', 'city', 'status']
    list_editable = ['status']
    list_display_links = ['title']
    inlines = [ImageHotelInline]
    readonly_fields = ['image_tag']


class RoomAdmin(admin.ModelAdmin):
    list_display = ['title', 'hotel_id', 'price', 'image_tag', 'status']
    list_filter = ['price', 'status']
    list_editable = ['status']
    list_display_links = ['title']
    inlines = [ImageRoomInline]
    readonly_fields = ['image_tag']


class UserAdmin(admin.ModelAdmin):
    list_display = ['full_Name', 'role', 'status']
    list_filter = ['role', 'status']
    list_editable = ['status']
    list_display_links = ['full_Name']

    def full_Name(self, obj):
        return obj.name + ' ' + obj.surname


class ImageHotelAdmin(admin.ModelAdmin):
    list_display = ['title', 'hotel_id', 'image_tag']
    list_filter = ['hotel_id']
    readonly_fields = ['image_tag']


class ImageRoomAdmin(admin.ModelAdmin):
    list_display = ['title', 'room_id', 'image_tag']
    list_filter = ['room_id']
    readonly_fields = ['image_tag']


admin.site.register(Category, CategoryAdmin2)
admin.site.register(Hotel, HotelAdmin)
admin.site.register(Room, RoomAdmin)
admin.site.register(User, UserAdmin)
#admin.site.register(ImageHotel, ImageHotelAdmin)
#admin.site.register(ImageRoom, ImageRoomAdmin)
