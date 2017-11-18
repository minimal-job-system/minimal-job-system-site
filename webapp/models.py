from django.contrib.postgres.fields import JSONField
from django.db import models

class JobSource(models.Model):
    """This class represents the job source model."""
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, blank=False, unique=True)
    type = models.IntegerField(choices=((0, 'Luigi Workflow'),), blank=False)
    uri = models.CharField(max_length=255, blank=False)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        """Return a human readable representation of the model instance."""
        return "Job Source: {}".format(self.name)

class JobTemplate(models.Model):
    """This class represents the job model."""
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, blank=False, unique=True)
    type = models.IntegerField(choices=((0, 'Luigi Workflow'),), blank=False)
    description = models.CharField(max_length=255, blank=False)
    parameters = JSONField(blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        """Return a human readable representation of the model instance."""
        return "Job Template: {}".format(self.name)

class Job(models.Model):
    """This class represents the job model."""
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, blank=False, unique=True)
    type = models.CharField(max_length=255, blank=False)
    status = models.CharField(max_length=255, blank=False)
    meta = JSONField(blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        """Return a human readable representation of the model instance."""
        return "Job: {}".format(self.name)
