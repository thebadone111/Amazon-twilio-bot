Automatic Bot which answers prompts sent over sms or whatsapp and give product recommendations.

Description:
Flask app webhook for twilio.
When recieves a prompt, uses ChatGPT to find products
Uses Amzapi (can use rainforest with some mod) to find product links
Makes the links into affiliate links
Uses ChatGPT to write a review for the prodcuts.
Sends the affiliate link and the reivew back to the orginial prompter

Installation:
pip install -r requirments.txt

for database:
    Make a mysql database (I used mariaDB)
        Database name: main
            table name: users
            columns: username, password

            table name: data
            columns: client_number, message, product, response

    put login for mysql in Databasing/main.py
    also put right ip and port for the flask app at the bottom


For Main/main.py
    1) put the right mysql login and data (row: 7-11)
    2) Change openai api key and amzapi api key

for Main/app.py
    1) Fill in twilio variables
    2) Change flask ip and port if necessary

