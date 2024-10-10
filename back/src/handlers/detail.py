import json
from repository.PullRequestRepository import PullRequestRepository
from datetime import datetime
from config import default_headers

# Serializer to onvert datetime objects to ISO format strings before returning as API response
def default_json_serializer(obj):
    if isinstance(obj, datetime):
        return obj.isoformat()
    raise TypeError(f"Type {type(obj)} not serializable")

def GET_list_handler(event):
    response = {}
    try:
        limit = event["queryStringParameters"]['limit']
        offset = event["queryStringParameters"]['offset']
        if not limit: 
            raise Exception("limit is a mandatory query string param")
        if not offset: 
            raise Exception("offset is a mandatory query string param")
        
        pr_repository = PullRequestRepository()
        db_response = pr_repository.list_pr_events(int(limit), int(offset))
        
        response = {
            'statusCode': 200, 
            'body': json.dumps(db_response, default=default_json_serializer),
            'headers': default_headers
        }
    except Exception as e:
        print("GET LIST EXCEPTION: ", e)
        response = {
            'statusCode': 500, 
            'body': json.dumps({'error': 'Failed to list items'}), 
            'headers': default_headers
        }
    finally:
        return response
