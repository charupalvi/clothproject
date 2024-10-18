# Generated by Django 5.1.1 on 2024-10-17 04:04

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clothapp', '0005_order'),
    ]

    operations = [
        migrations.CreateModel(
            name='Multiimage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('imagepath', models.ImageField(default='', upload_to='image')),
                ('clothid', models.ForeignKey(db_column='clothid', on_delete=django.db.models.deletion.CASCADE, to='clothapp.cloth')),
            ],
        ),
    ]
