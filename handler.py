import json
import pickle

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

def do_main():
    event = {
        'message': {
            'text': "What is the latest version of Flutter?"
        }
    }

    response = ask_question(event, None)
    body = json.loads(response['body'])
    with open('event.json', 'w') as event_file:
        event_file.write(json.dumps(event))
        
#do_main()