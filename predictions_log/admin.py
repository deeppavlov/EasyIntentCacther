from django.contrib import admin


# Register your models here.
from predictions_log.models import PredictionCase

class PredictionCaseAdmin(admin.ModelAdmin):
    search_fields = ['input_data']
    list_display = ('input_data', 'prediction_data', 'count', 'last_updated_at')
    # pass

admin.site.register(PredictionCase, PredictionCaseAdmin)
