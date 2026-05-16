import os
import hmac
import hashlib
import json
import requests

url = os.getenv("HERMES_WEBHOOK_URL")
secret = os.getenv("HERMES_SECRET")

def request(payload: dict):
    payloadstr = json.dumps(payload)
    signature = hmac.new(
        key=secret.encode('utf-8'),
        msg=payloadstr.encode('utf-8'),
        digestmod=hashlib.sha256
    ).hexdigest()

    response = requests.post(url, data=payloadstr, headers={
        "Content-Type": "application/json",
        "X-Webhook-Signature": signature
    })
    return response.json()