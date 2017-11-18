import abc, six
from django.conf.urls import url
from django.contrib import admin
from django.utils.html import format_html
from django.http import HttpResponse
from django.shortcuts import redirect
from .models import JobSource, JobTemplate, Job

import ast
from glob import glob


@six.add_metaclass(abc.ABCMeta)
class Tool():
    name = None
    icon = None

    @property
    def url(self):
        return "%s" % self.name

    @abc.abstractmethod
    def action(self, request, *args, **kwargs):
        pass

class TestTool(Tool):
    name = "test"
    icon = "unchecked"

    @property
    def url(self):
        return "%s?a=1" % self.name

    def action(self, request, *args, **kwargs):
        return HttpResponse(
            str({q_key: q_value for q_key, q_value in request.GET.items()})
        )

class JobTemplateSyncTool(Tool):
    name = "synchronize"
    icon = "upload"

    @property
    def url(self):
        return "%s" % self.name

    def action(self, request, *args, **kwargs):
        job_sources = JobSource.objects.all()
        source_types = JobSource._meta.get_field('type').flatchoices
        luigi_workflow_type = next(
            (k for k, v in source_types if v == 'Luigi Workflow'), None
        )
        for source in job_sources:
            if source.type != luigi_workflow_type:
                continue

            JobTemplate.objects.filter(type=luigi_workflow_type).delete()

            source_uri = source.uri

            file_list = []
            for file in glob(source_uri + "/*"):
                if not file.endswith(".py"):
                    continue

                with open(file,'r') as f:
                  ast_node = ast.parse(f.read())

                workflow_class_nodes = [
                    node for node in ast.walk(ast_node)
                    if isinstance(node, ast.ClassDef) and "WrapperTask" in [
                        base.attr for base in node.bases
                    ]
                ]

                for class_node in workflow_class_nodes:
                    #requires_func_node = [
                    #    node for node in ast.walk(class_node)
                    #    if isinstance(node, ast.FunctionDef) and node.name == "requires"
                    #][0]
                    
                    assign_nodes = [
                        node for node in ast.walk(class_node)
                        if isinstance(node, ast.Assign)
                    ]
                    parameters = {}
                    # search for luigi.Parameter assignments
                    # e.g. search_path = luigi.Parameter(default="")
                    for assign_node in assign_nodes:
                        if isinstance(assign_node.value, ast.Call):
                            if (
                                assign_node.value.func.value.id == "luigi" and
                                assign_node.value.func.attr == "Parameter"
                            ):
                                param_id = assign_node.targets[0].id
                                parameters[param_id] = None
                                for keyword_node in assign_node.value.keywords:
                                    if keyword_node.arg == "default":
                                        if isinstance(keyword_node.value, ast.NameConstant):
                                            parameters[param_id] = keyword_node.value.value
                                        if isinstance(keyword_node.value, ast.Str):
                                            parameters[param_id] = keyword_node.value.s

                    JobTemplate(
                        name=class_node.name,
                        type=source.type,
                        description=ast.get_docstring(class_node),
                        parameters=parameters
                    ).save()

        return redirect('..')

Tools = [TestTool(), JobTemplateSyncTool()]


admin.site.register(JobSource)

@admin.register(JobTemplate)
class JobTemplateAdmin(admin.ModelAdmin):
    object_tools = [
        JobTemplateSyncTool,
    ]

    def changelist_view(self, request, extra_context={}):
        extra_context['object_tools'] = self.object_tools
        return super(JobTemplateAdmin, self).changelist_view(request, extra_context=extra_context)

admin.site.register(Job)


admin_urls = admin.site.get_urls()
admin.site.get_urls = lambda: (
    [
        url(r'^(.+)/(.+)/%s/$' % tool.name, admin.site.admin_view(tool.action)) for tool in Tools
    ] +
    admin_urls
)

