# Generated by Django 3.2.9 on 2021-12-09 02:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0006_auto_20211208_2231'),
    ]

    operations = [
        migrations.AddField(
            model_name='comentarios',
            name='parent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to='network.comentarios'),
        ),
    ]