from pypresence import Presence
import time
import requests
import json

######### Global Parameters #########
client_id = 'your id' # Put your application client ID here
access_key = 'your key' # Put the minerstat access key here
worker_1 = 'your worker name' # Put your first worker name here. If you have only one worker, comment the other worker lines
worker_2 = 'your 2nd worker name' # Put your second worker name here
worker_3 = 'your 3rd worker name' # Put your third worker name here
#####################################

temp = 0
RPC = Presence(client_id, pipe=0)  # Initialize the client class
RPC.connect() # Start the handshake loop
if 'worker_2' in globals():
    wor2 = True
    worker_2 = worker_2.upper()
else:
    wor2 = False
if 'worker_3' in globals():
    wor3 = True
    worker_3 = worker_3.upper()
else:
    wor3 = False
worker_1 = worker_1.upper()

while True:  # The presence will stay on as long as the program is running
    
    response = requests.get("https://api.minerstat.com/v2/stats/"+access_key)
    json_response = response.text
    y = json.loads(json_response)
    hashrate_one = float(y[worker_1]["mining"]["hashrate"]["hashrate"])
    if wor2:
        hashrate_two = float(y[worker_2]["mining"]["hashrate"]["hashrate"])
    if wor3:
        hashrate_three = float(y[worker_3]["mining"]["hashrate"]["hashrate"])
    if wor2 and wor3:
        speed = str(round(hashrate_one + hashrate_two + hashrate_three, 2))
        for i in y[worker_1]["hardware"]:
            current_temp = int(i["temp"])
            if current_temp > temp:
                temp = current_temp
        for i in y[worker_2]["hardware"]:
            current_temp = int(i["temp"])
            if current_temp > temp:
                temp = current_temp
        for i in y[worker_3]["hardware"]:
            current_temp = int(i["temp"])
            if current_temp > temp:
                temp = current_temp
    elif wor2 is True and wor3 is False:
        speed = str(round(hashrate_one + hashrate_two, 2))
        for i in y[worker_1]["hardware"]:
            current_temp = int(i["temp"])
            if current_temp > temp:
                temp = current_temp
        for i in y[worker_2]["hardware"]:
            current_temp = int(i["temp"])
            if current_temp > temp:
                temp = current_temp
    elif wor2 is False and wor3 is False:
        speed = str(round(hashrate_one, 2))
        for i in y[worker_1]["hardware"]:
            current_temp = int(i["temp"])
            if current_temp > temp:
                temp = current_temp
    print(RPC.update(state="Max temp - " + str(temp) + "°C", details="Speed - " + speed + " MH/s"))  # Set the presence
    time.sleep(15) # Can only update rich presence every 15 seconds