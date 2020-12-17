from django.contrib import admin
from prediction_models.models import PredictionModel
from prediction_models.ssh_utils import upload_to_ssh_recursive


def models_export_ssh(modeladmin, request, queryset):
    for each_model in queryset:
        print(each_model.storage_path)
        upload_to_ssh_recursive(each_model.storage_path)
        print("Done.")

models_export_ssh.short_description = "Export models to remote SSH server"


class PredictionModelAdmin(admin.ModelAdmin):
    search_fields = ['model_hash_code']
    list_display = ('model_hash_code', 'state', 'last_updated_at', 'created_at')
    readonly_fields = ('model_hash_code', 'state', 'storage_path', 'last_updated_at', 'created_at')
    ordering = ('-last_updated_at', )
    actions = [models_export_ssh]

    def has_add_permission(self, request, obj=None):
        return False


admin.site.register(PredictionModel, PredictionModelAdmin)
