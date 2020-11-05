from django.http import HttpResponseRedirect
from django.shortcuts import render
from .forms import UploadFileForm
import os
from django.conf import settings
from django.http import HttpResponse, Http404
# Imaginary function to handle an uploaded file.
# from somewhere import handle_uploaded_file




def download_intent_phrases(request):
    """View for exporting from DB to intent_phrases.json"""
    from .from_db_2_icjson import ds_path

    if os.path.exists(ds_path):
        with open(ds_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="application/json")
            response['Content-Disposition'] = 'inline; filename=' + os.path.basename(ds_path)
            return response
    raise Http404

from django.shortcuts import redirect, render
# from .models import Document
from .forms import UploadFileForm
from ic_dataset.from_icjson_2_db import update_from_ic_ds_formatted_dict


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
            # print(content)
            # newdoc = Document(docfile=request.FILES['docfile'])
            # newdoc.save()
            update_from_ic_ds_formatted_dict(data)

            # Redirect to the document list after POST
            return redirect('upload_intents_json_view')
        else:
            message = 'The form is not valid. Fix the following error:'
    else:
        form = UploadFileForm()  # An empty, unbound form

    # Load documents for the list page
    # documents = Document.objects.all()

    # Render list page with the documents and the form
    context = {
        # 'documents': documents,
        'form': form,
        'message': message}
    return render(request, 'intents_upload.html', context)

def train_model_view(request):
    context = {
        'message': "Model is launched for training. Visit api in 5 minutes..."}
    return render(request, 'train_model.html', context)

# def handle_uploaded_file(f):
#     # TODO validat
#     #  e file
#     # try to call import
#     with open('some/file/name.txt', 'wb+') as destination:
#         for chunk in f.chunks():
#             destination.write(chunk)
#
# def upload_file(request):
#     if request.method == 'POST':
#         form = UploadFileForm(request.POST, request.FILES)
#         if form.is_valid():
#             handle_uploaded_file(request.FILES['file'])
#             return HttpResponseRedirect('/success/url/')
#     else:
#         form = UploadFileForm()
#     return render(request, 'upload.html', {'form': form})

# from django.shortcuts import render
#
# from rest_framework import status
# from rest_framework.decorators import api_view
# from rest_framework.response import Response
# #
# #
# # from django.http import HttpResponse, JsonResponse
# # from django.views.decorators.csrf import csrf_exempt
# # from rest_framework.parsers import JSONParser
# from ner_dataset.models import TrainingSample
# from ner_dataset.serializers import TrainingSampleSerializer
#
#
# @api_view(['GET', 'POST'])
# def training_samples_list(request, format=None):
#     """
#     List all training samples, or create a new training sample.
#     """
#     if request.method == 'GET':
#         training_samples = TrainingSample.objects.all()
#         serializer = TrainingSampleSerializer(training_samples, many=True)
#         return Response(serializer.data)
#
#     elif request.method == 'POST':
#         serializer = TrainingSampleSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#
# @api_view(['GET', 'PUT', 'DELETE'])
# def training_sample_detail(request, pk, format=None):
#     """
#     Retrieve, update or delete a TrainingSample
#     """
#     try:
#         training_sample = TrainingSample.objects.get(pk=pk)
#     except TrainingSample.DoesNotExist:
#         return Response(status=status.HTTP_404_NOT_FOUND)
#
#     if request.method == 'GET':
#         serializer = TrainingSampleSerializer(training_sample)
#         return Response(serializer.data)
#
#     elif request.method == 'PUT':
#         serializer = TrainingSampleSerializer(training_sample, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#     elif request.method == 'DELETE':
#         training_sample.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)
#
# #
# # @csrf_exempt
# # def training_samples_list(request):
# #     """
# #     List all training samples, or create a new training sample.
# #     """
# #     if request.method == 'GET':
# #         training_samples = TrainingSample.objects.all()
# #         serializer = TrainingSampleSerializer(training_samples, many=True)
# #         return JsonResponse(serializer.data, safe=False)
# #
# #     elif request.method == 'POST':
# #         data = JSONParser().parse(request)
# #         serializer = TrainingSampleSerializer(data=data)
# #         if serializer.is_valid():
# #             serializer.save()
# #             return JsonResponse(serializer.data, status=201)
# #         return JsonResponse(serializer.errors, status=400)
# #
# # @csrf_exempt
# # def training_sample_detail(request, pk):
# #     """
# #     Retrieve, update or delete a TrainingSample
# #     """
# #     try:
# #         training_sample = TrainingSample.objects.get(pk=pk)
# #     except TrainingSample.DoesNotExist:
# #         return HttpResponse(status=404)
# #
# #     if request.method == 'GET':
# #         serializer = TrainingSampleSerializer(training_sample)
# #         return JsonResponse(serializer.data)
# #
# #     elif request.method == 'PUT':
# #         data = JSONParser().parse(request)
# #         serializer = TrainingSampleSerializer(training_sample, data=data)
# #         if serializer.is_valid():
# #             serializer.save()
# #             return JsonResponse(serializer.data)
# #         return JsonResponse(serializer.errors, status=400)
# #
# #     elif request.method == 'DELETE':
# #         training_sample.delete()
# #         return HttpResponse(status=204)