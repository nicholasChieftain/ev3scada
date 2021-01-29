import ujson
import falcon
from random import randint

numbered_ports = ('in1', 'in2', 'in3', 'in4')
lettered_ports = ('outA', 'outB', 'outC', 'outD')

names_of_sensors = ('lego-ev3-color',
                    'lego-ev3-gyro',
                    'lego-ev3-us',
                    'lego-ev3-touch')

names_of_motors = {'lm': 'lego-ev3-l-motor',
                   'mm': 'lego-ev3-m-motor'}

modes_of_cs = ("COL-REFLECT", "COL-AMBIENT", "COL-COLOR", "REF-RAW", "RGB-RAW", "COL-CAL")

available_ports = ('in2', 'in3')
available_sensor = ('cs', 'us')
connected_sensor = {'in2':'lego-ev3-color', 'in3':'lego-ev3-color',}

pattern_for_name_of_port = 'ev3-ports:'

def list_sensors(driver_name=str, address=str):
    try:
        if connected_sensor[address] == driver_name:
            return [address]
        else:
            return []
    except KeyError:
        pass

class Sensor:
    def __init__(self, address=str, mode=str, driver_name=str):
        self.__value = randint(-100, 100)
        self.__driver_name = driver_name
        if self.__driver_name == 'lego-ev3-color':
            self.__mode = modes_of_cs[0]

    @property
    def value(self):
        self.__value = randint(-100, 100)
        return self.__value

    @property
    def modes(self):
        if self.__driver_name == 'lego-ev3-color':
            return modes_of_cs

    @property
    def mode(self):
        return self.__mode



class DataFromSensor(object):
    def on_get(self, req, resp):
        data = dict()
        name_of_sensor = req.get_param('name', required=True)
        port = req.get_param('port', required=True)
        mode = req.get_param('mode', required=False, default=None)

        if name_of_sensor not in names_of_sensors:
            raise falcon.HTTPNotAcceptable(description='There is no such name_of_sensor')
        if port not in numbered_ports:
            raise falcon.HTTPNotAcceptable(description='There is no such port')

        temp_port = list_sensors(driver_name=name_of_sensor, address=port)

        if not temp_port:
            raise falcon.HTTPNotFound(description='Sensor not connected')
        temp_sensor = Sensor(address=port)
        #
        # if mode and mode in modes_of_cs:
        #     temp_sensor.mode = mode
        # elif mode and not (mode in modes_of_cs):
        #     raise falcon.HTTPNotAcceptable(description='There is no such mode for this sensor')

        value = temp_sensor.value
        print(value)
        data = {"value": value,
                                                 "port": port,
                                                 "mode": mode,
                                                 "avalibale_modes": modes_of_cs}
        resp.body = ujson.dumps(data)
        resp.status = falcon.HTTP_200


class AvailableSensors(object):
    def on_get(self, req, resp):
        data = dict()
        for port in numbered_ports:
            for name in names_of_sensors:
                checking_port = list_sensors(driver_name=name, address=port)
                if checking_port:
                    temp_sensor = Sensor(address=port, driver_name=name)
                    data[port] = {'name': name, 'modes': temp_sensor.modes}

        # for port in lettered_ports:
        #     for name in names_of_motors:
        #         checking_port = list(list_motors(driver_name=names_of_motors[name], address=port))
        #         if checking_port:
        #             temp_motor = Motor(address=port)
        #             data[port] = {'name': names_of_motors[name], 'commands': temp_motor.commands}

        if len(data) != 0:
            resp.body = ujson.dumps(data)
            resp.status = falcon.HTTP_200
        else:
            resp.status = falcon.HTTP_204
