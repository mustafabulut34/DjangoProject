from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField
# Create your models here.

from django.urls import reverse
from django.utils.safestring import mark_safe
from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel


STATUS = (
    ('True', 'True'),
    ('False', 'False'),
)


class Menu(MPTTModel):
    parent = TreeForeignKey('self', blank=True, null=True,
                            related_name='children', on_delete=models.CASCADE)
    title = models.CharField(max_length=100, unique=True)
    link = models.CharField(max_length=100, blank=True)

    status = models.CharField(max_length=5, choices=STATUS)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class MPTTMeta:
        level_attr = 'mptt_level'
        order_insertion_by = ['title']

    def __str__(self):
        full_path = [self.title]
        prnt = self.parent
        while prnt is not None:
            full_path.append(prnt.title)
            prnt = prnt.parent
        return ' -> '.join(full_path[::-1])


class Content(models.Model):
    TYPE = (
        ('Menu', 'Menu'),
        ('News', 'News'),
        ('Campaign', 'Campaign'),
        ('Announcement', 'Announcement'),
    )

    menu = models.OneToOneField(
        Menu, null=True, blank=True, on_delete=models.CASCADE)
    kind = models.CharField(max_length=15, choices=TYPE)
    title = models.CharField(max_length=150)
    keywords = models.CharField(blank=True, max_length=255)
    description = models.CharField(blank=True, max_length=255)
    image = models.ImageField(blank=True, null=True,
                              upload_to='images/content/')
    detail = RichTextUploadingField()
    slug = models.SlugField(null=False, unique=True)

    status = models.CharField(max_length=5, choices=STATUS)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def image_tag(self):
        return mark_safe('<img src="{}"height="50"/>'.format(self.image.url))
    image_tag.short_description = 'Image'

    def get_absolute_url(self):
        return reverse("content_detail", kwargs={"slug": self.slug})


class CImages(models.Model):
    content = models.ForeignKey(Content, on_delete=models.CASCADE)
    title = models.CharField(max_length=50, blank=True)
    image = models.ImageField(blank=True, upload_to='images/content/')

    def image_tag(self):
        return mark_safe('<img src="{}"height="50"/>'.format(self.image.url))
    image_tag.short_description = 'Image'
