import abc
import ast
from glob import glob
import os
import six
import sys

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

            JobTemplate.objects.filter(type=job_source.type).delete()

            errors = sync_job_source(job_source)
            if len(errors) > 0:
                for error in errors:
                    messages.error(request, error)
                break

        if len(errors) == 0:
            messages.success(request, "Synchronization was successful!")


def sync_job_source(job_source):
    errors = []

    def error_callback(ex):
        errors.append(ex)

    for root, dirs, files in os.walk(
        job_source.uri, onerror=error_callback, topdown=True
    ):
        dirs = []  # stop recursion
        for file_name in files:
            file_path = os.path.join(root, file_name)

            if not file_path.endswith(".py"):
                continue

            with open(file_path, 'r') as fp:
                ast_node = ast.parse(fp.read())

            workflow_class_nodes = []
            for node in ast.walk(ast_node):
                if not isinstance(node, ast.ClassDef):
                    continue

                base_ids = [
                    base.id for base in node.bases
                    if isinstance(base, ast.Name)
                ]
                if any("JobSystemWorkflow" in id for id in base_ids):
                    workflow_class_nodes.append(node)

            parameter_types = \
                JobParameterDeclaration._meta.get_field('type').flatchoices

            for class_node in workflow_class_nodes:
                namespace = None
                parameters = []

                prev_child_node = None
                for child_node in ast.iter_child_nodes(class_node):
                    # search for luigi.Parameter assignments
                    # e.g. search_path = luigi.Parameter(default="")
                    if isinstance(child_node, ast.Assign):
                        assign_node = child_node
                        if (
                            isinstance(assign_node.value, ast.Str) and
                            assign_node.targets[0].id == "task_namespace"
                        ):
                            namespace = assign_node.value.s

                        if (
                            isinstance(assign_node.value, ast.Call) and
                            assign_node.value.func.value.id == "luigi"
                        ):
                            parameter = extract_parameter(
                                assign_node, parameter_types
                            )
                            parameters.append(parameter)

                    # search for docstrings
                    # Python does not treat strings defined IMMEDIATELY
                    # after a global definition as a docstring!
                    # Sphinx, however, does do so - which is certainly
                    # not a bad practice
                    if (
                        isinstance(child_node, ast.Expr)
                    ):
                        if (
                            isinstance(prev_child_node, ast.Assign) and
                            isinstance(prev_child_node.value, ast.Call) and
                            prev_child_node.value.func.value.id == "luigi"
                        ):
                            expr_node = child_node
                            if isinstance(expr_node.value, ast.Str):
                                parameter["description"] = \
                                    expr_node.value.s

                    prev_child_node = child_node

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
                        description=parameter["description"],
                        type=parameter["type"],
                        default=str(parameter["default"])
                    ).save()

    return errors


def extract_parameter(assign_node, parameter_types):
    parameter = {
        "name": None,
        "description": None,
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
            if sys.version_info.major == 2:
                if isinstance(keyword_node.value, ast.Name):
                    parameter["default"] = keyword_node.value.id
            if sys.version_info.major == 3:
                if isinstance(keyword_node.value, ast.NameConstant):
                    parameter["default"] = keyword_node.value.value

            if isinstance(keyword_node.value, ast.Str):
                parameter["default"] = keyword_node.value.s

    return parameter
