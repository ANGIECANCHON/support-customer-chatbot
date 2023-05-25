import functions_framework
import openai
import json
import random
import os
import firebase_admin
from firebase_admin import firestore

# Application Default credentials are automatically created.
app = firebase_admin.initialize_app()
db = firestore.client()

openai.api_key = os.environ.get('GTP4-KEY')
f = open('data.json')
bots = json.load(f)
f.close()

def getResponseTicket(message): 
    botInfo = any
    botID = getBotID(message)
    for bot in bots["bots"]:
        if bot["bot_id"] not in botID:

            return {
                "message": "bot not found"
            }
        else:
            botInfo = bot
            
            ubication = getUbication(botInfo)
            type = determineType(message)
            randomTicket = 'TK{}'.format(random.randint(100,300))
            
            ticket = {
                "ticket_id": randomTicket,
                "problem_location": ubication,
                "problem_type": type,
                "summary": message,
                "bot_id": botInfo["bot_id"],
                "status": "open"
            }

            db.collection(u'customer_bot').document(u'tickets').set(ticket)
        
            return {
                "message": "ticket creado correctamente",
                "ticket_id": ticket["ticket_id"]
                }
  
def getBotID(message):
    prompt = "Text: '{}'\nQuestion: '¿What is the bot ID?'\nAnswer:".format(message)

    return getChoiceTextIA(prompt)
    
def getUbication(data):
    latitude = data["location"]["lat"]
    longitude = data["location"]["lon"]
    
    prompt = "Text: 'La actual ubication is latitude {} y longitude {}. ¿What is the ubication name?'".format(latitude, longitude)
    
    response = getChoiceTextIA(prompt)

    return response[29:].strip()

def determineType(message):
    prompt = "Text of message: '{}'\nProblem Type (field,software,hardware):".format(message)

    return getChoiceTextIA(prompt)

def getChoiceTextIA(prompt):
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=50,
        temperature=0
    )

    return response.choices[0].text.strip()

@functions_framework.http
def customer_bot_service(request):
   
    request_json = request.get_json(silent=True)
    request_args = request.args

    if request_json and 'message' in request_json:
        message = request_json['message']
    elif request_args and 'message' in request_args:
        message = request_args['message']
    else:
        message = 'text random'
    
    return getResponseTicket(message)
    
