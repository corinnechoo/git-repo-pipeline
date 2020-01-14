from datetime import datetime

from django.db import connection


def format_end_date(request_body):
    end_date = request_body.get('end_date')
    if not end_date:
        request_body['end_date'] = datetime.today().strftime("%Y-%m-%d")
    return request_body


def raw_query(sql, start_date, end_date):
    with connection.cursor() as cursor:
        cursor.execute(sql, [start_date, end_date])
        results = cursor.fetchall()

    return results
