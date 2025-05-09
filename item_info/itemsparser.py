import xml.etree.ElementTree as ET
import json

def extract_ebay_data(xml_string):
    # Define the namespace
    namespace = {'ns': 'urn:ebay:apis:eBLBaseComponents'}

    # Parse the XML
    root = ET.fromstring(xml_string)

    # Prepare list to hold extracted items
    items = []

    # Loop through each item in the ActiveList
    for item in root.findall('.//ns:ActiveList/ns:ItemArray/ns:Item', namespace):
        # Extract relevant fields
        item_data = {
            'ItemID': item.findtext('ns:ItemID', default='', namespaces=namespace),
            'BuyItNowPrice': item.find('ns:BuyItNowPrice', namespace).text if item.find('ns:BuyItNowPrice', namespace) is not None else '',
            'Title': item.findtext('ns:Title', default='', namespaces=namespace),
            'StartTime': item.find('ns:ListingDetails/ns:StartTime', namespace).text if item.find('ns:ListingDetails/ns:StartTime', namespace) is not None else '',
            'ViewItemURL': item.find('ns:ListingDetails/ns:ViewItemURL', namespace).text if item.find('ns:ListingDetails/ns:ViewItemURL', namespace) is not None else '',
            'Quantity': item.findtext('ns:Quantity', default='', namespaces=namespace),
            'CurrentPrice': item.find('ns:SellingStatus/ns:CurrentPrice', namespace).text if item.find('ns:SellingStatus/ns:CurrentPrice', namespace) is not None else '',
            'ShippingCost': item.find('ns:ShippingDetails/ns:ShippingServiceOptions/ns:ShippingServiceCost', namespace).text if item.find('ns:ShippingDetails/ns:ShippingServiceOptions/ns:ShippingServiceCost', namespace) is not None else '',
            'TimeLeft': item.findtext('ns:TimeLeft', default='', namespaces=namespace),
            'QuantityAvailable': item.findtext('ns:QuantityAvailable', default='', namespaces=namespace),
            'GalleryURL': item.find('ns:PictureDetails/ns:GalleryURL', namespace).text if item.find('ns:PictureDetails/ns:GalleryURL', namespace) is not None else ''
        }

        # Append to the items list
        items.append(item_data)

        with open(f"./item_info/data/item_data.json","a") as file:
                json.dump(items,file)
                file.write("\n")


    return items