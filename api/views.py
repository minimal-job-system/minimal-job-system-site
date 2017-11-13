from rest_framework import generics
from .serializers import JobSerializer
from .models import Job

class CreateView(generics.ListCreateAPIView):
    """This class defines the create behavior of our rest api."""
    queryset = Job.objects.all()
    serializer_class = JobSerializer

    def perform_create(self, serializer):
        """Save the post data when creating a new job."""
        serializer.save()

class DetailsView(generics.RetrieveUpdateDestroyAPIView):
    """This class handles the http GET, PUT and DELETE requests."""

    queryset = Job.objects.all()
    serializer_class = JobSerializer
