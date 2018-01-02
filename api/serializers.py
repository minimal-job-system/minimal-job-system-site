from rest_framework import serializers
from webapp.models import JobTemplate, Job, JobParameterDeclaration, JobParameter

class JobParameterDeclarationSerializer(serializers.ModelSerializer):
    """Serializer to map the Model instance into JSON format."""
    class Meta:
        """Meta class to map serializer's fields with the model fields."""
        model = JobParameterDeclaration
        fields = ('id', 'name', 'description', 'type', 'default')

class JobTemplateSerializer(serializers.ModelSerializer):
    """Serializer to map the Model instance into JSON format."""
    parameter_declarations = JobParameterDeclarationSerializer(many=True, read_only=True)

    class Meta:
        """Meta class to map serializer's fields with the model fields."""
        model = JobTemplate
        fields = ('id', 'namespace', 'name', 'type', 'description', 'date_created', 'date_modified', 'parameter_declarations')
        read_only_fields = ('date_created', 'date_modified')

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
        fields = ('id', 'namespace', 'name', 'type', 'status', 'progress', 'date_created', 'date_modified', 'parameters')
        read_only_fields = ('date_created', 'date_modified')
