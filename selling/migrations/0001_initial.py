# Generated by Django 3.2.5 on 2021-07-25 14:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('administration', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Sortie',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data_exit', models.DateField(auto_now_add=True)),
                ('type_exit', models.CharField(max_length=20)),
                ('unity', models.CharField(max_length=10)),
                ('selling_price', models.FloatField()),
                ('qte', models.FloatField()),
                ('discount', models.FloatField(default=0)),
                ('profit', models.FloatField()),
                ('article_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='administration.articles')),
            ],
            options={
                'db_table': 'Sortie',
            },
        ),
        migrations.CreateModel(
            name='Commande',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('unity', models.CharField(max_length=10)),
                ('selling_price', models.FloatField()),
                ('qte', models.FloatField()),
                ('discount', models.FloatField(default=0)),
                ('num', models.CharField(max_length=10)),
                ('article_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='administration.articles')),
            ],
            options={
                'db_table': 'Commande',
            },
        ),
    ]
