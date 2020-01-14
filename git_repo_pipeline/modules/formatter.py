from datetime import datetime


def format_end_date(request_body):
    end_date = request_body.get('end_date')
    if not end_date:
        request_body['end_date'] = datetime.today().strftime("%Y-%m-%d")
    return request_body
