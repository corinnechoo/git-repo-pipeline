import json

from django.http import HttpResponse, JsonResponse
from rest_framework.decorators import api_view

from .serializers import InputSerializer
from datetime import datetime


@api_view(['POST'])
def index(request):
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

        return HttpResponse(status=200)
    return HttpResponse(status=400)
