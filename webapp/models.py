from django.contrib.postgres.fields import JSONField
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


JOB_TYPE_CHOICES = (
    (0, 'Luigi Workflow'),
)
PARAMETER_TYPE_CHOICES = (
    (0, 'Integer'),
    (1, 'Decimal'),
    (2, 'String'),
    (3, 'Boolean'),
    (4, 'Datetime'),
)


class JobSource(models.Model):
    """This class represents the job source model."""
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, blank=False)
    type = models.IntegerField(choices=JOB_TYPE_CHOICES, blank=False)
    uri = models.CharField(max_length=255, blank=False)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        """Return a human readable representation of the model instance."""
        return "Job Source: {}".format(self.name)


class JobTemplate(models.Model):
    """This class represents the job model."""
    id = models.AutoField(primary_key=True)
    namespace = models.CharField(max_length=255, blank=False)
    name = models.CharField(max_length=255, blank=False)
    type = models.IntegerField(choices=JOB_TYPE_CHOICES, blank=False)
    description = models.CharField(max_length=255, blank=False)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        """Return a human readable representation of the model instance."""
        return "Job Template: {}".format(self.name)


class JobParameterDeclaration(models.Model):
    """This class represents a job parameter declaration."""
    id = models.AutoField(primary_key=True)
    template = models.ForeignKey(
        'JobTemplate',
        related_name='parameter_declarations',
        on_delete=models.CASCADE,
    )
    name = models.CharField(max_length=255, blank=False)
    description = models.CharField(max_length=255, blank=False)
    type = models.IntegerField(choices=PARAMETER_TYPE_CHOICES, blank=False)
    default = models.CharField(max_length=255, blank=False)

    def __str__(self):
        """Return a human readable representation of the model instance."""
        return "Job Parameter Declaration: {}".format(self.name)


class Job(models.Model):
    """This class represents the job model."""
    id = models.AutoField(primary_key=True)
    namespace = models.CharField(max_length=255, blank=False)
    name = models.CharField(max_length=255, blank=False)
    type = models.IntegerField(choices=JOB_TYPE_CHOICES, blank=False)
    status = models.CharField(max_length=255, blank=False)
    progress = models.FloatField(
        blank=False, default=0,
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    owner = models.CharField(max_length=255, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        """Return a human readable representation of the model instance."""
        return "Job: {}".format(self.name)


class JobParameter(models.Model):
    """This class represents a job parameter."""
    id = models.AutoField(primary_key=True)
    job = models.ForeignKey(
        'Job',
        related_name='parameters',
        on_delete=models.CASCADE,
    )
    name = models.CharField(max_length=255, blank=False)
    type = models.IntegerField(choices=PARAMETER_TYPE_CHOICES, blank=False)
    value = models.CharField(max_length=255, blank=False)

    def __str__(self):
        """Return a human readable representation of the model instance."""
        return "Job Parameter: {}".format(self.name)
