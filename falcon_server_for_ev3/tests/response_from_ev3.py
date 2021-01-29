import requests
import ujson
from time import time
from dotenv import load_dotenv
from os import path, getenv

dotenv_path = path.join(path.dirname(__file__), '.env')
if path.exists(dotenv_path):
    load_dotenv(dotenv_path)
    IP_ADDRESS_OF_EV3 = getenv('IP_ADDRESS_EV3')
    PORT_OF_EV3 = getenv('PORT_EV3')
    MAIN_URL = 'http://' + str(IP_ADDRESS_OF_EV3) + ':' + str(PORT_OF_EV3)
else:
    exit("Create and fill in '.env' file.\nNeed two variables:\n1) IP_ADDRESS_EV3;\n2) PORT_EV3.")

methods = ('/sensors', '/color_sensor', '/encoder_sensor')
req = ('http://192.168.0.13:5000/data_from_sensor?name=lego-ev3-color&port=in1&mode=COL-REFLECT', 'http://192.168.0.13:5000/data_from_sensor?name=lego-ev3-color&port=in3&mode=COL-REFLECT')

while True:
    t = time()
    for i in req:
        temp_resp = requests.get(i)
        # print(temp_resp.content)
    print(time() - t)


