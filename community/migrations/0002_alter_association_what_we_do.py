# Generated by Django 4.1.3 on 2022-12-31 09:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('community', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='association',
            name='what_we_do',
            field=models.TextField(blank=True, null=True),
        ),
    ]