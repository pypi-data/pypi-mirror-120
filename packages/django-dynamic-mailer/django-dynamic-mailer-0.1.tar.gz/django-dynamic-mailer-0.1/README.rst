================
Emails
================


Detailed documentation is in the "docs" directory.

Quick start
-----------

1. Add "project-mailer" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'emails',
    ]

2. Include the polls URLconf in your project urls.py like this::

    url(r'emails/', include('emails.urls'))),


3. Run `python manage.py migrate` to create the emails models.

4. Start the development server and visit http://127.0.0.1:8000/admin/
   to create a emails (you'll need the Admin app enabled).

5. Visit http://127.0.0.1:8000/emails to participate in the emails.