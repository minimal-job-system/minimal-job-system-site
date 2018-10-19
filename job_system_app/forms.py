from django import forms
from django.forms import ModelForm, inlineformset_factory

from job_system_api.models import Job, JobParameter


class JobForm(ModelForm):
    class Meta:
        model = Job
        exclude = ()
        widgets = {
            field: forms.HiddenInput()
            for field in ['type', 'status', 'progress', 'owner']
        }


class JobParameterForm(ModelForm):
    job_id = forms.ModelChoiceField(queryset=Job.objects.all(), required=False)

    class Meta:
        model = JobParameter
        exclude = ()
        widgets = {
            field: forms.HiddenInput() for field in ['type', 'value']
        }


JobParameterFormSet = inlineformset_factory(
    Job, JobParameter, form=JobParameterForm, extra=0
)
