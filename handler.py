import json
import pickle
import base64
import urllib.parse
from langchain.chains import VectorDBQAWithSourcesChain
from langchain.chat_models import ChatOpenAI
from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)

# REF: https://www.kaggle.com/prmohanty/python-how-to-save-and-load-ml-models
model_name = 'faiss_store.pkl'
with open(model_name, 'rb') as file:  
    model = pickle.load(file)

system_template="""Use the following pieces of context to answer the users question. 
If you don't know the answer, just say "Hmm..., I'm not sure.", don't try to make up an answer.
ALWAYS return a "Sources" part in your answer.
The "Sources" part should be a reference to the source of the document from which you got your answer.

Example of your response should be:

```
The answer is foo

Sources: xyz
```

Begin!
----------------
{summaries}"""
messages = [
    SystemMessagePromptTemplate.from_template(system_template),
    HumanMessagePromptTemplate.from_template("{question}")
]
prompt = ChatPromptTemplate.from_messages(messages)

def get_chain(vectorstore, prompt):
    chain_type_kwargs = {"prompt": prompt}
    chain = VectorDBQAWithSourcesChain.from_chain_type(
    ChatOpenAI(temperature=0), 
        chain_type="stuff", 
        vectorstore=vectorstore,
        chain_type_kwargs=chain_type_kwargs
    )
    return chain

def ask_question(event, context):

    message = "The chatbot seems not functioning, please report the issue at https://github.com/limcheekin/serverless-flutter-gpt/issues."

    print("event.get('source')", event.get("source"))

    if event.get("source") == "serverless-plugin-warmup":
        message = 'WarmUP - Keep the Lambda warm!'

    else: 
        print(json.dumps(event))
        body = event.get("body")
        if event.get("isBase64Encoded"): 
            base64_bytes = base64.b64decode(body)
            body = base64_bytes.decode("utf-8")
            body = urllib.parse.parse_qs(body)
        context = json.loads(body['contextobj'][0])    
        senderobj = json.loads(body["senderobj"][0])
        messageobj = json.loads(body['messageobj'][0])
        qa_chain = get_chain(model, prompt)
        question = messageobj['text']
        if question == "/start":
            message = f"Hello {senderobj['display']}, I'm {context['botname']}.\nType /help for list of commands, otherwise you can start asking me anything about Flutter."
        elif question == "/help":
            message = "I'm an AI chatbot that can answer questions about Flutter.\nType /start to start asking questions.\nType /about to find out more about me and my creator."
        elif question == "/about":
            message = f"I'm {context['botname']}, my knowledge is derived from https://docs.flutter.dev/ since March 2023 and created by @limcheekin, feel free to contact me at https://www.linkedin.com/in/limcheekin/."
        else:
            result = qa_chain({"question": question})
            message = result['answer']
            print("\n\n")
            print(result)

    print(message)

    response = {
        "statusCode": 200,
        "body": message,
        "headers": {
            "Content-Type": 'application/json'
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

def test_ask_question(event_file):
    with open(event_file) as json_file:
        file_contents = json_file.read()
    event = json.loads(file_contents)
    response = ask_question(event, None)
    print(f"response:\n{response}")

def test_webhook():
    with open('test/data/webhook_event.json') as json_file:
        file_contents = json_file.read()
    event = json.loads(file_contents)
    response = webhook(event, None)
    print(f"response:\n{response}")

if __name__ == "__main__":
    test_ask_question("test/data/event_start.json")
    test_ask_question("test/data/event_help.json")
    test_ask_question("test/data/event_about.json")
    test_ask_question("test/data/event_question.json")