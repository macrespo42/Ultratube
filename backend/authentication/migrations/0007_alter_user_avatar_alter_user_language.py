# Generated by Django 5.0.1 on 2024-03-19 17:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0006_alter_user_avatar_alter_user_email_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='avatar',
            field=models.CharField(blank=True, choices=[('http://localhost:3000/src/assets/profiles/8.svg', 'http://localhost:3000/src/assets/profiles/8.svg'), ('http://localhost:3000/src/assets/profiles/6.svg', 'http://localhost:3000/src/assets/profiles/6.svg'), ('http://localhost:3000/src/assets/profiles/12.svg', 'http://localhost:3000/src/assets/profiles/12.svg'), ('http://localhost:3000/src/assets/profiles/4.svg', 'http://localhost:3000/src/assets/profiles/4.svg'), ('http://localhost:3000/src/assets/profiles/10.svg', 'http://localhost:3000/src/assets/profiles/10.svg'), ('http://localhost:3000/src/assets/profiles/5.svg', 'http://localhost:3000/src/assets/profiles/5.svg'), ('http://localhost:3000/src/assets/profiles/9.svg', 'http://localhost:3000/src/assets/profiles/9.svg'), ('http://localhost:3000/src/assets/profiles/7.svg', 'http://localhost:3000/src/assets/profiles/7.svg'), ('http://localhost:3000/src/assets/profiles/2.svg', 'http://localhost:3000/src/assets/profiles/2.svg'), ('http://localhost:3000/src/assets/profiles/3.svg', 'http://localhost:3000/src/assets/profiles/3.svg'), ('http://localhost:3000/src/assets/profiles/1.svg', 'http://localhost:3000/src/assets/profiles/1.svg'), ('http://localhost:3000/src/assets/profiles/11.svg', 'http://localhost:3000/src/assets/profiles/11.svg')]),
        ),
        migrations.AlterField(
            model_name='user',
            name='language',
            field=models.CharField(choices=[('ru', 'ru'), ('en', 'en'), ('gb', 'gb'), ('es', 'es'), ('fr', 'fr')], default='en'),
        ),
    ]
