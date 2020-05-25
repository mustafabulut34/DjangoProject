from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField
from ckeditor.widgets import CKEditorWidget
# Create your models here.
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.safestring import mark_safe
from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel
from django.forms import ModelForm, TextInput, Select, FileInput


STATUS = (
    ('True', 'True'),
    ('False', 'False'),
)

TYPE = (
    ('Menu', 'Menu'),
    ('Campaign', 'Campaign'),
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
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
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


class ContentForm(ModelForm):
    class Meta:
        model = Content
        fields = ['kind', 'title', 'keywords',
                  'description', 'image', 'detail', 'slug']
        widgets = {
            'title': TextInput(attrs={'class': 'form-control', 'placeholder': 'Title'}),
            'slug': TextInput(attrs={'class': 'form-control', 'placeholder': 'Slug'}),
            'keywords': TextInput(attrs={'class': 'form-control', 'placeholder': 'Keywords'}),
            'description': TextInput(attrs={'class': 'form-control', 'placeholder': 'Description'}),
            'kind': Select(attrs={'class': 'form-control', 'placeholder': 'Kind'}, choices=TYPE),
            'image': FileInput(attrs={'class': 'form-control', 'placeholder': 'Image'}),
            'detail': CKEditorWidget(),
        }


class CImages(models.Model):
    content = models.ForeignKey(Content, on_delete=models.CASCADE)
    title = models.CharField(max_length=50, blank=True)
    image = models.ImageField(blank=True, upload_to='images/content/')

    def __str__(self):
        return self.title

    def image_tag(self):
        return mark_safe('<img src="{}"height="50"/>'.format(self.image.url))
    image_tag.short_description = 'Image'


class CImagesForm(ModelForm):
    class Meta:
        model = CImages
        fields = ['title', 'image']
