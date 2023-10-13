# Generated by Django 4.2.5 on 2023-10-13 10:39

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('main', '0003_alter_service_options_remove_service_image_image'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='image',
            options={},
        ),
        migrations.AlterModelOptions(
            name='service',
            options={'verbose_name': 'Service', 'verbose_name_plural': 'Services'},
        ),
        migrations.CreateModel(
            name='ShoppingCart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('upload_at', models.DateTimeField(auto_now_add=True)),
                ('count', models.IntegerField(default=1)),
                ('service', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.service')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
