# Generated by Django 4.2.7 on 2023-11-09 01:18

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("blogs", "0006_alter_comment_parent"),
    ]

    operations = [
        migrations.AddField(
            model_name="comment",
            name="date",
            field=models.DateTimeField(auto_now_add=True, default="1111-11-11"),
            preserve_default=False,
        ),
    ]
