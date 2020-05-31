from django.db import models
from django.utils.html import mark_safe
from django.forms import ModelForm, TextInput, Textarea, EmailInput, NumberInput
from django.contrib.auth.models import User
from ckeditor_uploader.fields import RichTextUploadingField
from mptt.models import MPTTModel, TreeForeignKey

from django.urls import reverse
STATUS = (
    ('True', 'True'),
    ('False', 'False'),
)


class Category(MPTTModel):
    title = models.CharField(max_length=30)
    keywords = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    image = models.ImageField(blank=True, upload_to='images/category/')
    status = models.CharField(max_length=10, choices=STATUS)
    slug = models.SlugField(null=False, unique=True)
    parent = TreeForeignKey(
        'self', blank=True, null=True, related_name='children', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class MPTTMeta:
        level_attr = 'mptt_level'
        order_insertion_by = ['title']

    def __str__(self):
        cat = [self.title]
        prnt = self.parent
        while prnt is not None:
            cat.append(prnt.title)
            prnt = prnt.parent
        return ' -> '.join(cat[::-1])

    def image_tag(self):
        return mark_safe('<img src="{}" height="50"/>'.format(self.image.url))
    image_tag.short_description = 'Image'

    def get_absolute_url(self):
        return reverse("category_detail", kwargs={"slug": self.slug})


class Hotel(models.Model):
    STAR = (
        (1, 1),
        (2, 2),
        (3, 3),
        (4, 4),
        (5, 5),
    )
    title = models.CharField(max_length=30)
    keywords = models.CharField(max_length=255)
    description = RichTextUploadingField()
    image = models.ImageField(blank=True, upload_to='images/hotel/')
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    star = models.IntegerField(blank=True, choices=STAR)
    address = models.CharField(max_length=80)
    city = models.CharField(max_length=20)
    country = models.CharField(max_length=20)
    location = models.CharField(max_length=20)
    phone = models.CharField(max_length=20)
    fax = models.CharField(max_length=20)
    email = models.EmailField()
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=STATUS)
    slug = models.SlugField(null=False, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def image_tag(self):
        return mark_safe('<img src="{}" height="50"/>'.format(self.image.url))
    image_tag.short_description = 'Image'

    def get_absolute_url(self):
        return reverse("hotel", kwargs={"id": self.id, "slug": self.slug})


class Room(models.Model):
    hotel_id = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    title = models.CharField(max_length=30)
    keywords = models.CharField(max_length=255)
    description = RichTextUploadingField()
    image = models.ImageField(blank=True, upload_to='images/room/')
    price = models.IntegerField(blank=False)
    status = models.CharField(blank=True, max_length=5, choices=STATUS)
    count = models.IntegerField(blank=False)
    slug = models.SlugField(null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def image_tag(self):
        return mark_safe('<img src="{}" height="50"/>'.format(self.image.url))
    image_tag.short_description = 'Image'

    def get_absolute_url(self):
        return reverse("room", kwargs={"id": self.id, "hotelslug": self.hotel_id.slug, "roomslug": self.slug})

    def category(self):
        return self.hotel_id.category


class Comment(models.Model):
    COMMENT_STATUS = (
        ('New', 'New'),
        ('True', 'True'),
        ('False', 'False'),
    )
    comment = models.CharField(max_length=255, blank=True)
    subject = models.CharField(max_length=50, blank=True)
    rate = models.IntegerField()
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ip = models.CharField(max_length=20)
    status = models.CharField(max_length=10,
                              blank=True, choices=COMMENT_STATUS, default='New')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ('rate', 'subject', 'comment')
        widgets = {
            'rate': NumberInput(attrs={'class': 'form-control', 'min': 1, 'max': 5, 'placeholder': 'Rate'}),
            'subject': TextInput(attrs={'class': 'form-control', 'placeholder': 'Subject'}),
            'comment': Textarea(attrs={'class': 'form-control', 'placeholder': 'Comment', 'rows': '5'}),
        }


class ImageHotel(models.Model):
    hotel_id = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    title = models.CharField(blank=True, max_length=30)
    image = models.ImageField(blank=False, upload_to='images/hotel/')

    def __str__(self):
        return self.title

    def image_tag(self):
        return mark_safe('<img src="{}" height="50"/>'.format(self.image.url))
    image_tag.short_description = 'Image'


class ImageRoom(models.Model):
    room_id = models.ForeignKey(Room, on_delete=models.CASCADE)
    title = models.CharField(blank=True, max_length=30)
    image = models.ImageField(blank=False, upload_to='images/room/')

    def __str__(self):
        return self.title

    def image_tag(self):
        return mark_safe('<img src="{}" height="50"/>'.format(self.image.url))
    image_tag.short_description = 'Image'
