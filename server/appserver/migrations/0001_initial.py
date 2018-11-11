# Generated by Django 2.1.1 on 2018-10-12 10:16

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Child',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=30)),
                ('parent', models.IntegerField()),
                ('last_active', models.DateField()),
                ('birthday', models.DateField()),
                ('sec_code', models.IntegerField(blank=True, null=True)),
            ],
            options={
                'db_table': 'child',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Exercises',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lang', models.CharField(max_length=3)),
                ('ex', models.CharField(max_length=1000)),
                ('image_url', models.CharField(blank=True, max_length=1000, null=True)),
                ('video_url', models.CharField(blank=True, max_length=1000, null=True)),
            ],
            options={
                'db_table': 'exercises',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Milestones',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('target_age', models.IntegerField()),
                ('lang', models.CharField(max_length=3)),
                ('description', models.CharField(max_length=1000)),
            ],
            options={
                'db_table': 'milestones',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Results',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key_milestone', models.IntegerField()),
                ('key_user', models.IntegerField()),
                ('key_child', models.IntegerField()),
                ('result_value', models.BooleanField()),
                ('datetime', models.DateField()),
            ],
            options={
                'db_table': 'results',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Tests',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lang', models.CharField(max_length=3)),
                ('description', models.CharField(max_length=1000)),
                ('follow_up_question', models.IntegerField(blank=True, null=True)),
                ('back_question', models.IntegerField(blank=True, null=True)),
            ],
            options={
                'db_table': 'tests',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='UserChild',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('parent', models.IntegerField()),
                ('child', models.IntegerField()),
            ],
            options={
                'db_table': 'user_child',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Users',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_active', models.DateField()),
                ('pass_field', models.CharField(db_column='pass', max_length=256)),
                ('username', models.CharField(max_length=256)),
                ('email', models.CharField(max_length=256)),
                ('lang', models.CharField(max_length=3)),
            ],
            options={
                'db_table': 'users',
                'managed': False,
            },
        ),
    ]
