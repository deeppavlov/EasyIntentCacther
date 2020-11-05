from rest_framework import status
from django.http import HttpResponse, JsonResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
# from snippets.models import Snippet
# from snippets.serializers import SnippetSerializer
from dp_intent_catcher.src.build_model import get_prepared_model
from predictions_log.models import PredictionCase


@api_view(['GET', 'POST'])
@csrf_exempt
def ic_predict(request):
    """
    Prediction API interface

    """
    if request.method == 'GET':
        # snippets = Snippet.objects.all()
        # serializer = SnippetSerializer(snippets, many=True)
        # return Response({"kek": "lol"}, safe=False)
        return Response({"text": "what is the weather in Boston?"})

    elif request.method == 'POST':
        # TODO add input logging!
        # print(request)
        # print(request.__dict__)
        # # print(request.body)
        # print("request data VVVV")
        # print(type(request.data))
        # print(request.data)
        # print(request.data.__dict__)
        if 'text' in request.data:
            input_text = request.data['text']
        else:
            return Response("text attribute must be provided", status=status.HTTP_400_BAD_REQUEST)

        print("input_text VVVV")
        print(input_text)
        ic_model = get_prepared_model()
        # Hello Kennedy said Mister Harrison in Washington DC at  3pm Yesterday
        model_output = ic_model([[input_text]])
        print("model_out")
        print(model_output)
        # toks = model_output[0][0]
        # iobs = model_output[1][0]
        output_dict = {"input_text": input_text,
                         # "tokens": toks,
        #                  "bois": iobs,
        #                  "entities": "TODO",
                         "output": model_output}

        predictions = model_output[0]
        # find classes with detected: 1
        detections = []
        for intent_name, pred_data in predictions.items():
            if pred_data['detected']==1:
                detections.append(intent_name)
        result = "|".join(detections)
        case, created = PredictionCase.objects.get_or_create(input_data=input_text, prediction_data=result,
                                                             other_kwargs=model_output[0])
        if not created:
            case.count+=1
            case.save()
        return Response(output_dict)