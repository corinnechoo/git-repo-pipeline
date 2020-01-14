import json

import modules.contribution as contribution
import modules.heatmap as heat_map
import modules.rank as rank

from django.db import models
from django.http import HttpResponse
from rest_framework.decorators import api_view

from .formatter import format_end_date, raw_query
from .pipeline import DataPipeline
from .serializers import InputSerializer, PipelineInputSerializer


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
        validation = PipelineInputSerializer(data=request_body)

        if not validation.is_valid():
            return HttpResponse(json.dumps(validation.errors), status=400)

        pipeline = DataPipeline()
        pipeline.extract(request_body['owner'], request_body['repository'])

        return HttpResponse(status=200)
    return HttpResponse(status=400)


@api_view(['POST'])
def top_authors(request):
    """  
    Reads in stated parameters and returns top 3 authors
    Assumes top authors are authors that have the most commits in a given time frame.

    Returns
    -------
    list
        list of dictionaries with a maximum of 3 authors with the userid, username,
        name, email and commits

    """
    if request.method == 'POST':
        request_body = request.data
        validation = InputSerializer(data=request_body)

        if not validation.is_valid():
            return HttpResponse(json.dumps(validation.errors), status=400)

        request_body = format_end_date(request_body)
        author_ids = rank.query(request_body['start_date'], request_body['end_date'], 3)

        output = rank.format_output(author_ids)

        return HttpResponse(json.dumps(output))
    return HttpResponse(status=400)


@api_view(['POST'])
def most_contribution(request):
    """  
    Reads in stated parameters and returns 1 author with the longest contribution window

    Returns
    -------
    dict
        dictionary containing userid, username, name, email and contribution_window_days

    """
    if request.method == 'POST':
        request_body = request.data
        validation = InputSerializer(data=request_body)

        if not validation.is_valid():
            return HttpResponse(json.dumps(validation.errors), status=400)

        request_body = format_end_date(request_body)

        authors = contribution.raw_query(
            request_body['start_date'], request_body['end_date'])
        output = contribution.format_output(authors)

        return HttpResponse(json.dumps(output))
    return HttpResponse(status=400)


@api_view(['POST'])
def heatmap(request):
    """  
    Reads in stated parameters and returns a heatmap

    Returns
    -------
    list
        list of tuples, where each row contains the time frame, followed by
        the number of commits for each day of the week, starting from Monday to Sunday

    """
    if request.method == 'POST':
        request_body = request.data
        validation = InputSerializer(data=request_body)

        if not validation.is_valid():
            return HttpResponse(json.dumps(validation.errors), status=400)

        request_body = format_end_date(request_body)
        output = heat_map.raw_query(
            request_body['start_date'], request_body['end_date'])

        return HttpResponse(json.dumps(output))
    return HttpResponse(status=400)
