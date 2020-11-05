from django.contrib import admin

# Register your models here.
from ic_dataset.models import Intent, PhraseExpression, RegularExpression, PunctuationElement
from django import forms


class PhrasesForm( forms.ModelForm ):
    text = forms.CharField(widget=forms.Textarea(attrs={
        # 'size': 2000,
        'cols': 120, 'rows': 4}))

    fields = ['text']
    class Meta:
        model = PhraseExpression
        fields = ['text']


class PhrasesInline(admin.TabularInline):
    model = PhraseExpression
    form = PhrasesForm
    extra=0


class RegExpsInline(admin.TabularInline):
    model = RegularExpression
    extra=0


class PunctuationInline(admin.TabularInline):
    model = PunctuationElement
    extra=0



class IntentAdmin(admin.ModelAdmin):
    # search_fields = ['input_data']
    # list_display = ('input_data', 'golden_label')
    inlines = [
        PhrasesInline,
        RegExpsInline,
        PunctuationInline
    ]


admin.site.register(Intent, IntentAdmin)
