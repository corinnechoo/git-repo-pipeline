import json

from django.db import models
from django.db.models import Count
from django.http import HttpResponse
from rest_framework.decorators import api_view

from .formatter import format_end_date, raw_query
from .models import Commit, User
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

        author_ids = Commit.objects.filter(commitDate__range=[request_body['start_date'], request_body['end_date']]).values(
            'authorId').annotate(total=Count('authorId')).order_by('-total')[:3]

        store = {}
        for author in author_ids:
            store[author['authorId']] = author['total']

        authors = User.objects.filter(userId__in=list(store.keys()))
        output = [{'id': a.userId,
                   'username': a.username,
                   'name': a.name,
                   'email': a.email,
                   'commits': store.get(a.userId)
                   } for a in authors]

        sorted_output = json.dumps(
            sorted(output, key=lambda x: x['commits'], reverse=True))
        return HttpResponse(sorted_output)
    return HttpResponse(status=400)


@api_view(['POST'])
def most_contribution(request):
    """  
    Reads in stated parameters and 1 author with the longest contribution window

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
        sql = """
            with cte as (
                SELECT * FROM modules_user u
                INNER JOIN (
                    SELECT * FROM modules_commit
                    WHERE commitDate 
                    BETWEEN %s  AND %s
                ) c
                ON u.userId = c.authorId
            )
            SELECT userId, username, name, email, julianday(MAX(commitDate)) - julianday(MIN(commitDate)) dateDiff FROM cte
            GROUP BY userId 
            ORDER BY dateDiff DESC
            LIMIT 1
            ;
        """
        authors = raw_query(
            sql, request_body['start_date'], request_body['end_date'])

        output = {}

        if authors:
            author = authors[0]
            output = {'id': author[0],
                      'username': author[1],
                      'name': author[2],
                      'email': author[3],
                      'contribution_window_days': author[4]
                      }

        return HttpResponse(json.dumps(output))
    return HttpResponse(status=400)


@api_view(['POST'])
def heatmap(request):
    """  
    Reads in stated parameters and 1 author with the longest contribution window

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
        sql = """
            SELECT 
            CASE hour
                WHEN 0 THEN '12am-3am' 
                WHEN 1 THEN '3am-6am'
                WHEN 2 THEN '6am-9am'
                WHEN 3 THEN '9am-12pm'
                WHEN 4 THEN '12pm-3pm'
                WHEN 5 THEN '3pm-6pm'
                WHEN 6 THEN '6pm-9pm'
                WHEN 7 THEN '9pm-12am'
            END AS hour_group,
            SUM(CASE day WHEN 1 THEN 1 else 0 end) AS "Mon",
            SUM(CASE day WHEN 2 THEN 1 else 0 end) AS "Tues",
            SUM(CASE day WHEN 3 THEN 1 else 0 end) AS "Wed",
            SUM(CASE day WHEN 4 THEN 1 else 0 end) AS "Thurs",
            SUM(CASE day WHEN 5 THEN 1 else 0 end) AS "Fri",
            SUM(CASE day WHEN 6 THEN 1 else 0 end) AS "Sat",
            SUM(CASE day WHEN 0 THEN 1 else 0 end) AS "Sun"
            FROM (
                SELECT 
                CAST (strftime('%%w', commitDate) AS INTEGER) day, 
                CAST ((strftime( '%%H', commitDate) / 3) AS INTEGER) hour, 
                *  
                FROM modules_commit 
                WHERE commitDate BETWEEN %s AND %s
            ) p
            GROUP BY hour
            ORDER BY hour
            ;
            """

        output = raw_query(
            sql, request_body['start_date'], request_body['end_date'])

        return HttpResponse(json.dumps(output))
    return HttpResponse(status=400)
