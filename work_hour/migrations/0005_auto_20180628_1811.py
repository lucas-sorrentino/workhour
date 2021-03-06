# Generated by Django 2.0.6 on 2018-06-28 18:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('work_hour', '0004_auto_20180627_2243'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Relatorio',
        ),
        migrations.CreateModel(
            name='RelatorioAtividades',
            fields=[
            ],
            options={
                'verbose_name': 'Relatório Atividades',
                'verbose_name_plural': 'Relatórios Atividades',
                'proxy': True,
                'indexes': [],
            },
            bases=('work_hour.atividadediaria',),
        ),
        migrations.CreateModel(
            name='RelatorioHorasTrabalhadas',
            fields=[
            ],
            options={
                'verbose_name': 'Relatório Horas',
                'verbose_name_plural': 'Relatórios Horas',
                'proxy': True,
                'indexes': [],
            },
            bases=('work_hour.registrodiario',),
        ),
    ]
