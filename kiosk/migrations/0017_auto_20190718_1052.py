# Generated by Django 2.1 on 2019-07-18 08:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kiosk', '0016_buchung_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='zelt',
            name='zelt_balance',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=6),
        ),
        migrations.AddField(
            model_name='zeltlager',
            name='lager_balance',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=6),
        ),
    ]
