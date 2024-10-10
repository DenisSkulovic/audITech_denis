import json
from handlers.webhook import POST_handler
from handlers.detail import GET_list_handler
from dotenv import load_dotenv
import pg8000
import os
from config import default_headers

load_dotenv()

def lambda_handler(event, context):
    response = {'statusCode': 200, 'body': "empty", 'headers': default_headers}
    try:
        print("event:", event)
    
        path_method = f'{event["path"]} {event["httpMethod"]}'
        print("path_method: ", path_method)
        
        # ROUTING
        if path_method == "/webhook POST": 
            response = POST_handler(event)
        elif path_method == "/detail/search GET": 
            response = GET_list_handler(event)
        else:
            response = {'statusCode': 404, 'body': "unidentified path and/or method", 'headers': default_headers}
            print("unidentified path and/or method")            
            
        print("response", json.dumps(response))
        print("exiting lambda handler")
    except Exception as e:
        print("EXCEPTION: ", e)
        response["statusCode"] = 500
        response["body"] = "Server FATALITY"
    finally:
        print("final response", response)
        return response