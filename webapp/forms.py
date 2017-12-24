from django import forms
from django.forms import Form, ModelForm, formset_factory, inlineformset_factory
from .models import JobSource, JobTemplate, Job, JobParameter

class JobTemplateForm(Form):
    job_template = forms.ChoiceField(
        widget=forms.Select(attrs={'onchange': "this.form.submit()"}),
        choices=(
            [("", "---------")] +
            list(
                (templ.id, templ.name)
                for templ in JobTemplate.objects.all()
                if templ.type in [
                    # IF NOT 'CONFIDENTIAL'
                    k for k, v in JobSource._meta.get_field('type').choices
                    if v == 'Luigi Workflow'
                ]
            )
        ),
        initial="",
        required=True
    )

class JobParameterForm(ModelForm):
    class Meta:
        model = JobParameter
        exclude = ()

JobTemplateFormSet = formset_factory(JobTemplateForm)
JobParameterFormSet = inlineformset_factory(Job, JobParameter, form=JobParameterForm, extra=1, can_delete=False)
