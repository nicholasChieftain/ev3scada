from PyQt5 import QtCore

class CBButton(QtCore.QThread):
    def __init__(self, parent=None):
        QtCore.QThread.__init__(self, parent)
        print(self.boxs_of_ports)
    # def update(self, bofp):
    #     bofp['thread_s'].is_running = not bofp['thread_s'].is_running
    #     if bofp['thread_s'].is_running:
    #         keys = dict()
    #         keys['name'] = bofp['h2'].text()
    #         keys['port'] = bofp['h1'].text()
    #         keys['mode'] = bofp['qbox'].currentText()
    #         print(keys)
    #         bofp['thread_s'].run(keys)