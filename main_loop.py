import device
import switch

import random
import threading
import time

devices = [device.Device() for i in range(10)]  # create list of devices
Switch = switch.Switch(devices)  # create switch and unite all devices

result = []  # stores list of responses, device names, device numbers


def request_permission(device_num):
    """Requests permission from switch to send data packet.
Appends list containing response, device name and device number to list result(above)"""
    current_device = devices[device_num]
    current_result = list()
    current_result.append(Switch.receive_service_packet(current_device.generate_service_packet()))
    current_result.append(current_device.device_name)
    current_result.append(current_device.device_number)
    result.append(current_result)


def obtain_responses():
    """Obtains responses from devices. Uses function 'request_permission' """
    for i in range(len(devices)):
        random_time = 0.01 * random.random()
        t = threading.Timer(random_time, request_permission, [i])
        t.start()
    time.sleep(1)  # for asynchronous generation and obtaining
    print(result)


def handle_responses():
    current_device = devices[result.pop(0)[2] - 1]
    Switch.receive_data_packet(current_device.generate_data_packet())
    current_packet = Switch.packet
    receiver = devices[current_packet[1] - 1]
    Switch.send_packet_to_device(receiver)

    return [current_device, receiver, current_packet]


try:
    while 1:
        obtain_responses()
        print('\n[Beginning of exchange cycle]\n')
        while len(result) > 0:
            data = handle_responses()

            receiver = data[1]
            packet = data[2]

            print('Packet :' + str(packet) + ' has been received by ' + receiver.device_name)
            print()
        print('[End of exchange cycle]\n')

except KeyboardInterrupt:
    print('\nProgram has been terminated')

