# Generated by Django 2.0.6 on 2018-06-18 02:31

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Atividade',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=200)),
                ('descricao', models.TextField()),
            ],
            options={
                'verbose_name': 'Atividade',
                'verbose_name_plural': 'Atividades',
            },
        ),
        migrations.CreateModel(
            name='AtividadeDiaria',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hora_inicio', models.TimeField()),
                ('hora_fim', models.TimeField(blank=True, null=True)),
                ('horas_alocadas_minutos', models.IntegerField(blank=True, null=True)),
                ('atividade', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='work_hour.Atividade', verbose_name='atividades')),
            ],
            options={
                'verbose_name': 'Atividade Diária',
                'verbose_name_plural': 'Atividades Diárias',
            },
        ),
        migrations.CreateModel(
            name='Cliente',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=200)),
                ('cnpj', models.TextField()),
                ('telefone', models.TextField(max_length=13)),
                ('valor_plano', models.DecimalField(decimal_places=2, max_digits=8)),
            ],
            options={
                'verbose_name': 'Cliente',
                'verbose_name_plural': 'Clientes',
            },
        ),
        migrations.CreateModel(
            name='DiaDaSemana',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=15)),
                ('peso_hora', models.DecimalField(decimal_places=2, max_digits=4)),
            ],
            options={
                'verbose_name': 'Dia da Semana',
                'verbose_name_plural': 'Dias da Semana',
            },
        ),
        migrations.CreateModel(
            name='Feriado',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=15)),
                ('data', models.DateField()),
                ('fixo', models.BooleanField()),
            ],
            options={
                'verbose_name': 'Feriado',
                'verbose_name_plural': 'Feriados',
            },
        ),
        migrations.CreateModel(
            name='RegistroDiario',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data', models.DateField()),
                ('entrada_1', models.TimeField(blank=True, null=True)),
                ('entrada_2', models.TimeField(blank=True, null=True)),
                ('entrada_3', models.TimeField(blank=True, null=True)),
                ('saida_1', models.TimeField(blank=True, null=True)),
                ('saida_2', models.TimeField(blank=True, null=True)),
                ('saida_3', models.TimeField(blank=True, null=True)),
                ('horas_trabalhadas', models.IntegerField()),
                ('observacoes', models.TextField(blank=True, null=True)),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Horário Diário',
                'verbose_name_plural': 'Horários',
            },
        ),
        migrations.AddField(
            model_name='atividadediaria',
            name='cliente',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='work_hour.Cliente', verbose_name='atividades'),
        ),
        migrations.AddField(
            model_name='atividadediaria',
            name='registro_diario',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='work_hour.RegistroDiario', verbose_name='atividades'),
        ),
    ]
