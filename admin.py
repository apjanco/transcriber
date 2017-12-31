# Register your models here.
from django.contrib import admin

from .models import HandwrittenText, PendingTranscription


class HandwrittenTextAdmin(admin.ModelAdmin):
    list_display = ('title', 'year', 'page', 'archive', 'document_type', 'language', 'slug',)
    search_fields = ('slug',)
    fieldsets = (
            ('Basic Information', {
                'fields': ( ('title', 'título'), ('language', 'idioma'),
                            ('document_type', 'tipo_del_documento'),
                            'slug', 'material_type')
                }),
             ('Collection Information', {
                 'fields': ( ('archive', 'archivo'),
                             ('collection', 'colección'),
                             ('call_number', 'número_de_etiqueta'),
                             ('page', 'páginas'), 'date_digitized')
                 }),
             ('Document Information', {
                 'fields': ( ('town_modern_official', 'pueblo'),
                             'town_short', ('primary_parties',
                                            'personajes_principales'),
                             ('witnesses', 'testigos'),
                             ('scribe', 'escribano'),
                             ('date', 'fecha'), 'year', 'transcription', 'backup_transcription',
                             'interlinear_analysis')
                 }),
            ('Ticha Information', {
                'fields': ( ('has_translation', 'is_translation'),
                            ('acknowledgements', 'agradecimientos'),
                            'permission_file', 'percent_needs_review',
                            'requester_project', 'omeka_id')
                }) )


admin.site.register(HandwrittenText, HandwrittenTextAdmin)
admin.site.register(PendingTranscription)
