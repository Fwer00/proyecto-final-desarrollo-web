# Generated by Django 4.2.3 on 2023-07-21 02:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contacto', '0002_remove_contacto_avisos'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='contacto',
            name='tipo_consulta',
        ),
    ]