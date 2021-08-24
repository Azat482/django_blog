# Generated by Django 3.2.5 on 2021-08-24 14:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main_web', '0006_auto_20210824_1420'),
    ]

    operations = [
        migrations.DeleteModel(
            name='BaseSiteObject',
        ),
        migrations.AlterField(
            model_name='commentarticle',
            name='owner_object',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='main_web.article'),
        ),
        migrations.AlterField(
            model_name='dislikearticle',
            name='owner_object',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='main_web.article'),
        ),
        migrations.AlterField(
            model_name='dislikearticlecomment',
            name='owner_object',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='main_web.commentarticle'),
        ),
        migrations.AlterField(
            model_name='likearticle',
            name='owner_object',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='main_web.article'),
        ),
        migrations.AlterField(
            model_name='likearticlecomment',
            name='owner_object',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='main_web.commentarticle'),
        ),
    ]