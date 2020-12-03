from django.contrib import admin
from prediction_models.models import PredictionModel


class PredictionModelAdmin(admin.ModelAdmin):
    search_fields = ['model_hash_code']
    list_display = ('model_hash_code', 'state', 'last_updated_at')
    readonly_fields = ('model_hash_code', 'state', 'storage_path', 'last_updated_at', 'created_at')

    def has_add_permission(self, request, obj=None):
        return False


admin.site.register(PredictionModel, PredictionModelAdmin)
