# Generated by Django 3.2.6 on 2021-08-31 20:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authors', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='author',
            options={'ordering': ('last_name', 'first_name'), 'verbose_name': 'Author'},
        ),
    ]