# Generated by Django 4.1.3 on 2023-01-01 23:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Themesettings',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('theme_option', models.CharField(choices=[('light', 'light'), ('dark', 'dark')], default='light', max_length=10)),
                ('theme_owner', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='theme_owner', to='account.profile')),
            ],
        ),
    ]
