from flask import Flask, request
from twilio.rest import Client
from main import main
from multiprocessing import Process
import re
import random
# Variables
account_sid = ""
auth_token = ""
From_num = ""

client = Client(account_sid, auth_token)

app = Flask(__name__)


@app.route("/sms", methods=['GET', 'POST'])
def receive_sms():
	#get incoming message
	message_body = request.values.get('Body')
	Client_num = request.values.get("From")
	From_num = request.values.get("To")
	x = re.search("^.ello", message_body)
	print("Received message: ",message_body)
	p = Process(target=processing_msg, args=(x, Client_num, From_num, message_body))
	p.start()
	return ""

def processing_msg(x, client_num, from_num, msg_body):
	print("processing started for message from: " + client_num)
	if x:
		send_intro(client_num, from_num)
	else:
		send_waiting_msg(client_num, from_num, msg_body)
		links = main(msg_body, client_num)
		if links:
			if len(links) > 1600:
				links = split_string(links) 
			if type(links) != str:
				for x in links:
					send_response(x, client_num, from_num)
			else:
				send_response(links, client_num, from_num)
		else:
			send_error(client_num, from_num)
		
def split_string(string):
    if len(string) <= 1300:
        return [string]

    segments = []
    segment = ""
    for word in string.split():
        if len(segment + word) > 1300:
            segments.append(segment)
            segment = ""
        if re.match("https://.*", word):
            segments.append(segment + word)
            segment = ""
        else:
            segment += word + " "
    segments.append(segment)

    return segments
	
def send_response(msg_body, client_number, sender):
	print(msg_body, type(msg_body))
	message = client.messages.create(to=client_number, from_=sender, body=msg_body)
	print("Message sent to: " + client_number + " with the body: " + msg_body)

def send_intro(num, sender):
    body = "Welcome to Orea.ai! We're glad you're here.\n\nOur goal is to save you time and help you find the best products for your needs.\n\nYou can ask us questions like, \n\n 'What should I buy my dad for his fifties birthday?' \n\n or 'What's the best shampoo without chemicals?'\n\nWe can even help you find specific items, like 'Give me 3 baby monitors that connect to my phone with wifi for under 150$'\nReady to put us to the test?\n\n Simply send us a message now and see how we can help you find the perfect product.\n\nWhether you're looking for a gift for your dad's birthday or want to find the best shampoo without harmful chemicals, we're here to help.\n\n To try it out, write us a message!"
    message = client.messages.create(to=num, from_=sender, body=body)
    print("Intro message sent to: " + num + "\n with the body: " + body)

def send_waiting_msg(num, sender, prompt):
	body = ["No problem! I'll do my best to answer your question about" + prompt + " in just a few moments. It might take me 15-30 seconds to come up with the best answer.",
	 "You got it! I'll make sure to answer your question about " + prompt + " within the next 15-30 seconds. My goal is to provide you with a helpful response.",
	  "Absolutely! Just to let you know, I'll be providing an answer to your question about " + prompt + " within the next 15-30 seconds. I'll do my best to give you a complete and accurate response."]
	message = client.messages.create(to=num, from_=sender, body=body[random.randint(0,2)])
	print("Sent waiting message to client: " + num)

def send_error(num, sender):
	body = "Sadly theres was an error in the prompt you supplied, keep in mind that the limit is 20 product recommendations at a time. \n We are always expanding the services we provide, however, at this monment only product recommendations are possible. \n Thanks for understanding, and please try and send another prompt!"
	message = client.messages.create(to=num, from_=sender,body=body)
	print("Error message sent to: " + num)

if __name__ == "__main__":
	app.run(host='0.0.0.0', port=5000)