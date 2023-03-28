import json
import pickle
import base64
import urllib.parse

# REF: https://www.kaggle.com/prmohanty/python-how-to-save-and-load-ml-models
model_name = 'faiss_store.pkl'
with open(model_name, 'rb') as file:  
    model = pickle.load(file)

def ask_question(event, context):

    body = {
        "message": "OK",
    }

    print("event.get('source')", event.get("source"))

    if event.get("source") == "serverless-plugin-warmup":
        body['message'] = 'WarmUP - Keep the Lambda warm!'

    else: 
        print(json.dumps(event))

    print(body['message'])

    response = {
        "statusCode": 200,
        "body": json.dumps(body),
        "headers": {
            "Content-Type": 'application/json',
            "Access-Control-Allow-Origin": "*"
        }
    }

    return response

def webhook(event, context):
    body = event.get("body")

    if event.get("isBase64Encoded"): 
        base64_bytes = base64.b64decode(body)
        body = base64_bytes.decode("utf-8")
    
    body = urllib.parse.parse_qs(body)
    print(f"body:\n{body}")
    context = json.loads(body['contextobj'][0])
    sender = json.loads(body['senderobj'][0])
    message = json.loads(body['messageobj'][0])

    response = f"botname: {context['botname']}, channel: {context['channeltype']}, traceId: {context['traceId']}, contextid: {context['contextid']}, "
    response += f"sender: {sender['display']}, "
    response += f"message id: {message['id']}, type: {message['type']}, text: {message['text']}, timestamp: {message['timestamp']}"


    print(response)
    return {
        "statusCode": 200,
        "body": response,
        "headers": {
            "Content-Type": 'text/plain',
        }
    }   

def test_ask_question():
    event = {
        'message': {
            'text': "What is the latest version of Flutter?"
        }
    }

    response = ask_question(event, None)
    body = json.loads(response['body'])
    with open('event.json', 'w') as event_file:
        event_file.write(json.dumps(event))
        
def test_webhook():
    with open('webhook_event.json') as json_file:
        file_contents = json_file.read()
    event = json.loads(file_contents)
    response = webhook(event, None)

test_webhook()