# Generated by Django 2.2 on 2020-02-26 12:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('td_export', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='exportfile',
            name='study',
            field=models.CharField(blank=True, max_length=100),
        ),
    ]
