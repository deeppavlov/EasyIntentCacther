from django.contrib import admin


# Register your models here.
from predictions_log.models import PredictionCase

class PredictionCaseAdmin(admin.ModelAdmin):
    search_fields = ['input_data']
    list_display = ('input_data', 'prediction_data', 'count', 'last_updated_at')
    readonly_fields = ('input_data', 'prediction_data', 'count', 'last_updated_at', 'other_kwargs', 'created_at')

    def has_add_permission(self, request, obj=None):
        return False

admin.site.register(PredictionCase, PredictionCaseAdmin)
