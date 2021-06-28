from django.db import models
from django.utils import timezone
import sys 
from io import BytesIO 
from PIL import Image
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.template.defaultfilters import slugify
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token



CHOICES = (
        ('ENTERTAINMENT', 'Entertainment'),
        ('ENVIRONMENT', 'Environment'),
        ('BUSINESS', 'Business'),
        ('WOMEN', 'Women'),
        ('SPORTS', 'Sports'),
        ('HUMANITY', 'Humanity'),
        ('RESEARCH', 'Research'),
        ('PERSONAL', 'Personal'),
        ('INTERVIEWS', 'Interviews'),
        ('POLITICS', 'Politics'),
        ('TECHNOLOGY', 'Technology'),
        ('HEALTH', 'Health'),
        ('FEATURES', 'Features'),
        ('CRIME', 'Crime'),
        ('ROMANCE', 'Romance'),
        ('NEWS', 'news'),
        ('SDGS', 'SDGs')
    )

class BlogPost(models.Model):
    title = models.CharField(max_length=350)
    content = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to='post/images', blank=True, null=True)
    section = models.CharField(max_length=200, choices=CHOICES)
    slug = models.SlugField(max_length=500)
    posted = models.DateTimeField(auto_now_add=True)
    video = models.FileField(upload_to='post/videos', blank=True, null=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        if self.image:
            # Opening the uploaded image
            im = Image.open(self.image)

            output = BytesIO()

            # Resize/modify the image
            im = im.resize((800, 800))

            # after modifications, save it to the output
            im.save(output, format='PNG', quality=98)
            output.seek(0)

            # change the imagefield value to be the newley modifed image value
            self.image = InMemoryUploadedFile(output, 'ImageField', "%s.png" % self.image.name.split('.')[0], 'image/png',
                                            sys.getsizeof(output), None)

        super(BlogPost, self).save(*args, **kwargs)


class InPostImages(models.Model):
    upload = models.ImageField(upload_to='in-post/images', blank=True, null=True)

    def save(self, *args, **kwargs):
        if self.upload:
            # Opening the uploaded image
            im = Image.open(self.upload)

            output = BytesIO()

            # Resize/modify the image
            im = im.resize((250, 250))

            # after modifications, save it to the output
            im.save(output, format='PNG', quality=98)
            output.seek(0)

            # change the imagefield value to be the newley modifed image value
            self.upload = InMemoryUploadedFile(output, 'ImageField', "%s.png" % self.upload.name.split('.')[0], 'image/png',
                                            sys.getsizeof(output), None)

        super(InPostImages, self).save(*args, **kwargs)


@receiver(post_save, sender=BlogPost)
def edit_slug(sender, instance, created, **kwargs):
    if created:
        temp = instance.slug
        blog_post = BlogPost.objects.filter(id=instance.id).update(slug= temp + '-' + str(instance.id))

@receiver(post_save, sender=User)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
