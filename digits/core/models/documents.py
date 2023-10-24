from django.conf import settings
from django.db import models


class RiskQuestion(models.Model):
    ACCIDENT = 'ACI'
    BIOLOGICAL = 'BIO'
    PHYSICAL = 'FIS'
    CHEMICAL = 'QUI'
    CATEGORIES = (
        (ACCIDENT, 'Acidente'),
        (BIOLOGICAL, 'Biológico'),
        (PHYSICAL, 'Físico'),
        (CHEMICAL, 'Químico')

    )
    category = models.CharField(
        'Categoria do Risco', max_length=3, choices=CATEGORIES
    )
    order = models.PositiveSmallIntegerField('Ordem')
    description = models.CharField('Descrição', max_length=500)
    is_active = models.BooleanField('Ativa?', default=True)

    def __str__(self):
        return f'{self.order} - {self.description}'

    class Meta:
        verbose_name = 'Questâo de Risco'
        verbose_name_plural = 'Questões de Risco'


class DefaultRiskAnalysis(models.Model):
    description = models.CharField('Descrição', max_length=500)
    is_active = models.BooleanField('Ativa?', default=True)

    def __str__(self):
        return self.description

    class Meta:
        verbose_name = 'Análise de Risco Padrão'
        verbose_name_plural = 'Análises de Risco Padrão'


class DefaultRiskQuestion(models.Model):
    default_risk_analysis = models.ForeignKey(
        'core.DefaultRiskAnalysis', on_delete=models.CASCADE,
        verbose_name='Análise de Risco Padrão'
    )
    risk_question = models.ForeignKey(
        'core.RiskQuestion', on_delete=models.CASCADE,
        verbose_name='Questão de Risco'
    )

    def __str__(self):
        return f'{self.risk_question.order} - {self.risk_question.description}'

    class Meta:
        verbose_name = 'Questão da Análise de Risco Padrão'
        verbose_name_plural = 'Questões da Análise de Risco Padrão'


class PreliminaryRiskAnalysis(models.Model):
    REGISTERING = 'CAD'
    READY = 'PRT'
    EFFECTIVE = 'VIG'
    CANCELLED = 'CAN'
    STATUS = (
        (REGISTERING, 'Em cadastro'),
        (READY, 'Pronta para assinatura'),
        (EFFECTIVE, 'Vigente'),
        (CANCELLED, 'Cancelada')
    )
    company = models.ForeignKey(
        'core.Company', on_delete=models.CASCADE, verbose_name='Empresa'
    )
    create_date = models.DateTimeField('Data de emissão', auto_now_add=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.PROTECT,
        verbose_name='Criado por', related_name='created_risk_analysis'
    )
    last_update = models.DateTimeField('Última atualização', auto_now_add=True)
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.PROTECT,
        verbose_name='Atualizado por', related_name='updated_risk_analysis'
    )
    activity_type = models.CharField(
        'Tipo de Atividade', max_length=500, blank=True
    )
    location = models.CharField('Local', max_length=500, blank=True)
    estimated_execution_time = models.CharField(
        'Tempo previsto de execução', max_length=250, blank=True
    )
    work_permission = models.CharField(
        'Permissão de trabalho / Acompanhamento de Técnico de Segurança do '
        'Trabalho da contratada', max_length=250, blank=True
    )
    status = models.CharField('Situação', max_length=3, choices=STATUS)
    company_responsible_name = models.CharField(
        'Nome do responsável da empresa no canteiro de trabalho',
        max_length=250, blank=True
    )
    company_responsible_phone = models.CharField(
        'Telefone do responsável da empresa no canteiro de trabalho',
        max_length=20, blank=True
    )

    def user_can_sign(self, user):
        from digits.core.models.user import User
        allowed_roles = [
            User.TECHNICIAN, User.MANAGER, User.ENGINEER
        ]
        if user.role not in allowed_roles:
            return (False, 'Cargo do usuário não permite assinar este tipo de documento.')

        signature_type = None
        if user.role in User.EVALUATOR_ROLES:
            signature_type = RiskAnalysisSignature.EVALUATOR
        elif user.role in User.RESPONSIBLE_ROLES:
            signature_type = RiskAnalysisSignature.CONTRACT_RESPONSIBLE

        is_signed = self.signatures.filter(
                signature_type=signature_type
        ).exists()
        if is_signed:
            signature_types_dict = dict(RiskAnalysisSignature.TYPES)
            error_message = f'Documento já assinado pelo {signature_types_dict[signature_type]}.'
            return (False, error_message)

        return (True, 'OK')

    def __str__(self):
        title = (
            f'{self.company.name} - {self.activity_type} - '
            f'{self.create_date.strftime("%d/%m/%Y")}'
        )
        return title

    class Meta:
        verbose_name = 'Análise Preliminar de Risco'
        verbose_name_plural = 'Análises Preliminares de Risco'


class RiskAnswer(models.Model):
    preliminary_risk_analysis = models.ForeignKey(
        'core.PreliminaryRiskAnalysis', on_delete=models.CASCADE,
        verbose_name='Análise Preliminar de Risco', related_name='answers'
    )
    question = models.ForeignKey(
        'core.DefaultRiskQuestion', on_delete=models.PROTECT,
        verbose_name='Questão'
    )
    exists = models.BooleanField('Presente?', default=False)
    details = models.CharField('Qual(is)?', max_length=500, blank=True)
    form_of_control = models.CharField(
        'Forma(s) de Controle', max_length=500, blank=True
    )

    def __str__(self):
        exists = 'Sim' if self.exists else 'Não'
        title = (
            f'{self.question.risk_question.order} - '
            f'{self.question.risk_question.description}: {exists}'
        )
        return title


class RiskAnalysisSignature(models.Model):
    from digits.core.models.user import User

    EVALUATOR = 'AVA'
    CONTRACT_RESPONSIBLE = 'RES'
    TYPES = (
        (EVALUATOR, 'Avaliador'),
        (CONTRACT_RESPONSIBLE, 'Responsável pela Contratação')
    )
    preliminary_risk_analysis = models.ForeignKey(
        'core.PreliminaryRiskAnalysis', on_delete=models.CASCADE,
        verbose_name='Análise Preliminar de Risco', related_name='signatures'
    )
    signature_type = models.CharField(
        'Tipo de assinatura', max_length=3, choices=TYPES
    )
    signatory = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.PROTECT,
        verbose_name='Criado por'
    )
    signatory_role = models.CharField(
        'Cargo do Signatário', max_length=3, choices=User.ROLES
    )
    signature_date_time = models.DateTimeField(
        'Data de assinatura', blank=True, null=True
    )
    token = models.CharField(max_length=64, null=True, blank=True)

    def __str__(self):
        title = (
            f'{self.preliminary_risk_analysis} - {self.get_signature_type_display()} - '
            f'{self.signatory.get_full_name()}'
        )
        if self.signature_date_time is not None:
            f'{title}-{self.signature_date_time.strftime("%d/%m%Y %H:%M:%S")}'
        return title

    class Meta:
        verbose_name = 'Assinatura da Análise de Risco'
        verbose_name_plural = 'Assinaturas da Análise de Risco'
