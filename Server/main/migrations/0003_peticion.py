# Generated by Django 3.2.5 on 2021-09-24 17:58

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('main', '0002_alter_stock_options'),
    ]

    operations = [
        migrations.CreateModel(
            name='Peticion',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('hora', models.DateTimeField(auto_now_add=True)),
                ('estado', models.IntegerField(choices=[(1, 'Pendiente'), (2, 'Aprobada'), (3, 'Rechazada')])),
                ('pedido', models.TextField(null=True)),
                ('mensaje', models.TextField(blank=True, default=None, null=True)),
                ('autor', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('staff', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='staff_a_cargo', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['hora'],
            },
        ),
    ]
