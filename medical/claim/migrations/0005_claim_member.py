# Generated by Django 3.2.3 on 2022-03-30 10:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('claim', '0004_auto_20220329_2149'),
    ]

    operations = [
        migrations.AddField(
            model_name='claim',
            name='member',
            field=models.IntegerField(default=0),
        ),
    ]