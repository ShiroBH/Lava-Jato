# Generated by Django 4.1.7 on 2023-05-18 05:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('LavaJatoapp', '0005_alter_dados_foto'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dados',
            name='foto',
            field=models.FileField(upload_to='LavaJatoapp/static/img'),
        ),
    ]
