# Generated by Django 4.2.4 on 2023-08-17 11:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("posts", "0004_followers"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="followers",
            name="follow",
        ),
        migrations.RemoveField(
            model_name="followers",
            name="user",
        ),
        migrations.AddField(
            model_name="followers",
            name="follower",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="follower",
                to="posts.userprofile",
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="followers",
            name="following",
            field=models.ForeignKey(
                default="1",
                on_delete=django.db.models.deletion.CASCADE,
                related_name="following",
                to="posts.userprofile",
            ),
            preserve_default=False,
        ),
    ]