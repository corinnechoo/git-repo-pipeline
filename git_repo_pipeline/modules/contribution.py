from django.db import connection
from datetime import datetime


def format_output(result):
    """  
    Formats the output for the contribution endpoint. If not present, 
    return empty dict


    Returns
    -------
    dict
        dict containing the user with the most contribution
    """
    output = {}

    if result:
        author = result[0]
        output = {
            'id': author[0],
            'username': author[1],
            'name': author[2],
            'email': author[3],
            'contribution_window_days': author[4]
        }
    return output


def raw_query(start_date, end_date):
    """  
    Queries the database with a raw SQL query for the contributions endpoint


    Returns
    -------
    list
        list of tuples from the SQL query
    """
    sql = """
            WITH cte AS (
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
    with connection.cursor() as cursor:
        cursor.execute(sql, [start_date, end_date])
        results = cursor.fetchall()

    return results
