from PyQt5 import QtCore
from ujson import loads

from os import path, getenv
from dotenv import load_dotenv
from sys import exit
from time import sleep
from requests import get, exceptions

dotenv_path = path.join(path.dirname(__file__), '.env')
if path.exists(dotenv_path):
    load_dotenv(dotenv_path)
    IP_ADDRESS_OF_EV3 = getenv('IP_ADDRESS_EV3')
    # IP_ADDRESS_OF_EV3 = 'localhost'
    PORT_OF_EV3 = getenv('PORT_EV3')
    MAIN_URL = 'http://' + str(IP_ADDRESS_OF_EV3) + ':' + str(PORT_OF_EV3)
else:
    exit("Create and fill in '.env' file.\nNeed two variables:\n1) IP_ADDRESS_EV3;\n2) PORT_EV3.")

global keys_for_request


class ThreadOfSensor(QtCore.QThread):
    signal_from_sensor = QtCore.pyqtSignal(dict)

    def __init__(self, parent=None, keys=dict):
        QtCore.QThread.__init__(self, parent)
        self.is_running = False
        self.keys = keys

    def run(self):
        self.is_running = True
        while self.is_running:
            try:
                response = get(MAIN_URL + '/data_from_sensor', params=self.keys)
                if response.status_code == 200:
                    self.signal_from_sensor.emit(loads(response.content))
            except exceptions.ConnectionError:
                self.signal_from_thread.emit({'error': 'Trying to reconnect'})
                sleep(1)
            self.yieldCurrentThread()

    @property
    def keys(self):
        return self.__keys

    @keys.setter
    def keys(self, keys):
        self.__keys = keys


class CheckAvailableDevice(QtCore.QThread):
    signal_from_thread = QtCore.pyqtSignal(dict)

    def __init__(self, parent=None):
        QtCore.QThread.__init__(self, parent)
        self.dict_of_sensors = dict()

    def update(self):
        try:
            response = get(MAIN_URL + '/available_sensors')

            if response.status_code == 200:
                self.signal_from_thread.emit(loads(response.content))
            elif response.status_code == 204:
                self.signal_from_thread.emit({'error': 'No sensors connected'})
        except exceptions.ConnectionError:
            self.signal_from_thread.emit({'error': 'Trying to reconnect'})
