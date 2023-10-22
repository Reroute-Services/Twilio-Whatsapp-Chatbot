from fastapi import FastAPI, Request, BackgroundTasks
import uvicorn
from twilio.twiml.voice_response import VoiceResponse
from twilio.twiml.messaging_response import MessagingResponse
from twilio.rest import Client
from chatbot import ChatBot
import time
import os

app = FastAPI()

chatbot = ChatBot()

def sendWhatsappMsg(to_number, from_number, body):
    account_sid = os.environ['TWILIO_ACCOUNT_SID']
    auth_token = os.environ['TWILIO_AUTH_TOKEN']
    client = Client(account_sid, auth_token)

    message = client.messages \
        .create(
            content_sid='HX3058904f454d7ef1bb2ff37b9f203702',
            from_=from_number,
            body=body,
            to=to_number
        )
    
    print("Whatsapp Message Chased!:",message.sid)

def get_send_chatbot_response(sender_id, reciever_id, message_body):
    response_msg = chatbot.conversation_handler(sender_id, message_body)
    sendWhatsappMsg(sender_id, reciever_id, response_msg)

@app.post("/whatsapp")
@app.get("/whatsapp")
async def whatsapp(request : Request, background_tasks: BackgroundTasks):
    request_form = await request.form()

    print("""---------------------------------------------
    Whatsapp Message Recieved!
    Message SID: {}
    Sender ID: {}
    Sender Name: {}
    Reciever ID: {}
    Message Length: {}
    Message Body: {}
---------------------------------------------""".format(
        request_form["SmsSid"],
        request_form["From"],
        request_form["ProfileName"],
        request_form["To"],
        len(request_form["Body"]),
        request_form["Body"]))

    resp = MessagingResponse()

    background_tasks.add_task(get_send_chatbot_response, request_form["From"], request_form["To"], request_form["Body"])

    return str(resp)


if __name__ == '__main__':
    uvicorn.run(app, port=8080, host="0.0.0.0")
    # uvicorn.run(app)