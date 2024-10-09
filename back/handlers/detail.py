import json
from classes import Response
from repository import PullRequestRepository

def GET_list_handler(limit, offset):
    response = None
    try:
        pr_repository = PullRequestRepository()
        db_response = pr_repository.list_pr_events(limit, offset)
        response = Response(200, json.dumps(db_response))
    except:
        response = Response(500, json.dumps({'error': 'Failed to list items'}))
    finally:
        return response