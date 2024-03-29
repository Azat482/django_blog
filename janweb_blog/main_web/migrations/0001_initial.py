# Generated by Django 3.2.5 on 2021-08-23 17:38

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('short_description', models.CharField(default='', max_length=500)),
                ('text', models.TextField(max_length=200000)),
                ('data_post', models.DateField(null=True)),
                ('time_post', models.TimeField(null=True)),
                ('changed_flag', models.BooleanField(default=False)),
                ('author', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-data_post'],
            },
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cat', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='CommentArticle',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('datetime_creating', models.DateTimeField(auto_now_add=True)),
                ('comment_text', models.TextField(max_length=5000, null=True)),
                ('owner_object', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='main_web.article')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-datetime_creating'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='auth.user')),
                ('avatar_url', models.ImageField(max_length=200, null=True, upload_to='')),
                ('date_registration', models.DateTimeField(auto_now_add=True)),
                ('user_likes_count', models.IntegerField(default=0)),
                ('user_dislikes_count', models.IntegerField(default=0)),
                ('user_articles_count', models.IntegerField(default=0)),
                ('user_comments_count', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='LikeArticleComment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('datetime_creating', models.DateTimeField(auto_now_add=True)),
                ('owner_object', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='main_web.commentarticle')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-datetime_creating'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='LikeArticle',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('datetime_creating', models.DateTimeField(auto_now_add=True)),
                ('owner_object', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='main_web.article')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-datetime_creating'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='DislikeArticleComment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('datetime_creating', models.DateTimeField(auto_now_add=True)),
                ('owner_object', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='main_web.commentarticle')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-datetime_creating'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='DislikeArticle',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('datetime_creating', models.DateTimeField(auto_now_add=True)),
                ('owner_object', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='main_web.article')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-datetime_creating'],
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='article',
            name='cat',
            field=models.ManyToManyField(to='main_web.Category'),
        ),
    ]
