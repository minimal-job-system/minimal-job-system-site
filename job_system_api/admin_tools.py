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

from job_system_api.models import JobSource, JobTemplate, \
    JobParameterDeclaration, JobParameterDeclarationChoice


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

                child_nodes = list(ast.iter_child_nodes(class_node))
                for idx, child_node in enumerate(child_nodes):
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
                            hasattr(assign_node.value.func, 'value') and
                            assign_node.value.func.value.id == "luigi"
                        ):
                            parameter = extract_parameter(
                                assign_node, parameter_types
                            )
                            parameters.append(parameter)

                            # search for annotations
                            # this feature has no PEP specification
                            if (
                                idx-1 >= 0 and
                                isinstance(child_nodes[idx-1], ast.Expr)
                            ):
                                expr_node = child_nodes[idx-1]
                                if isinstance(expr_node.value, ast.Dict):
                                    annotations = {}
                                    for k, v in zip(
                                        expr_node.value.keys,
                                        expr_node.value.values
                                    ):
                                        if isinstance(v, ast.List):
                                            parameter["annotations"][k.s] = [
                                                item.s for item in v.elts
                                            ]
                                        else:
                                            parameter["annotations"][k.s] = v.s

                            # search for docstrings
                            # Python does not treat strings defined IMMEDIATELY
                            # after a global definition as a docstring!
                            # Sphinx, however, does do so - which is certainly
                            # not a bad practice
                            if (
                                idx + 1 < len(child_nodes) and
                                isinstance(child_nodes[idx+1], ast.Expr)
                            ):
                                expr_node = child_nodes[idx+1]
                                if isinstance(expr_node.value, ast.Str):
                                    parameter["description"] = \
                                        expr_node.value.s

                job_template = JobTemplate(
                    namespace=namespace,
                    name=class_node.name,
                    type=job_source.type,
                    description=ast.get_docstring(class_node)
                )
                job_template.save()
                for parameter in parameters:
                    job_param_decl = JobParameterDeclaration(
                        template=job_template,
                        name=parameter["name"],
                        description=parameter["description"],
                        type=parameter["type"],
                        default=str(
                            parameter["annotations"].get("default") or
                            parameter["default"]
                        ),
                        is_hidden=(
                            parameter["annotations"].get("is_hidden") or False
                        ),
                        is_dangerous=(
                            parameter["annotations"].get("is_dangerous") or
                            False
                        )
                    )
                    job_param_decl.save()

                    param_choices = parameter["annotations"].get("choices")
                    if param_choices:
                        for param_choice in param_choices:
                            JobParameterDeclarationChoice(
                                param_declaration=job_param_decl,
                                value=param_choice
                            ).save()

    return errors


def extract_parameter(assign_node, parameter_types):
    parameter = {
        "name": None,
        "description": None,
        "type": None,
        "default": None,
        'annotations': {}
    }
    parameter["name"] = assign_node.targets[0].id

    rev_parameter_types = {v: k for k, v in dict(parameter_types).items()}
    if assign_node.value.func.attr == "IntParameter":
        parameter["type"] = rev_parameter_types.get("Integer", None)
        parameter["default"] = ""
    if assign_node.value.func.attr == "FloatParameter":
        parameter["type"] = rev_parameter_types.get("Decimal", None)
        parameter["default"] = ""
    if assign_node.value.func.attr == "BoolParameter":
        parameter["type"] = rev_parameter_types.get("Boolean", None)
        parameter["default"] = "false"
    if assign_node.value.func.attr == "DateSecondParameter":
        parameter["type"] = rev_parameter_types.get("Datetime", None)
        parameter["default"] = ""
    if assign_node.value.func.attr in [
        "Parameter", "ChoiceParameter", "TaskParameter", "DictParameter"
    ]:
        parameter["type"] = rev_parameter_types.get("String", None)
        parameter["default"] = ""

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
