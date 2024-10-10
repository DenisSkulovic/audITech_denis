import os
import json
from classes import Response
from repository import PullRequestRepository

def POST_handler(event):
    body = None
    response = None
    
    try:
        body = json.loads(event['body'])
        
        table_name=os.getenv('POSTGRESQL_WEBHOOK_DETAIL_TABLE')
        webhook_event_repository = PullRequestRepository(table_name)
        
        db_response = webhook_event_repository.store_pr_event(body)
        
        response = Response(200, json.dumps(db_response))
    except json.JSONDecodeError:
        response = Response(400, json.dumps({'error': 'Invalid JSON'}))
    finally:
        return response