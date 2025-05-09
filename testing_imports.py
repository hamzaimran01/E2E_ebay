from email import message
import os
import json


file_path_hamza = os.path.join(os.getcwd(), 'hamzadur_0data.json')
with open (file_path_hamza,'r') as message_data:
    msgs = message_data.readlines()
last_line = msgs[-1].strip()

last_data = json.loads(last_line)
print(last_data)
print(last_data[0]['ItemID'])

