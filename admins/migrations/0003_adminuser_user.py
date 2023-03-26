# Generated by Django 4.1.7 on 2023-03-26 13:22

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('admins', '0002_remove_adminuser_user_adminuser_email_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='adminuser',
            name='user',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
