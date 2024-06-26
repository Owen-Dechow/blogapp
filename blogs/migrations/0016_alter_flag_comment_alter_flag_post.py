# Generated by Django 4.2.7 on 2024-05-17 21:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blogs', '0015_flag_delete_commentflag'),
    ]

    operations = [
        migrations.AlterField(
            model_name='flag',
            name='comment',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='CommentFlag_comment', to='blogs.comment'),
        ),
        migrations.AlterField(
            model_name='flag',
            name='post',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='CommentFlag_comment', to='blogs.post'),
        ),
    ]
