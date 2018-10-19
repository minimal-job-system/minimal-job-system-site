from django.conf.urls import url, include
from rest_framework.urlpatterns import format_suffix_patterns

from job_system_api.views import JobListView, JobDetailsView
from job_system_api.views import JobTemplateListView, JobTemplateDetailsView
from job_system_api.views import JobParameterListView, JobParameterDetailsView
from job_system_api.views import JobLogEntryListView, JobLogEntryDetailsView


urlpatterns = {
    url(r'^jobtemplates/$', JobTemplateListView.as_view(), name="jobtemplate_list"),
    url(r'^jobtemplates/(?P<pk>[0-9]+)/$', JobTemplateDetailsView.as_view(), name="jobtemplate_details"),
    url(r'^jobs/$', JobListView.as_view(), name="job_list"),
    url(r'^jobs/(?P<pk>[0-9]+)/$', JobDetailsView.as_view(), name="job_details"),
    url(r'^jobs/(?P<job_id>[0-9]+)/parameters/$', JobParameterListView.as_view(), name="job_parameter_list"),
    url(r'^jobs/(?P<job_id>[0-9]+)/parameters/(?P<pk>[0-9]+)/$', JobParameterDetailsView.as_view(), name="job_parameter_details"),
    url(r'^jobs/(?P<job_id>[0-9]+)/logs/$', JobLogEntryListView.as_view(), name="job_log_list"),
    url(r'^jobs/(?P<job_id>[0-9]+)/logs/(?P<pk>[0-9]+)/$', JobLogEntryDetailsView.as_view(), name="job_log_details"),
    # url(r'^jobs/(?P<pk>[0-9]+)/update$', JobCreateView.as_view(), name='jobs_create'),
}

urlpatterns = format_suffix_patterns(urlpatterns)
