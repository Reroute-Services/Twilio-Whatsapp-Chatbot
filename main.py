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
    # Find your Account SID and Auth Token at twilio.com/console
    # and set the environment variables. See http://twil.io/secure
    account_sid = os.environ['TWILIO_ACCOUNT_SID']
    auth_token = os.environ['TWILIO_AUTH_TOKEN']
    client = Client(account_sid, auth_token)

    message = client.messages \
        .create(
            from_=from_number,
            body=body,
            to=to_number
        )
    
    print("Whatsapp Message Chased!:",message.sid)

@app.post("/whatsapp")
@app.get("/whatsapp")
async def whatsapp(request : Request, background_tasks: BackgroundTasks):
    request_json = await request.form()
    # from_no = request.form['From']
    # to_number = request.form['To']
    # message_body = request.form['Body']
    print("---------------------------------------------\nWhatsapp Message Recieved!\n", request_json)

    # response_msg = chatbot.conversation_handler(from_no, message_body)
    
    resp = MessagingResponse()

    # background_tasks.add_task(session_manager.expirator)

    # resp.message(response_msg)
    # resp.message("response_msg")
    
    # total_time = time.time() - start_time
    # print("Total Response Time:", total_time)

    # if total_time >= 14:
    #     print("Timeout!!!!")
    #     # LOST_MESSAGES[from_no] = {"input":message_body, "response":resp}
    #     # sendWhatsappMsg(from_no, to_number, response_msg)

    return str(resp)


# @app.route("/whatsapp", methods=['GET', 'POST'])
# def whatsapp():
#     start = time.time()

#     """Respond to incoming calls with a simple text message."""
#     # Start our TwiML response
#     print("Whatsapp Message: ", request.values)
#     from_no = request.form['From']
#     to_number = request.form['To']
#     message_body = request.form['Body']

#     # response_msg = chat_session_handler(from_no, to_number, message_body=message_body)
#     response_msg = chatbot.conversation_handler(from_no, message_body)

#     resp = MessagingResponse()

#     # Add a message
#     # resp.message("The Robots are coming! Head for the hills!")
#     resp.message(response_msg)
    
#     end = time.time()
#     total_time = end-start
#     print("Time:", total_time)
#     if total_time >= 14:
#         print("Timeout!!!!")
#         # LOST_MESSAGES[from_no] = {"input":message_body, "response":resp}
#         sendWhatsappMsg(from_no, to_number, response_msg)

#     return str(resp)


if __name__ == '__main__':
    uvicorn.run(app, port=8080, host="0.0.0.0")
    # uvicorn.run(app)