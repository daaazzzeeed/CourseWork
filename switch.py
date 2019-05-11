class Switch:
    port = 0
    packet = None
    devices = []

    PERMISSION_GRANTED = [1, 1, 0]
    PERMISSION_DENIED = [1, 0, 1]
    ASK_FOR_PERMISSION = [0, -1]

    def __init__(self, devices, switch_name='коммутатор'):
        self.devices = devices
        self.switch_name = switch_name

    def receive_service_packet(self, data):
        if data[1] == self.ASK_FOR_PERMISSION[1]:
            if self.port == 0:
                self.port = 1
                return self.PERMISSION_GRANTED
            else:
                return self.PERMISSION_DENIED
        else:
            return self.PERMISSION_DENIED

    def receive_data_packet(self, data):
        self.packet = data
        message = 'Коммутатор получил пакет ' \
                  + str(self.packet) + ' от абонента: ' + self.devices[self.packet[0]-1].device_name
        print(message)
        return message

    def set_priority(self, packet1, packet2):
        if packet1[0] < packet2[0]:
            return packet1
        else:
            return packet2

    def send_packet_to_device(self, receiver):
        self.devices[self.packet[1]-1].packet = self.packet
        self.port = 0
        message = 'Пакет ' + str(self.packet) + ' был послан абоненту: устройство_' + str(self.packet[1])
        print(message)
        receiver.packet = self.packet
        self.packet = None
        return message

