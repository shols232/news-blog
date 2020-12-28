from django.db import models
from django.utils import timezone
import sys 
from io import BytesIO 
from PIL import Image
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.template.defaultfilters import slugify

CHOICES = (
        ('ENTERTAINMENT', 'Entertainment'),
        ('FASHION', 'Fashion'),
        ('BUSINESS', 'Business'),
        ('WOMEN', 'Women'),
        ('NEWS', 'News'),
        ('FEATURES', 'Features'),
        ('HUMANITY', 'Humanity'),
        ('WILDLIFE', 'Wildlife'),
        ('CRIME', 'Crime'),
        ('POLITICS', 'Politics')
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
        self.slug = slugify(self.title) + f'-{self.pk}' 
        if self.image:
            # Opening the uploaded image
            im = Image.open(self.image)

            output = BytesIO()

            # Resize/modify the image
            im = im.resize((300, 300))

            # after modifications, save it to the output
            im.save(output, format='PNG', quality=90)
            output.seek(0)

            # change the imagefield value to be the newley modifed image value
            self.image = InMemoryUploadedFile(output, 'ImageField', "%s.png" % self.image.name.split('.')[0], 'image/png',
                                            sys.getsizeof(output), None)

        super(BlogPost, self).save(*args, **kwargs)
