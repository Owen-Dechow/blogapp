# Generated by Django 4.2.7 on 2023-11-20 20:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blogs', '0011_remove_blog_url_name_blog_header'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='commentflag',
            name='manager',
        ),
        migrations.RemoveField(
            model_name='commentflag',
            name='reason',
        ),
    ]
