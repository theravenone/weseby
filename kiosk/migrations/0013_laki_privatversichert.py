# Generated by Django 2.1 on 2019-03-02 07:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kiosk', '0012_auto_20190210_1354'),
    ]

    operations = [
        migrations.AddField(
            model_name='laki',
            name='privatVersichert',
            field=models.BooleanField(default=False),
        ),
    ]