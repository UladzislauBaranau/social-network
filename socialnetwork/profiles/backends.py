from django.contrib.auth.backends import ModelBackend, UserModel
from django.db.models import Q

from .models import Friendship


class EmailPhoneAuthBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = UserModel.objects.get(Q(username__exact=username) |
                                         Q(email__exact=username) |
                                         Q(phone__exact=username))
        except UserModel.DoesNotExist:
            return None
        else:
            if user.check_password(password) and self.user_can_authenticate(user):
                return user

    def get_user(self, user_id):
        try:
            user = UserModel.objects.get(pk=user_id)
        except UserModel.DoesNotExist:
            return None
        return user if self.user_can_authenticate(user) else None


def get_friends(request):
    qs_senders = Friendship.objects.filter(sender=request.user).filter(status='A')
    qs_receivers = Friendship.objects.filter(receiver=request.user).filter(status='A')

    friends = []
    for i in qs_senders:
        friends.append(i.receiver)
    for i in qs_receivers:
        friends.append(i.sender) if i.sender not in friends else None
    return friends
