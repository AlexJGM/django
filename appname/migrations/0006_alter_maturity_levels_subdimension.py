# Generated by Django 4.1.7 on 2023-04-24 07:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appname', '0005_alter_preguntas_id_pregunta'),
    ]

    operations = [
        migrations.AlterField(
            model_name='maturity_levels',
            name='subdimension',
            field=models.CharField(max_length=10),
        ),
    ]