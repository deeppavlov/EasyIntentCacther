from django.contrib import admin
from prediction_models.models import PredictionModel
from prediction_models.ssh_utils import upload_to_ssh_recursive
from constance import config
from django.contrib import messages


class PredictionModelAdmin(admin.ModelAdmin):
    search_fields = ['model_hash_code']
    list_display = ('model_hash_code', 'state', 'last_updated_at', 'created_at')
    readonly_fields = ('model_hash_code', 'state', 'storage_path', 'last_updated_at', 'created_at')
    ordering = ('-last_updated_at', )
    actions = ["models_export_ssh"]

    def has_add_permission(self, request, obj=None):
        return False

    def models_export_ssh(self, request, queryset):
        """Django action for exporting Prediction model to SSH Server"""
        if config.SSH_EXPORT_MODELS:
            try:
                for each_model in queryset:
                    print(each_model.storage_path)
                    upload_to_ssh_recursive(each_model.storage_path)
                    print("Done.")

            except Exception as e:
                print(e)
                self.message_user(request, f"SSH Export failed: {e}", messages.ERROR)
            else:
                self.message_user(request, "Export to SSH Server succeed!", messages.SUCCESS)
        else:
            # Request to enable ssh export in settings
            self.message_user(
                request,
                f"SSH_EXPORT_MODELS option is disabled, enable it in configs to export models to SSH Server!",
                messages.WARNING)
    models_export_ssh.short_description = "Export models to remote SSH server"


admin.site.register(PredictionModel, PredictionModelAdmin)
