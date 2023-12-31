# Generated by Django 4.2.5 on 2023-10-25 15:06

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0005_preliminaryriskanalysis_company_responsible_name_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="preliminaryriskanalysis",
            name="last_update",
            field=models.DateTimeField(
                auto_now=True, verbose_name="Última atualização"
            ),
        ),
        migrations.AlterField(
            model_name="preliminaryriskanalysis",
            name="status",
            field=models.CharField(
                choices=[
                    ("CAD", "Em cadastro"),
                    ("PRT", "Pronta para assinatura"),
                    ("VIG", "Vigente"),
                    ("CAN", "Cancelada"),
                    ("ASS", "Assinada"),
                ],
                max_length=3,
                verbose_name="Situação",
            ),
        ),
    ]
