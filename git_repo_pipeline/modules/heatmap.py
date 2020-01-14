from django.db import connection
from datetime import datetime


def raw_query(start_date, end_date):
    """  
    Queries the database with a raw SQL query for the heatmap endpoint


    Returns
    -------
    list
        list of tuples from the SQL query
    """
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
    with connection.cursor() as cursor:
        cursor.execute(sql, [start_date, end_date])
        results = cursor.fetchall()

    return results
