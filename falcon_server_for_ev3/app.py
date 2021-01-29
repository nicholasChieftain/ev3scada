import falcon
import bjoern
from sensors import AvailableSensors, DataFromSensor
from socket import gethostname, gethostbyname

IP_ADDRESS_OF_EV3 = gethostbyname(gethostname())
PORT_OF_EV3 = 5000

api = application = falcon.API()

available_sensors = AvailableSensors()
data_from_sensor = DataFromSensor()

api.add_route('/available_sensors', available_sensors)
api.add_route('/data_from_sensor', data_from_sensor)

print('Start listening on', IP_ADDRESS_OF_EV3 + ':' + str(PORT_OF_EV3) + '/')
bjoern.run(api, IP_ADDRESS_OF_EV3, PORT_OF_EV3, reuse_port=True)
