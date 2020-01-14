import json

from django.http import HttpResponse, JsonResponse
from rest_framework.decorators import api_view
from django.core.management import call_command 


from .models import Repository
from .serializers import InputSerializer
from datetime import datetime
from .pipeline import DataPipeline

@api_view(['POST'])
def store(request):
    """  
    Reads in stated parameters and performs etl


    Returns
    -------
    str
        message containing status of request

    """
    if request.method == 'POST':
        request_body = request.data
        validation = InputSerializer(data=request_body)

        if not validation.is_valid():
            return HttpResponse(json.dumps(validation.errors), status=400)
        
        end_date = request_body.get('end_date')
        if not end_date:
            request_body['end_date'] = datetime.today().strftime("%Y-%m-%d")

        pipeline = DataPipeline()
        pipeline.extract(request_body['owner'], request_body['repository'])

        return HttpResponse(status=200)
    return HttpResponse(status=400)


