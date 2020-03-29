from django.contrib import admin
from .models import Category, Hotel, Room, User, ImageHotel, ImageRoom


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


class HotelAdmin(admin.ModelAdmin):
    list_display = ['title', 'category_id',
                    'country', 'city', 'user_id', 'image_tag', 'status']
    list_filter = ['category_id', 'country', 'city', 'status']
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


admin.site.register(Category, CategoryAdmin)
admin.site.register(Hotel, HotelAdmin)
admin.site.register(Room, RoomAdmin)
admin.site.register(User, UserAdmin)
#admin.site.register(ImageHotel, ImageHotelAdmin)
#admin.site.register(ImageRoom, ImageRoomAdmin)
