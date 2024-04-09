import openai
import requests
import pymysql
import logging

OPENAI_API_KEY = ""
AMZAPI_API_KEY = ""

# Connect to database
conn = pymysql.connect(
    host="*", 
    user="*", 
    password="*", 
    database="*")
#create a cursor object
cursor = conn.cursor()

# Functions
def remove_duplicate_newlines(string):
    return '\n'.join([line for line in string.splitlines() if line.strip()])

def remove_first_3_chars(strings):
    return [string[3:] for string in strings]

# Openai
def run_openai(body):
    prompt = body + ", give me only the product name"
    temp = 0
    openai_api_key = OPENAI_API_KEY
    model = "text-davinci-003"
    max_tokens = 500 

    # Script
    openai.api_key = openai_api_key

    response = openai.Completion.create(
    model=model,
    prompt=prompt,
    temperature=temp,
    max_tokens=max_tokens
    )
    #print(response)
    text = response["choices"][0]["text"]

    text = remove_duplicate_newlines(text)
    text = text.split("\n")
    print(text)

    if len(text) > 1:
        text = remove_first_3_chars(text)
    return text

# amazon affiliate links
def get_affiliate(text):
    final_link = []
    final_a_link = []
    affiliate_tag = "shoppingai0e-20"
    headers = {"apikey": AMZAPI_API_KEY}

    for product in text: 
        # set up the request parameters
        params = (("query",product),);
        # make the http GET request to Rainforest API
        response = requests.get('https://api.amzapi.com/v1/search', headers=headers, params=params);
        result = response.json()
        #print(result)
        try:
            link = result["search_results"][0]["link"]
            print(product, link)
        except:
            print(result)
            break
        affiliate_link = amazon_affiliate_link(link, affiliate_tag)
        #print(affiliate_link)
        final_link.append(link)
        final_a_link.append(affiliate_link)
        print("Got link(s)")
    return final_a_link

        # make the link into an affiliate link
def amazon_affiliate_link(product_link, affiliate_tag):
    if "amazon.com" not in product_link:
        return None
    if "?" in product_link:
        affiliate_link = product_link + "&tag=" + affiliate_tag
    else:
        affiliate_link = product_link + "?tag=" + affiliate_tag
    return affiliate_link

def round_two(client_prompt, link):
    #print(link)
    prompt = "Provide a short personalized product recommendations for "+ client_prompt + " by describing each product with a brief summary and including these links in your response: " + link
    temp = 0.7
    openai_api_key = OPENAI_API_KEY
    model = "text-davinci-003"
    max_tokens = 1000
    #print(prompt)
    # Script
    openai.api_key = openai_api_key

    response = openai.Completion.create(
    model=model,
    prompt=prompt,
    temperature=temp,
    max_tokens=max_tokens,
    n=1
    )
    text = response["choices"][0]["text"]
    #print(response)
    final_response = "Your prompt: " + client_prompt + "\n Our recommendation: " + text
    return final_response

def add_message(client_number, message, product, response):
    # Insert a new record into the table
    cursor.execute("INSERT INTO data (client_number, message, product, response) VALUES (%s, %s, %s, %s)", (client_number, message, product, response))
    conn.commit()
    print("Recored message in data base")
    return ""

def main(prompt, client_num):
    response = run_openai(prompt)
    logging.info("Response Done!")
    print("Response Done!")
    links = get_affiliate(response)
    print("Links Done!")
    final_string = '\n'.join(links)
    print("Final string made!")
    result = round_two(prompt, final_string)
    print("Round two done!")
    #print(result)
    add_message(client_num, prompt, ','.join(response), result)
    print("Added data into database done!")
    return result