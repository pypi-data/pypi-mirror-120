# Generated by Django 3.0.1 on 2020-02-12 06:43

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('textrank', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Sample',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='создан')),
                ('updated', models.DateTimeField(auto_now=True, db_index=True, verbose_name='обновлён')),
                ('checksum', models.CharField(blank=True, editable=False, max_length=32, verbose_name='контрольная сумма')),
                ('message', models.TextField(verbose_name='текст сообщения')),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='samples', to='textrank.Group', verbose_name='группа')),
                ('last_editor', models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL, verbose_name='последний редактор')),
            ],
            options={
                'verbose_name': 'образец',
                'verbose_name_plural': 'образцы',
                'ordering': ('-updated',),
                'unique_together': {('group', 'checksum')},
            },
        ),
    ]
