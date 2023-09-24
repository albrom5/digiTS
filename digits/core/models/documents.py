from django.db import models


class PreliminaryRiskAnalysis(models.Model):
    company = models.ForeignKey(
        'core.Company', on_delete=models.CASCADE, verbose_name='Empresa'
    )
    create_date = models.DateTimeField('Data de emissão', auto_now_add=True)

    class Meta:
        verbose_name = 'Análise Preliminar de Risco'
        verbose_name_plural = 'Análises Preliminares de Risco'
