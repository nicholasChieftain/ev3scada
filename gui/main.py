from PyQt5 import QtWidgets, QtCore
from pyqtgraph import PlotWidget, plot, mkPen
from pyqtgraph import PlotWidget
from gui.utils import create_boxs_of_ports
from random import choice

# colors =

import sys

from gui.threads import sensor_thread

numbered_ports = ('in1', 'in2', 'in3', 'in4')
lettered_ports = ('outA', 'outB', 'outC', 'outD')

names_of_sensors = ('lego-ev3-color',
                    'lego-ev3-gyro',
                    'lego-ev3-us',
                    'lego-ev3-touch')

names_of_motors = ('lego-ev3-l-motor',
                   'lego-ev3-m-motor')

#
# def update_request():
#
#

class ScadaWindow(QtWidgets.QWidget):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.boxs_of_ports = dict()
        self.main_layout = QtWidgets.QVBoxLayout()

        self.graphWidget = PlotWidget()
        self.graphWidget.setBackground('w')
        self.x = list(range(100))
        self.pen = mkPen(color=(255, 0, 0))
        self.main_layout.addWidget(self.graphWidget)
        self.data_lines = {}
        create_boxs_of_ports(numbered_ports, self.boxs_of_ports, self)
        create_boxs_of_ports(lettered_ports, self.boxs_of_ports, self)

        for key in self.boxs_of_ports:
            self.data_lines[key] = {'x': self.x.copy(),'y': [0 for i in range(len(self.x))]}
            self.main_layout.addLayout(self.boxs_of_ports[key]['Box'])

        self.button_check_available_sensors = QtWidgets.QPushButton('Обновить доступные порты')
        self.thread_check_available_sensors = sensor_thread.CheckAvailableDevice()
        self.thread_check_available_sensors.signal_from_thread.connect(self.on_thread_available_sensors,
                                                                       QtCore.Qt.QueuedConnection)
        self.button_check_available_sensors.clicked.connect(self.thread_check_available_sensors.update)

        self.main_layout.addWidget(self.button_check_available_sensors)

        self.setLayout(self.main_layout)


    def on_thread_available_sensors(self, s):
        print(s)
        if 'error' not in s:
            for key in s:
                if key in self.boxs_of_ports.keys():
                    self.boxs_of_ports[key]['cbx'].setDisabled(False)
                    self.boxs_of_ports[key]['h2'].setText(s[key]['name'])
                    print(self.boxs_of_ports[key]['h2'].text())
                    if s[key]['modes'] is None:
                        self.boxs_of_ports[key]['qbox'].setDisabled(True)
                    else:
                        self.boxs_of_ports[key]['qbox'].addItems(s[key]['modes'])
        else:
            print(s['error'])

    def on_clicked_to_cbx(self, state, port):
        print(port, state)
        keys_for_request = dict()
        print(self.data_lines[port])
        self.data_lines[port]['gw'] = self.graphWidget.plot(self.data_lines[port]['x'], self.data_lines[port]['y'], name=str(port), symbol='+', symbolSize=10)
        if state:
            keys_for_request['name'] = self.boxs_of_ports[port]['h2'].text()
            keys_for_request['port'] = self.boxs_of_ports[port]['h1'].text()
            keys_for_request['mode'] = self.boxs_of_ports[port]['qbox'].currentText()
            self.boxs_of_ports[port]['thread_s'].keys = keys_for_request
            self.boxs_of_ports[port]['thread_s'].start()
        else:
            self.boxs_of_ports[port]['thread_s'].is_running = False

    # def on_clicked_to_qbx(self, text, port):


    def on_change_h3(self, s):
        print(s)
        if 'error' not in s:
            self.boxs_of_ports[s['port']]['h3'].setText(str(s['value']))
            self.data_lines[s['port']]['x'] = self.data_lines[s['port']]['x'][1:]
            self.data_lines[s['port']]['x'].append(self.data_lines[s['port']]['x'][-1] + 1)
            self.data_lines[s['port']]['y'] = self.data_lines[s['port']]['y'][1:]
            self.data_lines[s['port']]['y'].append(s['value'])
            self.data_lines[s['port']]['gw'].setData(self.data_lines[s['port']]['x'], self.data_lines[s['port']]['y'])

        else:
            print(s['error'])



if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = ScadaWindow()
    print(type(window))
    # window.resize(800, 600)
    window.show()
    sys.exit(app.exec_())
