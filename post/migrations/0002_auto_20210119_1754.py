# Generated by Django 3.1.4 on 2021-01-19 17:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blogpost',
            name='section',
            field=models.CharField(choices=[('ENTERTAINMENT', 'Entertainment'), ('ENVIRONMENT', 'Environment'), ('BUSINESS', 'Business'), ('WOMEN', 'Women'), ('SPORTS', 'Sports'), ('HUMANITY', 'Humanity'), ('RESEARCH', 'Research'), ('PERSONAL', 'Personal'), ('INTERVIEWS', 'Interviews'), ('POLITICS', 'Politics'), ('TECHNOLOGY', 'Technology'), ('NEWS', 'news')], max_length=200),
        ),
    ]
