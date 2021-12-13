import os
from setuptools import find_packages, setup
from setuptools.command.install import install
import sys

with open(os.path.join(os.path.dirname(__file__), 'README.md')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='django-minimal-job-system-site',
    version='0.0.4',
    packages=find_packages(exclude=['docs', 'tests']),
    #packages=find_packages('job_system_frontend'),
    #package_dir={'': 'job_system_frontend'},
    include_package_data=True,
    license='MIT License',
    description='A minimalistic Django project for managing technology-independent jobs.',
    long_description=README,
    url='https://github.com/dvischi/minimal-job-system-site/',
    author='Dario Vischi',
    author_email='dario.vischi@fmi.ch',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 2.0',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
    scripts=['manage.py'],
    install_requires=[
        'django==2.0.13',
        'django-filter==2.1.0',
        'djangorestframework==3.7.7',
        'django-constance[database]==2.3.1',
        'psycopg2-binary>=2.7.5',
        'django-minimal-job-system-api==0.0.4',
        'django-minimal-job-system-frontend==0.0.4'
    ]
)
