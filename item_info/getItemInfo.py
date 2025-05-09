import sys
import os


current_directory = os.path.dirname(os.path.abspath(__file__))
parent_directory = os.path.dirname(current_directory)
# Add the parent directory to the sys.path
sys.path.append(parent_directory)

# Now import everything from tokens
from tokens import *


import requests

from itemsparser import extract_ebay_data




EBAY_APP_ID = APPLICATION_ID
EBAY_CERT_ID = CERTIFICATE_ID
EBAY_DEV_ID = DEVELOPER_ID
EBAY_USER_TOKEN = AUTH_TOKEN


headers = {
    "X-EBAY-API-CALL-NAME": "GetMyeBaySelling",
    "X-EBAY-API-SITEID": "0",
    "X-EBAY-API-COMPATIBILITY-LEVEL": "967",
    "X-EBAY-API-DEV-NAME": EBAY_DEV_ID,
    "X-EBAY-API-APP-NAME": EBAY_APP_ID,
    "X-EBAY-API-CERT-NAME": EBAY_CERT_ID,
    "X-EBAY-API-REQUEST-ENCODING": "XML",
    "Content-Type": "text/xml"
}
xml_payload = f"""<GetMyeBaySellingRequest xmlns="urn:ebay:apis:eBLBaseComponents">
  <RequesterCredentials>
    <eBayAuthToken>{EBAY_USER_TOKEN}</eBayAuthToken>
  </RequesterCredentials>
  <ActiveList>
    <Include>true</Include>
    <Pagination>
      <EntriesPerPage>100</EntriesPerPage>
      <PageNumber>1</PageNumber>
    </Pagination>
  </ActiveList>
  <SoldList>
    <Include>true</Include>
    <Pagination>
      <EntriesPerPage>100</EntriesPerPage>
      <PageNumber>1</PageNumber>
    </Pagination>
  </SoldList>
  <DetailLevel>ReturnAll</DetailLevel>
</GetMyeBaySellingRequest>
"""

response = requests.post(EBAY_API_URL, data=xml_payload, headers=headers)

print(response.text)

return_items = extract_ebay_data(response.text)
print(return_items)
