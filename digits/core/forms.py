from django import forms

from digits.core import models


class RiskAnalysisForm(forms.ModelForm):
    
    class Meta:
        model = models.PreliminaryRiskAnalysis
        fields = [
            'activity_type', 'location', 'estimated_execution_time',
            'work_permission'
        ]


class RiskAnswerForm(forms.ModelForm):

    question = forms.CharField(
        label=''
    )
    exists = forms.BooleanField(
        label='',
        widget=forms.RadioSelect(
            choices=(
                (True, 'Sim'),
                (False, 'Não')
            )
        )
    )
    details = forms.CharField(
        label=''
    )
    form_of_control = forms.CharField(
        label=''
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        question_id = self.initial.get('question')
        question = models.RiskQuestion.objects.filter(id=question_id).first()
        if question is not None:
            self.fields['question'].label = f'{question.order}- {question.description}'

    class Meta:
        model = models.RiskAnswer
        fields = [
            'question', 'exists', 'details', 'form_of_control'
        ]
