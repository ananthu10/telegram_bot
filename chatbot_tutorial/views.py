from django.views import generic
from django.views.decorators.csrf import csrf_exempt
import json
import requests
import random
from django.utils.decorators import method_decorator
from django.http.response import HttpResponse
from django.shortcuts import render
from decouple import config

from userlogger.models import UserLogger


from django.views.decorators.csrf import csrf_exempt


def get_message_from_request(request):

    received_message = {}
    decoded_request = json.loads(request.body.decode('utf-8'))
    print(decoded_request)
    userNew=0
    if 'callback_query' in decoded_request:
        received_message = decoded_request['callback_query'] 
        received_message['chat_id'] = received_message['from']['id']# simply for easier reference
        userNew=2
    if 'message' in decoded_request:
        print("new user 123")
        print(received_message)
        received_message = decoded_request['message'] 
        received_message['chat_id'] = received_message['from']['id'] # simply for easier reference
        print("new user inside lefi"+str( received_message['from']['id']))
        userNew=1
    if 'my_chat_member' in decoded_request:
        print("user in session")
        print(received_message)
        received_message = decoded_request['my_chat_member'] 
        received_message['chat_id'] = received_message['chat']['id'] # simply for easier reference
        print("new user inside lefi"+str( received_message['chat']['id']))
        userNew=0    


    return [received_message,userNew]

def send_messagesNewuser(message, token):
    # Ideally process message in some way. For now, let's just respond
    post_message_url = "https://api.telegram.org/bot{0}/sendMessage".format(token)
    print(message)
    result_message = {}         # the response needs to contain just a chat_id and text field for  telegram to accept it
    result_message['chat_id'] = message['chat_id']
    if '/start' in message['text']:
        result_message= {"chat_id":message['chat_id'],"text":"choose", "reply_markup": {"inline_keyboard": [[{"text":"fat", "callback_data": "fat"},{"text":"stupid", "callback_data": "stupid"},{"text":"dumb", "callback_data": "dumb"}]]} }
    id=message['chat_id']
    data = {"chat_id":id,"text":" coose", "reply_markup": {"inline_keyboard": [[{"text":"fat", "callback_data": "fat"},{"text":"stupid", "callback_data": "stupid"},{"text":"dumb", "callback_data": "dumb"}]]} }
    #data = {"chat_id":"752033724", "text":"Testing", "reply_markup": {"inline_keyboard": [[{"text":"fat"},{"text":"stupid", "url": "http://unofficed.com"},{"text":"dumb", "url": "http://unofficed.com"}]]} }
    response_msg = json.dumps(result_message)
    #response_msg = json.dumps(result_message)
    status = requests.post(post_message_url, headers={
        "Content-Type": "application/json"}, data=response_msg)
def welcome_messages(message,token):
    pass
def send_messages(message, token):
    # Ideally process message in some way. For now, let's just respond
    jokes = {
         'stupid': ["""Yo' Mama is so stupid, she needs a recipe to make ice cubes.""",
                    """Yo' Mama is so stupid, she thinks DNA is the National Dyslexics Association."""],
         'fat':    ["""Yo' Mama is so fat, when she goes to a restaurant, instead of a menu, she gets an estimate.""",
                    """ Yo' Mama is so fat, when the cops see her on a street corner, they yell, "Hey you guys, break it up!" """],
         'dumb':   ["""THis is fun""",
                    """THis isn't fun"""] 
    }

    post_message_url = "https://api.telegram.org/bot{0}/sendMessage".format(token)

    print(message)
    result_message = {}         # the response needs to contain just a chat_id and text field for  telegram to accept it
    result_message['chat_id'] = message['chat_id']
    userData={}
    userData['username']=message['from']['username']
    userData['chat_id']=message['chat_id']
    userData['data']=message['data']
    print( userData['data'])

    #user=UserLogger.objects.get(userName=userData['data'])
    print(userData['username'])
    print(UserLogger.objects.filter(userName=userData['username']).exists())
    if UserLogger.objects.filter(userName=userData['username']).exists():
        user=UserLogger.objects.get(userName=userData['username'])

    
    else:

        UserLogger.objects.create(userId=userData['chat_id'],userName=userData['username'])
        user=UserLogger.objects.get(userName=userData['username'])

        print(userData['data'])
    print(userData['data'])
    if  'fat' in userData['data']:
        user.fat=user.fat+1
        user.save()
        result_message['text'] = random.choice(jokes['fat'])
    elif  'stupid' in message['data']:
        result_message['text'] = random.choice(jokes['stupid'])
        user.stupid=user.stupid+1
        user.save()
    elif 'dumb' in message['data']:
        result_message['text'] = random.choice(jokes['dumb'])
        user.dumb=user.dumb+1
        user.save()
    else:
        result_message['text'] = "I don't know any responses for that. If you're interested in yo mama jokes tell me fat, stupid or dumb."
    id=message['chat_id']
    #UserLogger.objects.create(userId=message['chat_id'],userName=message['chat_id'],fat=1,stupid=1,dumb=1)
    data = {"chat_id":id,"text":result_message['text'], "reply_markup": {"inline_keyboard": [[{"text":"fat", "callback_data": "fat"},{"text":"stupid", "callback_data": "stupid"},{"text":"dumb", "callback_data": "dumb"}]]} }
    #data = {"chat_id":"752033724", "text":"Testing", "reply_markup": {"inline_keyboard": [[{"text":"fat"},{"text":"stupid", "url": "http://unofficed.com"},{"text":"dumb", "url": "http://unofficed.com"}]]} }
    response_msg = json.dumps(data)
    #response_msg = json.dumps(result_message)
    status = requests.post(post_message_url, headers={
        "Content-Type": "application/json"}, data=response_msg)


class TelegramBotView(generic.View):

    # csrf_exempt is necessary because the request comes from the Telegram server.
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return generic.View.dispatch(self, request, *args, **kwargs)

    # Post function to handle messages in whatever format they come
    def post(self, request, *args, **kwargs):
        TELEGRAM_TOKEN = config('TELEGRAM_TOKEN')
        message= get_message_from_request(request)
        print("inside post")
        print(message)
        if message[1]==1:
            print("new user on post")
            print(message[0])
            send_messagesNewuser(message[0], TELEGRAM_TOKEN)
        if message[1]==2:  
            print("existing user")
            print(message[0])
            send_messages(message[0], TELEGRAM_TOKEN)
        if message[1]==0: 
            welcome_messages(message[0], TELEGRAM_TOKEN)
        return HttpResponse()

 














def index(request):
    Users = UserLogger.objects.all()
    # for
    # list_reco_face.append(Recognize.objects.get(face_id=pk))

    return render(request, 'chatbot_tutorial/index.html', {'Users': Users})





def chat(request):
    context = {}
    return render(request, 'chatbot_tutorial/chatbot.html', context)


def respond_to_websockets(message):
    jokes = {
     'stupid': ["""Yo' Mama is so stupid, she needs a recipe to make ice cubes.""",
                """Yo' Mama is so stupid, she thinks DNA is the National Dyslexics Association."""],
     'fat':    ["""Yo' Mama is so fat, when she goes to a restaurant, instead of a menu, she gets an estimate.""",
                """ Yo' Mama is so fat, when the cops see her on a street corner, they yell, "Hey you guys, break it up!" """],
     'dumb':   ["""Yo' Mama is so dumb, when God was giving out brains, she thought they were milkshakes and asked for extra thick.""",
                """Yo' Mama is so dumb, she locked her keys inside her motorcycle."""] 
     }  

    result_message = {
        'type': 'text'
    }
    if 'fat' in message['text']:
        result_message['text'] = random.choice(jokes['fat'])
    
    elif 'stupid' in message['text']:
        result_message['text'] = random.choice(jokes['stupid'])
    
    elif 'dumb' in message['text']:
        result_message['text'] = random.choice(jokes['dumb'])

    elif message['text'] in ['hi', 'hey', 'hello']:
        result_message['text'] = "Hello to you too! If you're interested in yo mama jokes, just tell me fat, stupid or dumb and i'll tell you an appropriate joke."
    else:
        result_message['text'] = "I don't know any responses for that. If you're interested in yo mama jokes tell me fat, stupid or dumb."

    return result_message
    