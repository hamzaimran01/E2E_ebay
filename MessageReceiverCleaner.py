import json
def receivedMessages_cleaner(xml_string):
    import xml.etree.ElementTree as ET
    
    # Define the namespace
    namespace = {'ns': 'urn:ebay:apis:eBLBaseComponents'}
    
    # Parse the XML
    root = ET.fromstring(xml_string)

    # Prepare list to hold extracted messages
    messages = []
    b_value = 0
    # See if the root membermessageexhange is there

    exchange = root.findall('.//ns:MemberMessageExchange', namespace)
    

    if exchange:
        # Loop through each MemberMessageExchange

        for exchange in root.findall('.//ns:MemberMessageExchange', namespace):
            item = exchange.find('ns:Item', namespace)
            question = exchange.find('ns:Question', namespace)
            

            # Extract fields with default fallback
        
        
            message = {
                'ItemID': item.findtext('ns:ItemID', default='', namespaces=namespace),
                'ViewItemURL': item.find('ns:ListingDetails/ns:ViewItemURL', namespace).text if item.find('ns:ListingDetails/ns:ViewItemURL', namespace) is not None else '',
                'CurrentPrice': item.find('ns:SellingStatus/ns:CurrentPrice', namespace).text if item.find('ns:SellingStatus/ns:CurrentPrice', namespace) is not None else '',
                'Title': item.findtext('ns:Title', default='', namespaces=namespace),
                'ConditionDisplayName': item.findtext('ns:ConditionDisplayName', default='', namespaces=namespace),
                'SenderID': question.findtext('ns:SenderID', default='', namespaces=namespace),
                'SenderEmail': question.findtext('ns:SenderEmail', default='', namespaces=namespace),
                'Body': question.findtext('ns:Body', default='', namespaces=namespace),
                'MessageID': question.findtext('ns:MessageID', default='', namespaces=namespace),
                'MessageStatus': exchange.findtext('ns:MessageStatus', default='', namespaces=namespace)
            }
        
            messages.append(message)
        
        
            # this keeps on adding messages if they are unread. adjust this later to avoid duplication of message ids based on databases.
            with open(f"{message['SenderID']}data.json","a") as file:
                json.dump(messages,file)
                file.write("\n")
            b_value = 1
            return b_value

    else:
        print("No new messages")
        b_value = 0
        return b_value
    
    