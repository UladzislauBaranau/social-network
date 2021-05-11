from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='avatar',
            field=models.ImageField(blank=True,
                                    default='uploads/profile_avatars/default_avatar.png',
                                    upload_to='uploads/profile_avatars'),
        ),
    ]
