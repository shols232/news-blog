# Generated by Django 3.1.4 on 2021-01-11 13:41

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BlogPost',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=350)),
                ('content', models.TextField(blank=True, null=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to='post/images')),
                ('section', models.CharField(choices=[('ENTERTAINMENT', 'Entertainment'), ('ENVIRONMENT', 'Environment'), ('BUSINESS', 'Business'), ('WOMEN', 'Women'), ('SPORTS', 'Sports'), ('HUMANITY', 'Humanity'), ('RESEARCH', 'Research'), ('PERSONAL', 'Personal'), ('INTERVIEWS', 'Interviews'), ('POLITICS', 'Politics'), ('TECHNOLOGY', 'Technology')], max_length=200)),
                ('slug', models.SlugField(max_length=500)),
                ('posted', models.DateTimeField(auto_now_add=True)),
                ('video', models.FileField(blank=True, null=True, upload_to='post/videos')),
            ],
        ),
        migrations.CreateModel(
            name='InPostImages',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('upload', models.ImageField(blank=True, null=True, upload_to='in-post/images')),
            ],
        ),
    ]
