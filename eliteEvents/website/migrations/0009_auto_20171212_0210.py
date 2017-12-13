# Generated by Django 2.0 on 2017-12-12 02:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0008_event_attendees'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='end_time',
            field=models.TimeField(null=True),
        ),
        migrations.AddField(
            model_name='event',
            name='start_time',
            field=models.TimeField(null=True),
        ),
        migrations.AlterField(
            model_name='event',
            name='end_date',
            field=models.DateField(null=True),
        ),
        migrations.AlterField(
            model_name='event',
            name='start_date',
            field=models.DateField(null=True),
        ),
    ]