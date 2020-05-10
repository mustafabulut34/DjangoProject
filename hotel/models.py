from django.db import models
from django.utils.html import mark_safe
from django.forms import ModelForm, TextInput, Textarea, EmailInput, NumberInput
from django.contrib.auth.models import User
from ckeditor_uploader.fields import RichTextUploadingField
from mptt.models import MPTTModel, TreeForeignKey

STATUS = (
    ('True', 'Evet'),
    ('False', 'Hayır'),
)


class Category(MPTTModel):
    title = models.CharField(max_length=30)
    keywords = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    image = models.ImageField(blank=True, upload_to='images/')
    status = models.CharField(max_length=10, choices=STATUS)
    slug = models.SlugField()
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


class Hotel(models.Model):
    STAR = (
        ('One', '1'),
        ('Two', '2'),
        ('Three', '3'),
        ('Four', '4'),
        ('Five', '5'),
    )
    title = models.CharField(max_length=30)
    keywords = models.CharField(max_length=255)
    description = RichTextUploadingField()
    image = models.ImageField(blank=True, upload_to='images/')
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    star = models.CharField(blank=True, max_length=10, choices=STAR)
    address = models.CharField(max_length=80)
    city = models.CharField(max_length=20)
    country = models.CharField(max_length=20)
    location = models.CharField(max_length=20)
    phone = models.CharField(max_length=20)
    fax = models.CharField(max_length=20)
    email = models.EmailField()
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=STATUS)
    slug = models.SlugField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def image_tag(self):
        return mark_safe('<img src="{}" height="50"/>'.format(self.image.url))
    image_tag.short_description = 'Image'


class Room(models.Model):
    hotel_id = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    title = models.CharField(max_length=30)
    description = RichTextUploadingField()
    image = models.ImageField(blank=True, upload_to='images/')
    price = models.IntegerField(blank=False)
    status = models.CharField(blank=True, max_length=5, choices=STATUS)
    slug = models.SlugField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def image_tag(self):
        return mark_safe('<img src="{}" height="50"/>'.format(self.image.url))
    image_tag.short_description = 'Image'


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
    image = models.ImageField(blank=False, upload_to='images/')

    def __str__(self):
        return self.title

    def image_tag(self):
        return mark_safe('<img src="{}" height="50"/>'.format(self.image.url))
    image_tag.short_description = 'Image'


class ImageRoom(models.Model):
    room_id = models.ForeignKey(Room, on_delete=models.CASCADE)
    title = models.CharField(blank=True, max_length=30)
    image = models.ImageField(blank=False, upload_to='images/')

    def __str__(self):
        return self.title

    def image_tag(self):
        return mark_safe('<img src="{}" height="50"/>'.format(self.image.url))
    image_tag.short_description = 'Image'
