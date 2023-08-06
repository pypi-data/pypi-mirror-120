from allauth.socialaccount.adapter import DefaultSocialAccountAdapter

from django.conf import settings


def verify_user(user):
    # Create a new user. There's no ne®ed to set a password
    # because only the password from settings.py is checked.
    user.is_staff = check_user(user.email)
    user.is_superuser = check_user(user.email)
    user.save()
    return user


def check_user(username):
    # return username in settings.EMAIL_FOR_ADMIN
    return True

class CustomSocialAccountAdapter(DefaultSocialAccountAdapter):
    def save_user(self, request, sociallogin, form):
        sociallogin.user.username = sociallogin.user.email
        user = super(CustomSocialAccountAdapter, self).save_user(request, sociallogin, form)

        return verify_user(user)

    def is_safe_url(self, url):
        from django.utils.http import is_safe_url
        return is_safe_url(url)
