import os
import json
from repository.PullRequestRepository import PullRequestRepository
from config import default_headers

def POST_handler(event):
    body = None
    
    body = json.loads(event['body'])
    print("body: ", body)
    
    webhook_event_repository = PullRequestRepository()
    
    print("got repository")
    
    db_response = webhook_event_repository.store_pr_event(body)
    
    print("got db response")
    
    response = {'statusCode': 200, 'body': json.dumps(db_response), 'headers': default_headers}
    return response