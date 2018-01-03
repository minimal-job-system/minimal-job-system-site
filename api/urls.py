from django.conf.urls import url, include
from rest_framework.urlpatterns import format_suffix_patterns
from .views import JobListView, JobCreateView, JobDetailsView
from .views import JobTemplateCreateView, JobTemplateDetailsView

urlpatterns = {
    url(r'^jobtemplates/$', JobTemplateCreateView.as_view(), name="jobtemplate_create"),
    url(r'^jobtemplates/(?P<pk>[0-9]+)/$', JobTemplateDetailsView.as_view(), name="jobtemplate_details"),
    url(r'^jobs/$', JobListView.as_view(), name="job_list"),
    url(r'^jobs/(?P<pk>[0-9]+)/$', JobDetailsView.as_view(), name="job_details"),
    # url(r'^jobs/(?P<pk>[0-9]+)/update$', JobCreateView.as_view(), name='jobs_create'),
}

urlpatterns = format_suffix_patterns(urlpatterns)
