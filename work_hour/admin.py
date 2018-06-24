from django.contrib import admin
from import_export import resources
from reversion.admin import VersionAdmin
from admin_reports import Report, register

from work_hour.ImportExportVersionModelAdmin import ImportExportVersionModelAdmin
from work_hour.models import RegistroDiario, Cliente, Atividade, AtividadeDiaria, DiaDaSemana, Feriado


class RegistroDiarioResource(resources.ModelResource):

    class Meta:
        model = RegistroDiario


class ClienteResource(resources.ModelResource):

    class Meta:
        model = Cliente


class AtividadeResource(resources.ModelResource):

    class Meta:
        model = Atividade


class AtividadeDiariaResource(resources.ModelResource):

    class Meta:
        model = AtividadeDiaria


class DiaDaSemanaResource(resources.ModelResource):

    class Meta:
        model = DiaDaSemana


class FeriadoResource(resources.ModelResource):

    class Meta:
        model = Feriado


@admin.register(RegistroDiario)
class RegistroDiarioAdmin(ImportExportVersionModelAdmin):
    resource_class = RegistroDiarioResource
    list_display = ("data", "horas_trabalhadas", "observacoes")
    # list_filter = ("")
    search_fields = ("data", "observacoes")
    exclude = ("horas_trabalhadas", "usuario")


@admin.register(Cliente)
class ClienteAdmin(ImportExportVersionModelAdmin):
    resource_class = ClienteResource
    list_display = ("nome", "cnpj", "telefone")
    list_filter = ("nome", "cnpj")
    search_fields = ("nome", "cnpj")


@admin.register(Atividade)
class AtividadeAdmin(ImportExportVersionModelAdmin):
    resource_class = AtividadeResource
    list_display = ("nome", "descricao")
    list_filter = ("nome", "descricao")
    search_fields = ("nome", "descricao")


@admin.register(AtividadeDiaria)
class AtividadeDiariaAdmin(ImportExportVersionModelAdmin):
    resource_class = AtividadeDiariaResource
    list_display = ("data", "nome_atividade", "nome_cliente",)
    # list_filter = ("",)
    # search_fields = ("",)


@admin.register(DiaDaSemana)
class DiaDaSemanaAdmin(ImportExportVersionModelAdmin):
    resource_class = DiaDaSemanaResource
    list_display = ("nome", "peso_hora",)
    list_filter = ("nome",)
    search_fields = ("nome",)

@admin.register(Feriado)
class FeriadoAdmin(ImportExportVersionModelAdmin):
    resource_class = FeriadoResource
    list_display = ("nome", "data", "fixo",)
    list_filter = ("nome", "data")
    search_fields = ("nome",)

@register()
class MyReport(Report):
    def aggregate(self, **kwargs):
        return [
            dict([(k, v) for v, k in enumerate('abcdefgh')]),
            dict([(k, v) for v, k in enumerate('abcdefgh')]),
        ]

