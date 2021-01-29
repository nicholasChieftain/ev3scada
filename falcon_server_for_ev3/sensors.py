import ujson
import falcon
from schemas import *

# from ev3dev2.sensor.lego import ColorSensor
# from ev3dev2 import DeviceNotFound

from ev3dev2 import list_devices
from ev3dev2.sensor import list_sensors, Sensor
from ev3dev2.motor import list_motors, Motor
from ev3dev2.port import LegoPort

# names_of_sensor = {'cs': 'lego-ev3-color',
#                    'gs': 'lego-ev3-gyro',
#                    'us': 'lego-ev3-us',
#                    'ts': 'lego-ev3-touch'}


numbered_ports = ('in1', 'in2', 'in3', 'in4')
lettered_ports = ('outA', 'outB', 'outC', 'outD')

names_of_sensors = ('lego-ev3-color',
                    'lego-ev3-gyro',
                    'lego-ev3-us',
                    'lego-ev3-touch')

names_of_motors = ('lego-ev3-l-motor',
                  'lego-ev3-m-motor')

modes_of_cs = ("COL-REFLECT", "COL-AMBIENT", "COL-COLOR", "REF-RAW", "RGB-RAW", "COL-CAL")

pattern_for_name_of_port = 'ev3-ports:'

sensorschema = SensorSchema()
availablesensor = AvailableSensorSchema()

check_port = lambda x: True if 'no' in LegoPort(x).status else False


def Dev_init(self, port):
    self.port = port
    self.motor = False
    if self.port in numbered_ports:
        self.motor = False
    elif self.port:
        self.motor = True


def getmode(self):
    self._mode = Sensor(self.port).mode
    return self._mode


def setmode(self, mode):
    Sensor(self.port).mode = mode


Dev = type('Dev', (),
           {'__init__': Dev_init,
            'value': lambda self:
                Motor(self.port).position if self.motor
                else Sensor(self.port).value(),
            'modes':
                lambda self: None if self.motor
                else Sensor(self.port).modes,
            'mode': property(getmode, setmode)
            })


class DataFromSensor(object):
    def on_get(self, req, resp):
        name_of_sensor = req.get_param('name', required=True)
        port = req.get_param('port', required=True)
        mode = req.get_param('mode', required=False, default=None)

        if name_of_sensor not in names_of_sensors and name_of_sensor not in names_of_motors:
            raise falcon.HTTPNotAcceptable(description='There is no such name_of_sensor')
        else:
            if port not in numbered_ports and port not in lettered_ports:
                raise falcon.HTTPNotAcceptable(description='There is no such port')
        if check_port(port):
            raise falcon.HTTPNotFound(description='Device not connected')

        temp_device = Dev(port)

        if mode and mode in modes_of_cs and not temp_device.motor:
            temp_device.mode = mode
        elif mode and not (mode in modes_of_cs):
            raise falcon.HTTPNotAcceptable(description='There is no such mode for this sensor')

        val = temp_device.value()
        sensor_data = SensorData(name_of_sensor, port, val)

        resp.body = ujson.dumps(sensorschema.dump(sensor_data))
        resp.status = falcon.HTTP_200


class AvailableSensors(object):
    def on_get(self, req, resp):
        data = dict()
        for port in numbered_ports:
            for name in names_of_sensors:
                checking_port = list(list_sensors(driver_name=name, address=port))
                if checking_port:
                    temp_sensor = Sensor(address=port)
                    data[port] = {'name': name, 'modes': temp_sensor.modes}

        for port in lettered_ports:
            for name in names_of_motors:
                checking_port = list(list_motors(driver_name=name, address=port))
                if checking_port:
                    temp_motor = Motor(address=port)
                    data[port] = {'name': name, 'modes': None}

        if len(data) != 0:
            resp.body = ujson.dumps(data)
            resp.status = falcon.HTTP_200
        else:
            resp.status = falcon.HTTP_204
