from datetime import datetime

from django.db import connection


def format_end_date(request_body):
    """  
    Formats the end_date for the request_body. If not present, 
    add the current date as the end_date, else return request_body


    Returns
    -------
    json
        request_body containing an end_date
    """
    end_date = request_body.get('end_date')
    if not end_date:
        request_body['end_date'] = datetime.today().strftime("%Y-%m-%d")
    return request_body


def raw_query(sql, start_date, end_date):
    """  
    Queries the database with a raw SQL query


    Returns
    -------
    list
        list of results from the SQL query
    """

    with connection.cursor() as cursor:
        cursor.execute(sql, [start_date, end_date])
        results = cursor.fetchall()

    return results
