import json
from back.handlers.webhook import POST_handler
from dotenv import load_dotenv
from classes import Response

load_dotenv()

def lambda_handler(event, context):
    response = {}
    
    path_method = f'{event["rawPath"]} {event["httpmethod"]}'
    print("path_method: ", path_method)
    
    if path_method == "/webhook POST": 
        response = POST_handler(event)
    elif path_method == "/detail/search POST": 
        response = POST_handler(event)
    else:
        response = Response(404, "unidentified path and/or method")
        print("unidentified path and/or method")            
        
    print("response", json.dumps(response))
    print("exiting lambda handler")
    return response