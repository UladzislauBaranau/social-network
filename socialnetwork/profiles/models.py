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

    def __str__(self):
        return f'{self.first_name} {self.last_name} {self.date_joined}'
