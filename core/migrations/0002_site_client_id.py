# Generated by Django 2.1.4 on 2018-12-17 19:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='site',
            name='client_id',
            field=models.CharField(max_length=100, null=True),
        ),
    ]