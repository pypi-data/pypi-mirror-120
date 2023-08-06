=====
polibraslogin
=====

polibraslogin is a Django app to conduct Web-based polibraslogin. For each question,
visitors can choose between a fixed number of answers.

Detailed documentation is in the "docs" directory.

Quick start
-----------

1. Add "polibraslogin" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        'polibraslogin',
        'django.contrib.sites',
        'allauth',
        'allauth.account',
        'allauth.socialaccount',
        'allauth.socialaccount.providers.google',
        ...
    ]

1.1 Add next lines in your settings.py::

    ACCOUNT_EMAIL_REQUIRED = True
    ACCOUNT_AUTHENTICATION_METHOD = 'email'
    SOCIALACCOUNT_ADAPTER = 'polibraslogin.social.CustomSocialAccountAdapter'

2. Include the polibraslogin URLconf in your project urls.py like this::

    path('accounts/', include('allauth.urls')),

3. Run ``python manage.py migrate`` to create the polls models.

4. Start the development server and visit http://127.0.0.1:8000/admin/
   to create a poll (you'll need the Admin app enabled).
