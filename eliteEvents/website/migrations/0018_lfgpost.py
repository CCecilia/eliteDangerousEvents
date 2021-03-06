# Generated by Django 2.0 on 2018-01-15 15:08

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('website', '0017_auto_20180114_0245'),
    ]

    operations = [
        migrations.CreateModel(
            name='LFGPost',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('platform', models.CharField(choices=[('XB', 'XBox'), ('PC', 'Computer'), ('PS', 'Playstation')], default='PC', max_length=2)),
                ('group_size', models.IntegerField(default=3)),
                ('post_type', models.CharField(max_length=200, null=True)),
                ('creator', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('players', models.ManyToManyField(related_name='players', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
