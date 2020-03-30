from django.db import models

STATUS = (
    ('True', 'Evet'),
    ('False', 'Hayır'),
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
    image = models.ImageField(blank=True, upload_to='images/')
    facebook = models.CharField(max_length=80, blank=True)
    instagram = models.CharField(max_length=80, blank=True)
    twitter = models.CharField(max_length=80, blank=True)
    aboutus = models.TextField()
    contact = models.CharField(max_length=255)
    references = models.TextField()
    status = models.CharField(blank=True, max_length=5, choices=STATUS)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
