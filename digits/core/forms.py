from django import forms

from digits.core import models


class RiskAnalysisForm(forms.ModelForm):
    activity_type = forms.CharField(
        label='Tipo de Atividade',
        required=True
    )
    location = forms.CharField(
        label='Local',
        required=True
    )
    estimated_execution_time = forms.CharField(
        label='Tempo previsto de execução',
        required=True
    )
    work_permission = forms.CharField(
        label=(
            'Permissão de trabalho / Acompanhamento de Técnico de Segurança do'
            ' Trabalho da contratada'
        ),
        required=True
    )

    class Meta:
        model = models.PreliminaryRiskAnalysis
        fields = [
            'activity_type', 'location', 'estimated_execution_time',
            'work_permission'
        ]


class RiskAnswerForm(forms.ModelForm):

    question = forms.CharField(
        label='',
        required=False,
    )
    exists = forms.BooleanField(
        label='',
        required=False,
        widget=forms.RadioSelect(
            choices=(
                (True, 'Sim'),
                (False, 'Não')
            )
        )
    )
    details = forms.CharField(
        label='',
        required=False,
    )
    form_of_control = forms.CharField(
        label='',
        required=False,
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        question_id = self.initial.get('question')
        self.question = models.RiskQuestion.objects.filter(
            id=question_id
        ).first()
        if self.question is not None:
            self.fields['question'].label = (
                f'{self.question.order}- {self.question.description}'
            )

    def clean_question(self):
        risk_question = models.DefaultRiskQuestion.objects.filter(
            default_risk_analysis__id=1,
            risk_question=self.question
        ).first()
        return risk_question

    def clean(self):
        data = self.cleaned_data
        exists = data.get('exists', False)
        details = data.get('details')
        if exists and not details:
            self.add_error('details', 'Informe quais os riscos')
        form_of_control = data.get('form_of_control')
        if exists and not form_of_control:
            self.add_error(
                'form_of_control', 'Informe a(s) forma(s) de controle'
            )

    class Meta:
        model = models.RiskAnswer
        fields = [
            'question', 'exists', 'details', 'form_of_control'
        ]
