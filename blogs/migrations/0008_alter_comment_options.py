# Generated by Django 4.2.7 on 2023-11-09 01:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blogs', '0007_comment_date'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='comment',
            options={'ordering': ['-date']},
        ),
    ]