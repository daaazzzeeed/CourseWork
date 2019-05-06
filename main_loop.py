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
    threads = list()
    for i in range(len(devices)):
        random_time = 0.01 * random.random()
        t = threading.Timer(random_time, request_permission, [i])
        t.start()
        time.sleep(0.1)  # delay so you can see what's happening
        threads.append(t)
    for thread in threads:
        thread.join()  # for asynchronous generation and obtaining
    print(result)


def handle_responses():
    current_device = devices[result.pop(0)[2] - 1]
    Switch.receive_data_packet(current_device.generate_data_packet())
    current_packet = Switch.packet
    receiver = devices[current_packet[1] - 1]
    Switch.send_packet_to_device(receiver)

    return [current_device, receiver, current_packet]


try:
    for i in range(10):
        print('TEST NO {n}'.format(n=i+1))
        obtain_responses()
        print('\n[Beginning of exchange cycle]\n')
        elapsed_time = 0  # pseudo time
        elapsed_time += len(devices)*20*10**-5  # time to obtain data from N devices
        elapsed_time += 2*10**-4  # switch receives data
        elapsed_time += 5*10**-4  # switch processes data
        elapsed_time += 2*10**-4  # switch sends data
        while len(result) > 0:
            data = handle_responses()
            receiver = data[1]
            packet = data[2]

            print("""Packet : {packet} has been received by {receiver},
             [elapsed time: {elapsed_time} sec.]"""
            .format(packet=str(packet), receiver=receiver.device_name,
            elapsed_time=elapsed_time))
            print()
            elapsed_time += 2*10**-4
        print('[End of exchange cycle]\n')

except KeyboardInterrupt:
    print('\nProgram has been terminated')

