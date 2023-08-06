===============
Django Mailauth
===============

Mailauth is a Django authentication app to replace the default
username-based authentication with an email-based authentication.

Note: Mailauth should installed & setup before any migration is created.

Quick start
-----------
0. Install the ``django-mailauth`` authentication using pip from PyPi::
   
      pip install django-mailauth

1. Add "mailauth" to your INSTALLED_APPS setting like this::

      INSTALLED_APPS = [
        ...
        'mailauth',
      ]

2. Replace your default "User" model with with Mailauth's custom user model
   In your ``settings.py`` module, add or update the following line::
   
      AUTH_USER_MODEL = 'mailauth.User'

3. Run ``python manage.py makemigrations`` to create your first migrations.
4. Run ``python manage.py migrate`` to apply the changes to your database tables.

5. Start the development server and visit http://127.0.0.1:8000/admin/
   to add new users (you'll need the Admin app enabled).
