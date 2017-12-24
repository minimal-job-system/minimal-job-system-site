import abc
import ast
from glob import glob
import six

from django.conf.urls import url
from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import redirect

from .models import JobSource, JobTemplate, JobParameterDeclaration


@six.add_metaclass(abc.ABCMeta)
class Tool():
    name = None
    icon = None
    description = None

    def __init__(self):
        self.action.short_description = self.description

    @property
    def location(self):
        return "tools/%s/" % self.__class__.__name__.lower()

    def get_url(self):
        return url(
            r'^tools/%s/$' % self.__class__.__name__.lower(),
            lambda request: self.tool(request),
            name="tools_%s" % self.__class__.__name__.lower()
        )

    def tool(self, request):
        self.action(None, request, [])
        return redirect('../..')

    @abc.abstractmethod
    def action(modeladmin, request, queryset):
        pass

class PrintJobSourcesTool(Tool):
    name = "Print job sources"
    icon = "unchecked"
    description = "Print selected job sources"

    def tool(self, request):
        self.action(None, request, JobSource.objects.all())
        return redirect('../..')

    @staticmethod
    def action(modeladmin, request, queryset):
        for job_source in queryset:
            print(job_source)

class SyncJobSourcesTool(Tool):
    name = "Synchronize job sources"
    icon = "unchecked"
    description = "Synchronize selected job sources"

    def tool(self, request):
        self.action(None, request, JobSource.objects.all())
        return redirect('../..')

    @staticmethod
    def action(modeladmin, request, queryset):
        source_types = JobSource._meta.get_field('type').flatchoices
        luigi_workflow_type = next(
            (k for k, v in source_types if v == 'Luigi Workflow'), None
        )
        for job_source in queryset:
            if job_source.type != luigi_workflow_type:
                continue

            JobTemplate.objects.filter(type=luigi_workflow_type).delete()

            job_source_uri = job_source.uri

            file_list = []
            for file in glob(job_source_uri + "/*"):
                if not file.endswith(".py"):
                    continue

                with open(file,'r') as fp:
                  ast_node = ast.parse(fp.read())

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

                    parameter_types = JobParameterDeclaration._meta.get_field('type').flatchoices
                    assign_nodes = [
                        node for node in ast.walk(class_node)
                        if isinstance(node, ast.Assign)
                    ]
                    namespace = None
                    parameters = []
                    # search for luigi.Parameter assignments
                    # e.g. search_path = luigi.Parameter(default="")
                    for assign_node in assign_nodes:
                        if isinstance(assign_node.value, ast.Str):
                            if assign_node.targets[0].id == "task_namespace":
                                namespace = assign_node.value.s
                        if isinstance(assign_node.value, ast.Call):
                            if assign_node.value.func.value.id == "luigi":
                                parameter = {
                                    "name": None,
                                    "type": None,
                                    "default": None
                                }
                                parameter["name"] = assign_node.targets[0].id

                                search_type = None
                                if assign_node.value.func.attr == "IntParameter":
                                    search_type = "Integer"
                                if assign_node.value.func.attr == "FloatParameter":
                                    search_type = "Decimal"
                                if assign_node.value.func.attr == "BoolParameter":
                                    search_type = "Boolean"
                                if assign_node.value.func.attr == "DateSecondParameter":
                                    search_type = "Datetime"
                                if assign_node.value.func.attr == "Parameter":
                                    search_type = "String"

                                parameter["type"] = next(
                                    (k for k, v in parameter_types if v == search_type), None
                                )

                                for keyword_node in assign_node.value.keywords:
                                    if keyword_node.arg == "default":
                                        if isinstance(keyword_node.value, ast.NameConstant):
                                            parameter["default"] = keyword_node.value.value
                                        if isinstance(keyword_node.value, ast.Str):
                                            parameter["default"] = keyword_node.value.s
                                parameters.append(parameter)

                    job_template = JobTemplate(
                        namespace=namespace,
                        name=class_node.name,
                        type=job_source.type,
                        description=ast.get_docstring(class_node)
                    )
                    job_template.save()
                    for parameter in parameters:
                        JobParameterDeclaration(
                            template=job_template,
                            name=parameter["name"],
                            type=parameter["type"],
                            default=str(parameter["default"])
                        ).save()

            messages.success(request, "Synchronization was successful!")
