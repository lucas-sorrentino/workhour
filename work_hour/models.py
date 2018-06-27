from datetime import time, datetime

from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from django.db import models

# Create your models here.

class RegistroDiario(models.Model):

    data = models.DateField()
    entrada_1 = models.TimeField(null=True, blank=True)
    saida_1 = models.TimeField(null=True, blank=True)
    entrada_2 = models.TimeField(null=True, blank=True)
    saida_2 = models.TimeField(null=True, blank=True)
    entrada_3 = models.TimeField(null=True, blank=True)
    saida_3 = models.TimeField(null=True, blank=True)
    horas_trabalhadas = models.IntegerField(null=True, blank=True)
    observacoes = models.TextField(null=True, blank=True)
    usuario = models.ForeignKey(User, on_delete=models.PROTECT, null=True, blank=True)

    class Meta:
        verbose_name = 'Horário Diário'
        verbose_name_plural = 'Horários'


    def __str__(self):
        return '%s' % self.data


    @property
    def horas_totais(self):
        hora = '-'
        if self.saida_1 and self.entrada_1 and not self.entrada_2 and not self.saida_2:
            time1 = time.strftime(self.saida_1, '%Y-%m-%d %H:%M:%S')
            time2 = time.strftime(self.entrada_1, '%Y-%m-%d %H:%M:%S')

            hora = datetime.strptime(time1, '%Y-%m-%d %H:%M:%S') - datetime.strptime(time2, '%Y-%m-%d %H:%M:%S')
            # hora.strftime(format['%H:%M', t])
        return hora


class Cliente(models.Model):

    nome = models.CharField(max_length=200)
    cnpj = models.CharField(max_length=20)
    telefone = models.CharField(max_length=13)
    valor_plano = models.DecimalField(max_digits=8, decimal_places=2)

    class Meta:
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'

    def __str__(self):
        return '%s' % self.nome


class Atividade(models.Model):

    nome = models.CharField(max_length=200)
    descricao = models.TextField()

    class Meta:
        verbose_name = 'Atividade'
        verbose_name_plural = 'Atividades'

    def __str__(self):
        return '%s' % self.nome


class AtividadeDiaria(models.Model):

    hora_inicio = models.TimeField()
    hora_fim = models.TimeField(blank=True, null=True)
    horas_alocadas_minutos = models.IntegerField(blank=True, null=True)
    atividade = models.ForeignKey(Atividade, verbose_name='atividade', on_delete=models.PROTECT)
    registro_diario = models.ForeignKey(RegistroDiario, verbose_name='horario', on_delete=models.PROTECT)
    cliente = models.ForeignKey(Cliente, verbose_name='cliente', on_delete=models.PROTECT)


    class Meta:
        verbose_name = 'Atividade Diária'
        verbose_name_plural = 'Atividades Diárias'

    def __str__(self):
        return '%s - %s' % (self.cliente.nome, self.atividade.nome)

    @property
    def nome_atividade(self):
        return '%s' % (self.atividade.nome)

    @property
    def nome_cliente(self):
        return '%s' % (self.cliente.nome)

    @property
    def data(self):
        return '%s' % (self.registro_diario.data)

class DiaDaSemana(models.Model):

    nome = models.CharField(max_length=15)
    peso_hora = models.DecimalField(max_digits=4, decimal_places=2)


    class Meta:
        verbose_name = 'Dia da Semana'
        verbose_name_plural = 'Dias da Semana'

    def __str__(self):
        return '%s' % self.nome


class Feriado(models.Model):
    nome = models.CharField(max_length=15)
    data = models.DateField()
    fixo = models.BooleanField()

    class Meta:
        verbose_name = 'Feriado'
        verbose_name_plural = 'Feriados'

    def __str__(self):
        return '%s' % self.nome

