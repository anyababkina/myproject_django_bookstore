# Generated by Django 3.2.18 on 2023-04-22 14:42

from django.db import migrations, models
import django.db.models.deletion
import users.models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0007_bookorder_order_steporder_wayorder'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='user',
            managers=[
                ('objects', users.models.UserManager()),
            ],
        ),
        migrations.RemoveField(
            model_name='user',
            name='username',
        ),
        migrations.AlterField(
            model_name='order',
            name='step',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.DO_NOTHING, to='users.steporder'),
        ),
        migrations.AlterField(
            model_name='order',
            name='way',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='users.wayorder', verbose_name='Как доставить заказ?'),
        ),
        migrations.AlterField(
            model_name='wayorder',
            name='name',
            field=models.CharField(max_length=255, verbose_name='Как доставить заказ?'),
        ),
    ]
