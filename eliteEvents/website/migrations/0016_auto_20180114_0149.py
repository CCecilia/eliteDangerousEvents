# Generated by Django 2.0 on 2018-01-14 01:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0015_auto_20180113_0231'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='timezone',
            field=models.CharField(default='America/New_York', max_length=200),
        ),
        migrations.AlterField(
            model_name='event',
            name='platform',
            field=models.CharField(choices=[('XB', 'XBox'), ('PC', 'Computer'), ('PS', 'Playstation')], default='PC', max_length=2),
        ),
    ]
