import os
import json
import tempfile
from django.conf import settings
from django.http import HttpResponse, Http404
from django.shortcuts import render
from ic_dataset.from_icjson_2_db import update_from_ic_ds_formatted_dict
from .forms import UploadFileForm
from ic_dataset.from_db_2_icjson import export_db_2_ic_json
from django.http import FileResponse

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def download_intent_phrases(request):
    """View for exporting from DB to intent_phrases.json"""
    fd, ds_path = tempfile.mkstemp(suffix='.json')
    # try:
    export_db_2_ic_json(ds_path)
    if os.path.exists(ds_path):
        response = FileResponse(open(ds_path, 'rb'), as_attachment=True,
                                filename="intent_phrases_export.json")
        return response
    raise Http404
    # finally:
    #     os.remove(ds_path)
    #     raise Http404


def upload_intents_json_view(request):
    """
    Handles uploading of intent_phrase.json file and exporting intents to DB
    """

    message = 'Upload your intent_phrases.json!'
    # Handle file upload
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            # got a file
            print("got a file with content...")

            data = json.load(request.FILES['file'])
            print("JSON:")
            print(data)
            # TODO validate file before uploading to DB!
            update_from_ic_ds_formatted_dict(data)
            message = 'Intents import successfully completed!'
            # TODO redirect to intents list (render intents list with success message)
        else:
            message = 'The form is not valid. Fix the following error:'
    else:
        form = UploadFileForm()  # An empty, unbound form
    context = {
        'form': form,
        'message': message}
    return render(request, 'intents_upload.html', context)

def train_model_view(request):
    from ic_dataset.tasks import dp_retrain_task
    from ic_dataset.models import calc_dataset_hash
    hash = calc_dataset_hash()
    context = {
        'message': f"Model is launched for training. It's hash code is: {hash}. Visit api in about 25 minutes..."
    }

    dp_retrain_task.delay()
    return render(request, 'train_model.html', context)
