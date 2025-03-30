# Generated by Django 5.0.6 on 2025-03-30 15:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Company', '0002_remove_department_departmentcards_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('accountCode', models.AutoField(primary_key=True, serialize=False, unique=True)),
                ('name', models.CharField(default='', max_length=200)),
                ('userName', models.CharField(default='', max_length=200)),
                ('emailAddress', models.EmailField(max_length=254)),
                ('password', models.CharField(max_length=254)),
                ('accountRole', models.CharField(choices=[('ENGINEER', 'ENGINEER'), ('TEAM LEADER', 'TEAM LEADER'), ('DEPARTMENT LEADER', 'DEPARTMENT LEADER'), ('SENIOR MANAGER', 'SENIOR MANAGER')], default='ENGINEER', max_length=20)),
            ],
        ),
    ]
