# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2017-05-01 20:01
from __future__ import unicode_literals

import background.models
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Background',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.FileField(blank=True, null=True, upload_to=background.models.download_location)),
            ],
        ),
    ]
