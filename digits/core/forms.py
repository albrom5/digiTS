from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import ReadOnlyPasswordHashField

from digits.core import models


class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField(
        help_text=("Raw passwords are not stored, so there is no way to see "
                    "this user's password, but you can change the password "
                    "using <a href=\"../password/\">this form</a>.")
    )

    class Meta:
        model = models.User
        fields = ['first_name', 'last_name', 'email', 'is_active', 'is_staff',
            'companies', 'selected_company', 'role', 'password']


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
    company_responsible_name = forms.CharField(
        label='Nome do responsável da empresa no canteiro de trabalho',
        required=True
    )
    company_responsible_phone = forms.CharField(
        label='Telefone do responsável da empresa no canteiro de trabalho',
        required=True
    )

    class Meta:
        model = models.PreliminaryRiskAnalysis
        fields = [
            'activity_type', 'location', 'estimated_execution_time',
            'work_permission', 'company_responsible_name',
            'company_responsible_phone'
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
            'question', 'exists', 'details', 'form_of_control',
        ]


class SignForm(forms.Form):
    username = forms.EmailField(
        widget=forms.EmailInput(attrs={"autofocus": True})
    )
    password = forms.CharField(
        label='Senha',
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "current-password"}),
    )

    def __init__(self, *args, **kwargs):
        if 'user' in kwargs:
            self.user = kwargs.pop('user')
        super().__init__(*args, **kwargs)

    def clean(self):
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")

        if username is not None and password:
            user = authenticate(
                username=username, password=password
            )
            if user is None or user != self.user:
                raise forms.ValidationError('Credenciais incorretas')
