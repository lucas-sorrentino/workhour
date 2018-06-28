from datetime import datetime, timedelta, time

from django.contrib import admin
from django.contrib.admin import AdminSite, ModelAdmin
from django.db.models import Count, Sum
from django.template.response import TemplateResponse
from django.urls import path
from import_export import resources
from reversion.admin import VersionAdmin
from admin_reports import Report, register

from work_hour.ImportExportVersionModelAdmin import ImportExportVersionModelAdmin
from work_hour.models import RegistroDiario, Cliente, Atividade, AtividadeDiaria, DiaDaSemana, Feriado, \
    RelatorioHorasTrabalhadas, RelatorioAtividades


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
class RegistroDiarioAdmin(ImportExportVersionModelAdmin, ModelAdmin):
    resource_class = RegistroDiarioResource
    list_display = ("data", "horas_totais", "observacoes")
    # list_filter = ("")
    search_fields = ("data", "observacoes")
    exclude = ("horas_trabalhadas", "usuario")

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(usuario=request.user)

    def save_model(self, request, instance, form, change):
        usuario = request.user
        instance = form.save(commit=False)
        if not change or not instance.usuario:
            instance.usuario = usuario
        instance.save()
        form.save_m2m()
        return instance


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
class AtividadeDiariaAdmin(ImportExportVersionModelAdmin, ModelAdmin):
    resource_class = AtividadeDiariaResource
    list_display = ("data", "nome_atividade", "nome_cliente",)
    # list_filter = ("",)
    search_fields = ("atividade",)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(registro_diario__usuario=request.user)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "registro_diario":
            if not request.user.is_superuser:
                kwargs["queryset"] = RegistroDiario.objects.filter(usuario=request.user)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


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


@admin.register(RelatorioHorasTrabalhadas)
class RelatorioHorasAdmin(ModelAdmin):
    change_list_template = 'admin/work_hour/templates/relatorio.html'
    # date_hierarchy = 'created'

    list_filter = (
        'usuario',
    )

    def queryset(self, request):
        qs = super(RelatorioHorasAdmin, self).queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(usuario=request.user)

    def changelist_view(self, request, extra_context=None):
        response = super().changelist_view(
            request,
            extra_context=extra_context,
        )
        try:
            qs = response.context_data['cl'].queryset
        except (AttributeError, KeyError):
            return response

        lista = []
        if request.user.is_superuser:
            horarios = RegistroDiario.objects.all()
        else:
            horarios = RegistroDiario.objects.filter(usuario=request.user).all()
        horas_totais = timedelta(hours=0, minutes=0)
        for horario in horarios:
            dado = None
            if len(lista) > 0:
                dado = [{'index': lista.index(item), 'item': item} for item in lista if item["usuario"] == horario.usuario.username]
            if dado:
                if not isinstance(horario.horas_totais, str) and not isinstance(dado[0]['item']['horas_trabalhadas'], str):
                    data = {
                        'usuario': horario.usuario.username,
                        'horas_trabalhadas': dado[0]['item']['horas_trabalhadas'] + horario.horas_totais
                    }
                    lista.append(data)
                    lista.pop(dado[0]['index'])
            else:
                data = {
                    'usuario': horario.usuario.username,
                    'horas_trabalhadas': horario.horas_totais
                }
                lista.append(data)
            if not isinstance(horario.horas_totais, str):
                horas_totais += horario.horas_totais

        response.context_data['summary'] = lista

        response.context_data['summary_total'] = {
            'total': horas_totais
        }

        horas_previstas = len(horarios) * timedelta(hours=8, minutes=0)

        response.context_data['saldo'] = {'saldo': str(horas_totais - horas_previstas)}

        return response


@admin.register(RelatorioAtividades)
class RelatorioAtividadesAdmin(ModelAdmin):
    change_list_template = 'admin/work_hour/templates/relatorio_atividades.html'
    # date_hierarchy = 'created'

    # def queryset(self, request):
    #     qs = super(RelatorioAtividades, self).queryset(request)
    #     if request.user.is_superuser:
    #         return qs
    #     return qs.filter(usuario=request.user)

    def changelist_view(self, request, extra_context=None):
        response = super().changelist_view(
            request,
            extra_context=extra_context,
        )
        try:
            qs = response.context_data['cl'].queryset
        except (AttributeError, KeyError):
            return response

        lista = []
        if request.user.is_superuser:
            atividades = AtividadeDiaria.objects.all()
        else:
            atividades = AtividadeDiaria.objects.filter(registro_diario__usuario=request.user).all()
        horas_totais = timedelta(hours=0, minutes=0)
        for atividade in atividades:
            dado = None
            if len(lista) > 0:
                dado = [{'index': lista.index(item), 'item': item} for item in lista if item["atividade"] == atividade.atividade]
            if dado:
                if not isinstance(atividade.registro_diario.horas_totais, str) and not isinstance(dado[0]['item']['horas_trabalhadas'], str):
                    data = {
                        'atividade': atividade.atividade.nome,
                        'horas_trabalhadas': dado[0]['item']['horas_trabalhadas'] + atividade.registro_diario.horas_totais
                    }
                    lista.append(data)
                    lista.pop(dado[0]['index'])
            else:
                data = {
                    'atividade': atividade.atividade.nome,
                    'horas_trabalhadas': atividade.registro_diario.horas_totais
                }
                lista.append(data)
            if not isinstance(atividade.registro_diario.horas_totais, str):
                horas_totais += atividade.registro_diario.horas_totais

        response.context_data['summary'] = lista

        response.context_data['summary_total'] = {
            'total': horas_totais
        }

        # horas_previstas = len(horarios) * timedelta(hours=8, minutes=0)

        # response.context_data['saldo'] = {'saldo': str(horas_totais - horas_previstas)}

        return response


