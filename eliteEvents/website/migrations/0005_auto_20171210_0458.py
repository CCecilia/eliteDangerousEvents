# Generated by Django 2.0 on 2017-12-10 04:58

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('website', '0004_delete_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='creator',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='event',
            name='end_date',
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name='event',
            name='event_type',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='event',
            name='location',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='event',
            name='start_date',
            field=models.DateTimeField(null=True),
        ),
    ]