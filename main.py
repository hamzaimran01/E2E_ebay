from email import message
from tokens import *
import requests
from datetime import datetime,timedelta
from MessageReceiverCleaner import receivedMessages_cleaner
import json
from huggingface_hub import InferenceClient
import os
import json

#importing items_data file
file_path_items = os.path.join(os.getcwd(), './item_info/data', 'item_data.json')

with open (file_path_items,'r') as file_data:
    data_items = json.load(file_data)

#importing buyer_data:
file_path_hamza = os.path.join(os.getcwd(), 'hamzadur_0data.json')
with open (file_path_hamza,'r') as message_data:
    msgs = message_data.readlines()

with open (file_path_items,'r') as file_data:
    data_items = json.load(file_data)



EBAY_APP_ID = APPLICATION_ID
EBAY_CERT_ID = CERTIFICATE_ID
EBAY_DEV_ID = DEVELOPER_ID
EBAY_USER_TOKEN = AUTH_TOKEN


def get_unread_msgs():
    headers = {
        "X-EBAY-API-CALL-NAME": "GetMemberMessages",
        "X-EBAY-API-COMPATIBILITY-LEVEL": "967",
        "X-EBAY-API-SITEID": "0",
        "X-EBAY-API-DEV-NAME": EBAY_DEV_ID,
        "X-EBAY-API-APP-NAME": EBAY_APP_ID,
        "X-EBAY-API-CERT-NAME": EBAY_CERT_ID,
        "Content-Type": "text/xml"
    }

    # eBay API endpoint
   
    xml_payload = f"""<?xml version="1.0" encoding="utf-8"?>
    <GetMemberMessagesRequest xmlns="urn:ebay:apis:eBLBaseComponents">
        <RequesterCredentials>
            <eBayAuthToken>{EBAY_USER_TOKEN}</eBayAuthToken>
        </RequesterCredentials>
        <DetailLevel>ReturnMessages</DetailLevel>
        <MailMessageType>All</MailMessageType>
        <MessageStatus>Unanswered</MessageStatus>
        <StartCreationTime>2025-05-08T00:00:00.000Z</StartCreationTime>
        <EndCreationTime>2025-05-09T23:59:59.999Z</EndCreationTime>
        <Pagination>
            <EntriesPerPage>100</EntriesPerPage>
            <PageNumber>1</PageNumber>
        </Pagination>
    </GetMemberMessagesRequest>"""
    
    response = requests.post(EBAY_API_URL, headers = headers, data = xml_payload)
    return response

def respond_to_message(message_id, item_id, recipient_id, llmresponse):
    #HARDCODED_RESPONSE = "Does it become unread, thatt izz the question"

    """ Sends a hardcoded response to the eBay user """
    headers = {
        "X-EBAY-API-CALL-NAME": "AddMemberMessageRTQ",
        "X-EBAY-API-COMPATIBILITY-LEVEL": "967",
        "X-EBAY-API-SITEID": "0",
        "X-EBAY-API-DEV-NAME": EBAY_DEV_ID,
        "X-EBAY-API-APP-NAME": EBAY_APP_ID,
        "X-EBAY-API-CERT-NAME": EBAY_CERT_ID,
        "Content-Type": "text/xml"
    }

    xml_payload = f"""<?xml version="1.0" encoding="utf-8"?>
<AddMemberMessageRTQRequest xmlns="urn:ebay:apis:eBLBaseComponents">
    <RequesterCredentials>
        <eBayAuthToken>{EBAY_USER_TOKEN}</eBayAuthToken>
    </RequesterCredentials>
    <ItemID>{item_id}</ItemID>
    <MemberMessage>
        <RecipientID>{recipient_id}</RecipientID>
        <Body>{llm_response}</Body>
        <ParentMessageID>{message_id}</ParentMessageID>
    </MemberMessage>
</AddMemberMessageRTQRequest>"""

    response = requests.post(EBAY_API_URL, headers=headers, data=xml_payload)
    
        
        


def llm_answers(items_data, query):
    access_token = "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"
    client = InferenceClient(
        provider = "hyperbolic",
        api_key = access_token
    )

    completion = client.chat.completions.create(
        model="meta-llama/Llama-3.3-70B-Instruct",
        messages=[
            {
            "role": "system",
            "content": f"""You are an Ebay seller. You should only reply back based on this data:'''{items_data}'''
            If there is not a match you should write about which product you are asking."""
            },
            {
            "role":"user",
            "content": f"""Here is the query regarding a product that a buyer is asking'''{query}'''"""    
            }
            
        ],
            
        max_tokens = 512,
     
    )
    llm_response = completion.choices[0].message
    print(llm_response)
    return llm_response
    




########################
#get unread msgs

unread_msgs = get_unread_msgs()
#check unread msgs if they are there and than clean it.
print(unread_msgs)

if(unread_msgs.status_code == 200):
    print("succesful api connection")
    b_value_status = receivedMessages_cleaner(unread_msgs.text)
    print(b_value_status)
    if(b_value_status == 1):
        last_data = msgs[-1].strip()
        last_msg = json.loads(last_data)
        
        query = f"""Here is the query of the buyer along side other information of the buyer:{last_msg}"""
        llm_response = llm_answers(data_items, query)

        




        #pass the llm_response to the seller, send MessageID from query, Item ID and receipientID
        msgID = last_msg[0]["MessageID"]
        itemID = last_msg[0]["ItemID"]
        buyerID = last_msg[0]["SenderID"]
        respond_to_message(msgID, itemID, buyerID, llm_response)



else:
    print("no xml response")
    print(unread_msgs.status_code)


# gather the items  message in the data file.


# write the query + items information + the message -> llm


  