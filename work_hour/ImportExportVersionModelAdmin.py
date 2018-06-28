from django.contrib.admin import ModelAdmin
from import_export.admin import ImportMixin, ExportMixin
from reversion.admin import VersionAdmin


class ImportExportVersionModelAdmin(ImportMixin, ExportMixin, VersionAdmin):
    """
    Import, export and Version admin.
    Fixes missing link in change_list admin view :)
    """
    #: template for change_list view
    change_list_template = 'change_list_import_export_version.html'