# Generated by Django 2.1.1 on 2018-10-21 11:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appserver', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Exercise',
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
            name='Milestone',
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
            name='MilestonesExercises',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('milestone', models.IntegerField(blank=True, null=True)),
                ('exercise', models.IntegerField(blank=True, db_column='test', null=True)),
            ],
            options={
                'db_table': 'milestones_exercises',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='MilestonesTest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('milestone', models.IntegerField(blank=True, null=True)),
                ('test', models.IntegerField(blank=True, null=True)),
            ],
            options={
                'db_table': 'milestones_test',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Test',
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
            name='Result',
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
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_active', models.DateField()),
                ('password', models.CharField(db_column='pass', max_length=256)),
                ('username', models.CharField(max_length=256)),
                ('email', models.CharField(max_length=256)),
                ('lang', models.CharField(max_length=3)),
            ],
            options={
                'db_table': 'users',
                'managed': True,
            },
        ),
        migrations.AlterModelOptions(
            name='child',
            options={'managed': True},
        ),
        migrations.AlterModelOptions(
            name='userchild',
            options={'managed': True},
        ),
    ]