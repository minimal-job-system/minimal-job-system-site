from django.db import transaction
from django.shortcuts import render
from django.views.generic import DetailView
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.utils import timezone

from .models import JobSource, JobTemplate, Job, JobParameter
from .forms import JobTemplateFormSet, JobParameterFormSet

def index(request):
    return HttpResponse("<h1>Welcome to the Minimal Job System Web Application</h1>")


class JobListView(ListView):
    model = Job
    ordering = ["date_created"]

    """
    def get_queryset(self):
        jobs = Job.objects.all()
        for job in jobs:
            #job.parameters = JobParameter.objects.filter(job=job)
            #job.refresh_from_db()
            print(job.parameters.all())
        return jobs
    """

    def get_context_data(self, **kwargs):
        context = super(JobListView, self).get_context_data(**kwargs)
        """
        for job in context['object_list']:
            parameters = JobParameter.objects.filter(job=job)
            #qs = context['object_list']
            #media = qs.aggregate(a=JobParameter.objects.filter(job=job))
            #print(parameters )
        """
        context['now'] = timezone.now()
        return context

class JobDetailView(DetailView):
    model = Job

class JobCreateView(CreateView):
    model = Job
    #form_class = JobForm
    success_url = reverse_lazy('jobs_list')
    fields = ['namespace', 'name', 'type', 'status']

    def get_context_data(self, **kwargs):
        context = super(JobCreateView, self).get_context_data(**kwargs)
        source_types = JobSource._meta.get_field('type').flatchoices
        luigi_workflow_type = next(
            (k for k, v in source_types if v == 'Luigi Workflow'), None
        )
        #context['job_templates'] = JobTemplateFormSet()
        context['job_templates'] = JobTemplate.objects.all()
        context['selected_job_templates'] = ['']
        if self.request.POST:
            context['selected_job_templates'] = self.request.POST["job_templates"]
            context['job_parameters'] = JobParameterFormSet(self.request.POST)
        else:
            #context['job_parameters'] = JobParameterFormSet(instance=Job.objects.get(id=11), queryset=JobParameter.objects.filter(job=Job.objects.filter(id=11)))
            context['job_parameters'] = JobParameterFormSet()

        return context

    def form_valid(self, form):
        context = self.get_context_data()
        job_parameters = context['job_parameters']

        #return super(JobCreateView, self).form_valid(form)
        print("b")

        # validate job form data (not only job_parameters)

        #print(job_parameters)
        #return super(JobCreateView, self).form_valid(form)

        with transaction.atomic():
            print(job_parameters)
            #job_parameters.instance = self.object
            if job_parameters.is_valid():
                self.object = form.save()

                job_parameters.instance = self.object
                job_parameters.save()
                return super(JobCreateView, self).form_valid(form)
            else:
                context.update({
                    'job_parameters': job_parameters
                })
        #return super(JobCreateView, self).form_valid(form)
        return self.render_to_response(context)


#if phones.is_valid():
# phones.instance = user
# phones.save()
#else:
# context.update({
# ‘phones’: phones
# })
# return self.render_to_response(context)


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
