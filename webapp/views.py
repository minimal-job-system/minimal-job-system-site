from django.shortcuts import render
from django.views.generic import DetailView
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.utils import timezone

from .models import JobTemplate, Job

def index(request):
    return HttpResponse("<h1>Welcome to the Minimal Job System Web Application</h1>")


class JobListView(ListView):
    model = Job

    def get_context_data(self, **kwargs):
        context = super(JobListView, self).get_context_data(**kwargs)
        context['now'] = timezone.now()
        return context

class JobDetailView(DetailView):
    model = Job

class JobCreateView(CreateView):
    model = Job
    success_url = reverse_lazy('jobs_list')
    fields = ['name']

    def get_context_data(self, **kwargs):
        context = super(JobCreateView, self).get_context_data(**kwargs)
        return context

class JobUpdateView(UpdateView):
    model = Job
    success_url = reverse_lazy('jobs_list')
    fields = ['name']

    def get_context_data(self, **kwargs):
        context = super(JobUpdateView, self).get_context_data(**kwargs)
        return context

class JobDeleteView(DeleteView):
    model = Job
    success_url = reverse_lazy('jobs_list')

    def get_context_data(self, **kwargs):
        context = super(JobDeleteView, self).get_context_data(**kwargs)
        return context
