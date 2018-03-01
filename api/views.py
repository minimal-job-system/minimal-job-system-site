from django_filters import rest_framework as filters
from rest_framework import generics
from .serializers import JobTemplateSerializer, JobSerializer

from webapp.models import JobTemplate, Job
from webapp.models import JOB_TYPE_CHOICES


class JobTemplateCreateView(generics.ListCreateAPIView):
    """This class defines the create behavior of our rest api."""
    queryset = JobTemplate.objects.all()
    serializer_class = JobTemplateSerializer

    def perform_create(self, serializer):
        """Save the post data when creating a new job template."""
        serializer.save()


class JobTemplateDetailsView(generics.RetrieveUpdateDestroyAPIView):
    """This class handles the http GET, PUT and DELETE requests."""
    queryset = JobTemplate.objects.all()
    serializer_class = JobTemplateSerializer


class JobTypeFilter(filters.FilterSet):
    type_name = filters.CharFilter(label="Type Name", method="filter_type")

    class Meta:
        model = Job
        fields = [
            'id', 'namespace', 'name', 'type_name', 'type', 'status',
            'progress', 'owner'
        ]

    def filter_type(self, queryset, name, value):
        type = [
            choice_key for choice_key, choice_value in JOB_TYPE_CHOICES
            if choice_value == value
        ]
        return queryset.filter(
            type=type[0] if len(type) == 1 else -1
        )


class JobListView(generics.ListAPIView):
    """This class defines the create behavior of our rest api."""
    queryset = Job.objects.all()
    serializer_class = JobSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filter_class = JobTypeFilter
    filter_fields = ('type',)

    def perform_create(self, serializer):
        """Save the post data when creating a new job."""
        serializer.save()


class JobCreateView(generics.ListCreateAPIView):
    """This class defines the create behavior of our rest api."""
    queryset = Job.objects.all()
    serializer_class = JobSerializer

    def perform_create(self, serializer):
        """Save the post data when creating a new job."""
        serializer.save()


class JobDetailsView(generics.RetrieveUpdateDestroyAPIView):
    """This class handles the http GET, PUT and DELETE requests."""
    queryset = Job.objects.all()
    serializer_class = JobSerializer
