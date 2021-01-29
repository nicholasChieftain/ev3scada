from lima import Schema, fields


class SensorData:
    def __init__(self, name: str, port: str, value: float):
        self.name = name
        self.port = port
        self.value = value


class SensorSchema(Schema):
    name = fields.String()
    port = fields.String()
    value = fields.Float()


class AvailableSensor:
    def __init__(self, name: str, modes: list,):
        self.name = name
        self.modes = modes


class AvailableSensorSchema(Schema):
    name = fields.String()
    modes = fields.String()