from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField
from django.forms import ModelForm, TextInput, EmailInput, Textarea


STATUS = (
    ('True', 'True'),
    ('False', 'False'),
)


class Setting(models.Model):
    title = models.CharField(max_length=200)
    keywords = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    company = models.CharField(max_length=80)
    address = models.CharField(max_length=255, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    fax = models.CharField(max_length=20, blank=True)
    email = models.EmailField()
    smtpserver = models.CharField(max_length=255, blank=True)
    smtpemail = models.EmailField(blank=True)
    smtppassword = models.CharField(max_length=50, blank=True)
    smtpport = models.IntegerField(blank=True, null=True)
    image = models.ImageField(blank=True, upload_to='images/setting/')
    facebook = models.CharField(max_length=80, blank=True)
    instagram = models.CharField(max_length=80, blank=True)
    twitter = models.CharField(max_length=80, blank=True)
    aboutus = RichTextUploadingField()
    contact = RichTextUploadingField()
    references = RichTextUploadingField()
    status = models.CharField(blank=True, max_length=5, choices=STATUS)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class ContactFormMessage(models.Model):
    STATUS = {
        ('New', 'New'),
        ('Read', 'Read'),
        ('Closed', 'Closed')
    }
    name = models.CharField(blank=False, max_length=20)
    email = models.CharField(blank=False, max_length=50)
    subject = models.CharField(blank=False, max_length=50)
    message = models.TextField(blank=False, max_length=255)
    status = models.CharField(
        blank=True, max_length=10, choices=STATUS, default='New')
    ip = models.CharField(blank=True, max_length=20)
    note = models.CharField(blank=True, max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class ContactForm(ModelForm):
    class Meta:
        model = ContactFormMessage
        fields = ('name', 'email', 'subject', 'message')
        widgets = {
            'name': TextInput(attrs={'class': 'form-control', 'placeholder': 'Name & Surname'}),
            'subject': TextInput(attrs={'class': 'form-control', 'placeholder': 'Subject'}),
            'email': EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email Address'}),
            'message': Textarea(attrs={'class': 'form-control', 'placeholder': 'Your Message', 'rows': '5'}),

        }


class Faq(models.Model):
    ordernumber = models.IntegerField()
    question = models.TextField(max_length=255)
    answer = models.TextField()
    status = models.CharField(max_length=10, choices=STATUS)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.question
