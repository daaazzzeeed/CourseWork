import random
import constants


class Device:
    """Specifies device in a network"""
    packet = None
    device_number = None

    PERMISSION_GRANTED = [1, 1, 0]
    PERMISSION_DENIED = [1, 0, 1]
    ASK_FOR_PERMISSION = [0, -1]

    def __init__(self, device_name='device_'):
        """Creates device with given name or with name device_[device_counter]"""
        self.device_name = device_name + str(constants.DEVICE_COUNTER + 1)
        constants.DEVICE_COUNTER += 1
        self.device_number = constants.DEVICE_COUNTER


    def generate_service_packet(self):
        """Generates service packet asking for permission"""
        if constants.DEVICE_COUNTER != 0:
            self.ASK_FOR_PERMISSION[0] = constants.DEVICE_COUNTER 
        else:
            self.ASK_FOR_PERMISSION[0] = 1
        serv_pack = self.ASK_FOR_PERMISSION
        return serv_pack

    def wait_for_permission(self, reply):
        """Waits until obtaining permission from switch"""
        if reply == self.PERMISSION_GRANTED:
            return True
        elif reply == self.PERMISSION_DENIED:
            return False
        else:
            return False

    def generate_data_packet(self):
        """Generates packet specifying data"""
        data = [random.randint(0, 10) for i in range(constants.PACKET_LENGTH)]
        data[0] = self.device_number
        send_to = random.randint(1, constants.DEVICES_NUMBER)
        data[1] = send_to
        return data

    def receive_packet(self, data):
        self.packet = data

