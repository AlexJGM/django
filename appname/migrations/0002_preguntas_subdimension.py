# Generated by Django 4.1.7 on 2023-03-13 11:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('appname', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='preguntas',
            name='subdimension',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='appname.subdimension'),
            preserve_default=False,
        ),
    ]
