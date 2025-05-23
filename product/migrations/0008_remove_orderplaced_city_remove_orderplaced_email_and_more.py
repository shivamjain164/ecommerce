# Generated by Django 4.2.20 on 2025-04-11 10:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0007_address'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orderplaced',
            name='city',
        ),
        migrations.RemoveField(
            model_name='orderplaced',
            name='email',
        ),
        migrations.RemoveField(
            model_name='orderplaced',
            name='name',
        ),
        migrations.RemoveField(
            model_name='orderplaced',
            name='state',
        ),
        migrations.RemoveField(
            model_name='orderplaced',
            name='zip_code',
        ),
        migrations.AlterField(
            model_name='orderplaced',
            name='address',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='product.address'),
        ),
    ]
