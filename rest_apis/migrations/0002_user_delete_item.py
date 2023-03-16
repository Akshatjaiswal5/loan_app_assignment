# Generated by Django 4.1.7 on 2023-03-14 01:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rest_apis', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('email_id', models.EmailField(max_length=254, unique=True)),
                ('aadhar_id', models.CharField(max_length=12, unique=True)),
                ('annual_income', models.DecimalField(decimal_places=2, max_digits=12)),
                ('credit_score', models.IntegerField(blank=True, null=True)),
            ],
        ),
        migrations.DeleteModel(
            name='Item',
        ),
    ]