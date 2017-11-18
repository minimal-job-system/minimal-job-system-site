from django.conf.urls import url, include
from rest_framework.urlpatterns import format_suffix_patterns
from .views import index, JobListView, JobDetailView, JobCreateView, JobUpdateView, JobDeleteView

urlpatterns = {
    url(r'index$', index, name="index"),
    #url(r'^admin/sync_job_tmpl$', sync_job_tmpl, name="sync_job_tmpl"),
    url(r'jobs/$', JobListView.as_view(), name="jobs_list"),
    url(r'jobs/create$', JobCreateView.as_view(), name="jobs_create"),
    url(r'jobs/(?P<pk>[0-9]+)/$', JobDetailView.as_view(), name='jobs_detail'),
    url(r'jobs/(?P<pk>[0-9]+)/update$', JobUpdateView.as_view(), name='jobs_update'),
    url(r'jobs/(?P<pk>[0-9]+)/delete$', JobDeleteView.as_view(), name='jobs_delete'),
}

urlpatterns = format_suffix_patterns(urlpatterns)
