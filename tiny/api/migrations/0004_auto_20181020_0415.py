# Generated by Django 2.1.2 on 2018-10-20 04:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_auto_20181020_0308'),
    ]

    operations = [
        migrations.AlterField(
            model_name='record',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]
