from dataclasses import dataclass

@dataclass(statusCode=200, body="", headers={'Content-Type': 'application/json'})
class Response():
    statusCode: int
    body: str
    headers: object