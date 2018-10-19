from django.utils import timezone
from rest_framework import serializers

from job_system_api.models import JobTemplate, Job, JobParameterDeclaration, \
    JobParameterDeclarationChoice, JobParameter, JobLogEntry


class DynamicFieldsModelSerializer(serializers.ModelSerializer):
    """
    A ModelSerializer that takes an additional `fields` and 'exclude' argument
    that controls which fields should be displayed.
    """
    def __init__(self, *args, **kwargs):
        fields = kwargs.pop('fields', None)
        exclude = kwargs.pop('exclude', None)

        super(DynamicFieldsModelSerializer, self).__init__(*args, **kwargs)

        if fields is not None:
            for field_name in set(self.fields.keys()) - set(fields):
                self.fields.pop(field_name)
        if exclude is not None:
            for exclude_name in set(exclude):
                self.fields.pop(exclude_name)


class JobParameterDeclarationChoiceSerializer(serializers.ModelSerializer):
    """Serializer to map the Model instance into JSON format."""
    class Meta:
        """Meta class to map serializer's fields with the model fields."""
        model = JobParameterDeclarationChoice
        fields = (
            'id', 'value'
        )


class JobParameterDeclarationSerializer(serializers.ModelSerializer):
    """Serializer to map the Model instance into JSON format."""
    choices = JobParameterDeclarationChoiceSerializer(many=True)

    class Meta:
        """Meta class to map serializer's fields with the model fields."""
        model = JobParameterDeclaration
        fields = (
            'id', 'name', 'description', 'type', 'default',
            'is_hidden', 'is_dangerous', 'choices'
        )


class JobTemplateSerializer(serializers.ModelSerializer):
    """Serializer to map the Model instance into JSON format."""
    parameter_declarations = JobParameterDeclarationSerializer(
        many=True, read_only=True
    )

    class Meta:
        """Meta class to map serializer's fields with the model fields."""
        model = JobTemplate
        fields = (
            'id', 'namespace', 'name', 'type', 'description',
            'date_created', 'date_modified', 'parameter_declarations'
        )
        read_only_fields = ('date_created', 'date_modified')


class JobLogEntrySerializer(serializers.ModelSerializer):
    """Serializer to map the Model instance into JSON format."""
    date_created = serializers.DateTimeField(default=timezone.now())

    class Meta:
        """Meta class to map serializer's fields with the model fields."""
        model = JobLogEntry
        fields = ('id', 'level', 'message', 'date_created')


class JobParameterSerializer(serializers.ModelSerializer):
    """Serializer to map the Model instance into JSON format."""
    class Meta:
        """Meta class to map serializer's fields with the model fields."""
        model = JobParameter
        fields = ('id', 'name', 'type', 'value')


class JobSerializer(serializers.ModelSerializer):
    """Serializer to map the Model instance into JSON format."""
    parameters = JobParameterSerializer(many=True, read_only=True)

    class Meta:
        """Meta class to map serializer's fields with the model fields."""
        model = Job
        fields = (
            'id', 'namespace', 'name', 'type', 'status', 'progress', 'owner',
            'date_created', 'date_modified', 'parameters'
        )
        read_only_fields = ('date_created', 'date_modified')


class JobDetailsSerializer(serializers.ModelSerializer):
    """Serializer to map the Model instance into JSON format."""
    parameters = JobParameterSerializer(many=True, read_only=True)
    log_entries = JobLogEntrySerializer(many=True, read_only=True)

    class Meta:
        """Meta class to map serializer's fields with the model fields."""
        model = Job
        fields = (
            'id', 'namespace', 'name', 'type', 'status', 'progress', 'owner',
            'date_created', 'date_modified', 'parameters', 'log_entries'
        )
        read_only_fields = ('date_created', 'date_modified')
