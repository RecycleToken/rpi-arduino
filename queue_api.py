import requests
import json

url = 'http://green-dashboard.mehmetalicakmak.org/api/'

def get_queue():
    response = requests.post(url + 'get-queue', verify=False)
    # print("Queue response: ", json.dumps(response.json(), indent=4)) 
    return response

def update_queue(data):
    response = requests.post(url + 'update-queue', json=data, verify=False)
    # print("Update queue Data: ", json.dumps(data, indent=4))
    # print("Queue update response: ", json.dumps(response.json(), indent=4))
    return response

# example queue data 
# {
#   "status":"Ready",
#   "user": "666451049484d4c3e65fe43c"
# }

def create_transaction(data):
    response = requests.post(url + 'create-transaction', json=data, verify=False)
    # print("Transaction Data: ", json.dumps(data, indent=4))
    # print("Transaction response: ", json.dumps(response.json(), indent=4))
    return response

# example transaction data 
#{
#   "recycled": {
#     "plastic": 10,
#     "glass": 50,
#     "metal": 30,
#     "paper": 20
#   },
#   "user": "666451049484d4c3e65fe43c"
# }
