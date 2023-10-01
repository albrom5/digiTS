from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.core.mail import send_mail
from django.db import models

from digits.core.managers import UserManager

from .abstract import TimeStampedModel


class User(AbstractBaseUser, PermissionsMixin):
    ENGINEER = 'ENG'
    ADMINISTRATOR = 'ADM'
    MANAGER = 'GER'
    TECHNICIAN = 'TEC'

    ROLES = (
        (ENGINEER, 'Engenheiro'),
        (ADMINISTRATOR, 'Administrador'),
        (MANAGER, 'Gerente'),
        (TECHNICIAN, 'Técnico'),
    )
    email = models.EmailField('email', unique=True)
    first_name = models.CharField('nome', max_length=30, blank=True)
    last_name = models.CharField('sobrenome', max_length=60, blank=True)
    date_joined = models.DateTimeField('data de cadastro', auto_now_add=True)
    is_active = models.BooleanField('ativo', default=True)
    is_staff = models.BooleanField(
        'Pode acessar o painel de administração?',
        default=False,
        help_text='Define se o usuário pode acessar o painel de administração.',
    )
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    has_changed_password = models.BooleanField(default=False)
    companies = models.ManyToManyField(
        'core.Company', blank=True, verbose_name='Empresas'
    )
    selected_company = models.ForeignKey(
        'core.Company', on_delete=models.SET_NULL, blank=True, null=True,
        verbose_name='Empresa selecionada', related_name='selected_users'
    )
    role = models.CharField('Cargo', max_length=3, choices=ROLES, blank=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def get_full_name(self):
        '''
        Retorna o nome completo do usuário
        '''
        full_name = f'{self.first_name} {self.last_name}'
        return full_name.strip()

    def get_short_name(self):
        '''
        Retorna o primeiro nome do usuário
        '''
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        '''
        Envia email ao usuário
        '''
        send_mail(subject, message, from_email, [self.email], **kwargs)

    class Meta:
        verbose_name = 'usuário'
        verbose_name_plural = 'usuários'


class Company(TimeStampedModel):
    name = models.CharField('nome', max_length=500)
    cnpj = models.CharField(max_length=18)

    def __str__(self):
        return f'{self.name} - {self.cnpj}'

    class Meta:
        verbose_name = 'empresa'
        verbose_name_plural = 'empresas'
