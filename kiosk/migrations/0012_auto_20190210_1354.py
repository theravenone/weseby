# Generated by Django 2.1 on 2019-02-10 12:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kiosk', '0011_laki_hinweis'),
    ]

    operations = [
        migrations.AlterField(
            model_name='zelt',
            name='zeltnummer',
            field=models.IntegerField(default=1),
        ),
    ]