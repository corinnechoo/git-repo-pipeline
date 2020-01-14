from .models import Commit, User
from django.db.models import Count


def format_output(result):
    """  
    Formats and sorts the output for the top authors endpoint. 
    If not present, return empty list


    Returns
    -------
    list
        list containing the top 3 users with the most commits
    """
    store = {}
    for author in result:
        store[author['authorId']] = author['total']

    authors = User.objects.filter(userId__in=list(store.keys()))
    output = [{'id': a.userId,
                'username': a.username,
                'name': a.name,
                'email': a.email,
                'commits': store.get(a.userId)
                } for a in authors]

    sorted_output = sorted(output, key=lambda x: x['commits'], reverse=True)
    return sorted_output


def query(start_date, end_date, top_num):
    """  
    Queries the database using orm to obtain the top n authors


    Returns
    -------
    list
        list of tuples from the SQL query
    """
    author_ids = Commit.objects.filter(commitDate__range=[start_date, end_date]).values(
            'authorId').annotate(total=Count('authorId')).order_by('-total')[:top_num]
    return author_ids