# Generated by Django 3.1.4 on 2020-12-23 03:58

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('category', models.IntegerField(default=1)),
                ('manufacturer', models.CharField(default='производитель не выбран', max_length=25)),
                ('description', models.TextField()),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('price_purc', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('shelf_life', models.IntegerField(default=0)),
                ('image', models.ImageField(default='pies\\products\\static\x08otw.jpg', upload_to='static/')),
            ],
        ),
    ]
