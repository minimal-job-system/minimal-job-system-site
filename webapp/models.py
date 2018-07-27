from dateutil.parser import parse
from decimal import Decimal, InvalidOperation

from django.contrib.postgres.fields import JSONField
from django.core.exceptions import ValidationError
from django.core.validators import DecimalValidator, \
    MinValueValidator, MaxValueValidator
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
LOG_LEVEL_CHOICES = (
    (50, 'CRITICAL'),
    (40, 'ERROR'),
    (30, 'WARNING'),
    (20, 'INFO'),
    (10, 'DEBUG'),
    (0, 'NOTSET'),
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
    description = models.CharField(max_length=1024, blank=False)
    type = models.IntegerField(choices=PARAMETER_TYPE_CHOICES, blank=False)
    default = models.CharField(max_length=255, blank=False)
    # The following fields may contain dynamic expressions
    # which are evaluated during runtime
    is_hidden = models.CharField(max_length=255, blank=False, default="False")
    is_dangerous = models.CharField(
        max_length=255, blank=False, default="False"
    )

    def __str__(self):
        """Return a human readable representation of the model instance."""
        return "Job Parameter Declaration: {}".format(self.name)


class JobParameterDeclarationChoice(models.Model):
    """This class represents a job parameter declaration choice."""
    id = models.AutoField(primary_key=True)
    param_declaration = models.ForeignKey(
        'JobParameterDeclaration',
        related_name='choices',
        blank=True, null=True,
        on_delete=models.CASCADE,
    )
    value = models.CharField(max_length=255, blank=False)

    def __str__(self):
        """Return a human readable representation of the model instance."""
        return "Job Parameter Declaration Choice: {}".format(self.value)


class Job(models.Model):
    """This class represents the job model."""
    id = models.AutoField(primary_key=True)
    namespace = models.CharField(max_length=255, blank=False)
    name = models.CharField(max_length=255, blank=False)
    type = models.IntegerField(choices=JOB_TYPE_CHOICES, blank=False)
    status = models.CharField(max_length=255, blank=False)
    progress = models.FloatField(
        blank=False, default=0,
        #validators=[MinValueValidator(0), MaxValueValidator(100)]
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

    def clean(self):
        super(JobParameter, self).clean()

        if PARAMETER_TYPE_CHOICES[self.type][1] == "Integer":
            try:
                DecimalValidator(max_digits=None, decimal_places=0)(
                    Decimal(self.value)
                )
            except (ValidationError, InvalidOperation):
                raise ValidationError({
                    'value': ValidationError(
                        'Invalid integer value: "%(value)s"',
                        code='invalid', params={'value': self.value}
                    )
                })
        if PARAMETER_TYPE_CHOICES[self.type][1] == "Decimal":
            try:
                DecimalValidator(max_digits=None, decimal_places=None)(
                    Decimal(self.value)
                )
            except (ValidationError, InvalidOperation):
                raise ValidationError({
                    'value': ValidationError(
                        'Invalid decimal value: "%(value)s"',
                        code='invalid', params={'value': self.value}
                    )
                })
        if PARAMETER_TYPE_CHOICES[self.type][1] == "Boolean":
            if self.value.lower() not in ["true", "false"]:
                raise ValidationError({
                    'value': ValidationError(
                        'Invalid boolean value: "%(value)s"',
                        code='invalid', params={'value': self.value}
                    )
                })
        if PARAMETER_TYPE_CHOICES[self.type][1] == "Datetime":
            try:
                self.value = parse(self.value).isoformat()
            except ValueError:
                raise ValidationError({
                    'value': ValidationError(
                        'Invalid datetime value: "%(value)s"',
                        code='invalid', params={'value': self.value}
                    )
                })

    def __str__(self):
        """Return a human readable representation of the model instance."""
        return "Job Parameter: {}".format(self.name)


class JobLogEntry(models.Model):
    """This class represents a job log entry."""
    id = models.AutoField(primary_key=True)
    job = models.ForeignKey(
        'Job',
        related_name='log_entries',
        on_delete=models.CASCADE,
    )
    level = models.IntegerField(choices=LOG_LEVEL_CHOICES, blank=False)
    message = models.CharField(max_length=512, blank=False)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """Return a human readable representation of the model instance."""
        return "Job Log Entry: {}".format(self.name)
