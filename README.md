# Minimal Job System - Site
Minimal Job System Site is a ready-to-use Django project including the Minimal Job System API and Frontend.

Detailed documentation is in the "docs" directory.

## Quick start
1. Setup web server

2. Setup postgres, create a new database 'jobsystem' and adapt job_system_site/settings.py accordingly

2. Setup a virtual environment and install the Django project with all its dependencies::

    pip install --editable .

3. Setup Minimal Job System API (see corresponding docs)

4. Setup Minimal Job System Frontend (see corresponding docs)

5. Run `python manage.py collectstatic` (within the virtual environment) to collect all static files from the apps


## architecture
![Architecture](/docs/architecture.png)
