# Generated by Django 3.2.5 on 2021-07-25 20:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('selling', '0002_auto_20210725_1414'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sortie',
            name='num',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
    ]
