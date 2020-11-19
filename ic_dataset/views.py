from django.shortcuts import render
import os
from django.conf import settings
from django.http import HttpResponse, Http404
from django.shortcuts import render
from ic_dataset.from_icjson_2_db import update_from_ic_ds_formatted_dict
from .forms import UploadFileForm


def download_intent_phrases(request):
    """View for exporting from DB to intent_phrases.json"""
    from .from_db_2_icjson import ds_path

    if os.path.exists(ds_path):
        with open(ds_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="application/json")
            response['Content-Disposition'] = 'inline; filename=' + os.path.basename(ds_path)
            return response
    raise Http404


def upload_intents_json_view(request):

    message = 'Upload your intent_phrases.json!'
    # Handle file upload
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            # got a file
            print("got a file with content...")
            # content = request.FILES['file'].read()
            import json
            data = json.load(request.FILES['file'])
            print("JSON:")
            print(data)
            # TODO validate file before uploading to DB!
            update_from_ic_ds_formatted_dict(data)
            message = 'Intents import successfully completed!'
        else:
            message = 'The form is not valid. Fix the following error:'
    else:
        form = UploadFileForm()  # An empty, unbound form
    context = {
        'form': form,
        'message': message}
    return render(request, 'intents_upload.html', context)

def train_model_view(request):
    context = {
        'message': "Model is launched for training. Visit api in 5 minutes..."}
    return render(request, 'train_model.html', context)
