from PyQt5 import QtWidgets, QtCore
from .threads import sensor_thread


def create_boxs_of_ports(ports: tuple, bops: dict, obj) -> None:
    for port in ports:
        print(port)
        bops[port] = {'Box': QtWidgets.QHBoxLayout(),
                      'h1': QtWidgets.QLabel(port),
                      'h2': QtWidgets.QLabel('None'),
                      'h3': QtWidgets.QLabel('None'),
                      'cbx': QtWidgets.QCheckBox(),
                      'thread_s': sensor_thread.ThreadOfSensor(),
                      'qbox': QtWidgets.QComboBox()}
        bops[port]['Box'].addWidget(bops[port]['cbx'])
        bops[port]['cbx'].setDisabled(True)
        bops[port]['cbx'].stateChanged.connect(
            lambda state, x=port: obj.on_clicked_to_cbx(state, port=x))
        bops[port]['qbox'].activated.connect(lambda text, x=port: obj.on_clicked_to_cbx(text, port=x))
        bops[port]['thread_s'].signal_from_sensor.connect(obj.on_change_h3,
                                                          QtCore.Qt.QueuedConnection)
        bops[port]['Box'].addWidget(bops[port]['h1'])
        bops[port]['Box'].addWidget(bops[port]['h2'])
        bops[port]['Box'].addWidget(bops[port]['h3'])
        bops[port]['Box'].addWidget(bops[port]['qbox'])
