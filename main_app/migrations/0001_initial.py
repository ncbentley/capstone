# Generated by Django 3.0.8 on 2020-07-08 22:35

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Page',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=50)),
                ('email', models.EmailField(max_length=50, unique=True)),
                ('user_type', models.CharField(choices=[('client', 'Client'), ('dev', 'Developer')], max_length=10)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='client', to='main_app.Profile')),
                ('dev', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='dev', to='main_app.Profile')),
            ],
        ),
        migrations.CreateModel(
            name='Sprint',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main_app.Project')),
            ],
        ),
        migrations.CreateModel(
            name='Wireframe',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='')),
                ('description', models.TextField(max_length=200)),
                ('page', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main_app.Page')),
            ],
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField(max_length=200)),
                ('completed', models.BooleanField(default=False)),
                ('sprint', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main_app.Sprint')),
            ],
        ),
        migrations.AddField(
            model_name='page',
            name='project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main_app.Project'),
        ),
    ]