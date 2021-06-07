from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class Profile(AbstractUser):
    GENDER_CHOICES = [
        ('M', _('Male')),
        ('F', _('Female')),
    ]
    avatar = models.ImageField(upload_to='uploads/profile_avatars',
                               default='uploads/profile_avatars/default_avatar.png',
                               blank=True)
    bio = models.TextField(default=_("Tell about yourself..."), max_length=200, blank=True)
    country = models.CharField(_("Country"), max_length=100, blank=True)
    city = models.CharField(_("City"), max_length=100, blank=True)
    phone = models.CharField(_("Phone"), max_length=50, blank=True)
    birth_date = models.DateField(_("Birth date"), null=True, blank=True)
    gender = models.CharField(_("Gender"), max_length=1, choices=GENDER_CHOICES)
    friends = models.ManyToManyField('self', through='Friendship')

    def __str__(self):
        return f"{self.username} {self.date_joined.strftime('%Y-%m-%d %H:%M:%S')}"


class Friendship(models.Model):
    STATUS_CHOICES = [
        ('S', _('Send')),
        ('A', _('Accepted')),
    ]
    sender = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='sender')
    receiver = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='receiver')
    date_created = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=8, choices=STATUS_CHOICES, default='S')

    def __str__(self):
        return f"{self.sender} - {self.receiver}, status={self.status}. " \
               f"Date created: {self.date_created.strftime('%Y-%m-%d %H:%M:%S')}"
