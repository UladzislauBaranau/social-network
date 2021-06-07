from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0003_model_friendship'),
    ]

    operations = [
        migrations.AddField(
            model_name='friendship',
            name='status',
            field=models.CharField(choices=[('S', 'Send'), ('A', 'Accepted')], default='S', max_length=8),
        ),
    ]
