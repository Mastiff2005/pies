# Generated by Django 3.2 on 2021-11-21 12:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0006_alter_product_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='image',
            field=models.ImageField(default='cupcake.png', upload_to='products/'),
        ),
    ]
