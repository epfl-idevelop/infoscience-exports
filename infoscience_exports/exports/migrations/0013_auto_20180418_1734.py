# Generated by Django 2.0.3 on 2018-04-18 15:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exports', '0012_export_show_summary'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='memberof',
        ),
        migrations.AlterField(
            model_name='user',
            name='group',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='units',
            field=models.TextField(blank=True, null=True),
        ),
    ]
