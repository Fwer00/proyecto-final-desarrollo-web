# Generated by Django 4.2.2 on 2023-07-27 20:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('noticias', '0007_remove_comentario_parent'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comentario',
            name='noticia',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='noticias.noticia'),
        ),
    ]
