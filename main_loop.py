import device
import switch

import random
import threading
import time

devices = [device.Device() for i in range(10)]  # create list of devices
Switch = switch.Switch(devices)  # create switch and unite all devices

result = []


def request_permission(device_num):
    current_device = devices[device_num]
    current_result = list()
    current_result.append(Switch.receive_service_packet(current_device.generate_service_packet()))
    current_result.append(current_device.device_name)
    current_result.append(current_device.device_number)
    result.append(current_result)


try:
    while 1:
        for i in range(len(devices)):
            random_time = 0.01 * random.random()
            t = threading.Timer(random_time, request_permission, [i])
            t.start()

        time.sleep(0.1)  # for asynchronous generation and obtaining
        # print('results: ' + str(result))  # debug purposes
        current_device = devices[result[0][2]-1]
        # print(current_device.device_name)  # debug purposes
        result.clear()

        Switch.receive_data_packet(current_device.generate_data_packet())
        current_packet = Switch.packet
        receiver = devices[current_packet[1]-1]
        Switch.send_packet_to_device(receiver)
        # print('Current packet ' + str(current_packet))  # debug purposes

        print('Packet :' + str(current_packet) + ' has been received by ' + receiver.device_name)
        print()
except KeyboardInterrupt:
    print('\nProgram has been terminated')

