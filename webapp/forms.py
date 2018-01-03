from django import forms
from django.forms import ModelForm, inlineformset_factory
from .models import Job, JobParameter


class JobForm(ModelForm):
    class Meta:
        model = Job
        exclude = ()
        widgets = {
            field: forms.HiddenInput()
            for field in ['type', 'status', 'progress']
        }


class JobParameterForm(ModelForm):
    job_id = forms.ModelChoiceField(queryset=Job.objects.all(), required=False)

    class Meta:
        model = JobParameter
        exclude = ()
        widgets = {
            field: forms.HiddenInput() for field in ['type']
        }


JobParameterFormSet = inlineformset_factory(
    Job, JobParameter, form=JobParameterForm, extra=0
)
