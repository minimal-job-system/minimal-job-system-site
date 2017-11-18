# adapted from https://docs.djangoproject.com/en/1.11/howto/initial-data/

python3 manage.py makemigrations --name load_job_sources --empty webapp

cat > ./webapp/migrations/0004_load_job_sources.py << EOL
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models, migrations

def load_job_sources(apps, schema_editor):
    JobSource = apps.get_model("webapp", "JobSource")
    JobSource(
        id=0, name='Luigi Workflow Path [Primary]', type=0,
        uri='/home/dvischi/Documents/Django/job-system-project/luigi_workflows/'
    ).save()

class Migration(migrations.Migration):
    dependencies = [
        ('webapp', '0003_jobsource'),
    ]
    operations = [
        migrations.RunPython(load_job_sources),
    ]
EOL

python3 manage.py migrate
