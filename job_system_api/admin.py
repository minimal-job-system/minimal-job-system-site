from django.conf.urls import url
from django.contrib import admin
from django.utils.html import format_html
from django.shortcuts import redirect

from job_system_api.admin_tools import SyncJobSourcesTool
from job_system_api.models import JobSource, JobTemplate, Job


class ToolModelAdmin(admin.ModelAdmin):
    tools = []

    def get_urls(self):
        urls = super(ToolModelAdmin, self).get_urls()
        tool_urls = [tool.get_url() for tool in self.tools]
        return tool_urls + urls

    def changelist_view(self, request, extra_context={}):
        extra_context['object_tools'] = self.tools
        return super(ToolModelAdmin, self).changelist_view(
            request, extra_context=extra_context
        )


sync_job_sources_tool = SyncJobSourcesTool()


@admin.register(JobSource)
class JobSourceAdmin(admin.ModelAdmin):
    actions = [sync_job_sources_tool.action, ]


@admin.register(JobTemplate)
class JobTemplateAdmin(ToolModelAdmin):
    tools = [sync_job_sources_tool, ]


admin.site.register(Job)
