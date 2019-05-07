import device
import switch
import constants
import random
import threading
import time

number_of_devices = [i for i in range(3, 100, 2)]
result = []  # stores list of responses, device names, device numbers


def request_permission(device_num, devices_list, switch_):
    """Requests permission from switch to send data packet.
Appends list containing response, device name and device number to list result(above)"""
    current_device = devices_list[device_num]
    current_result = list()
    current_result.append(switch_.receive_service_packet(current_device.generate_service_packet()))
    current_result.append(current_device.device_name)
    current_result.append(current_device.device_number)
    result.append(current_result)


def obtain_responses(devices_list, switch_):
    """Obtains responses from devices. Uses function 'request_permission' """
    threads = list()
    for i in range(len(devices_list)):
        random_time = 0.01 * random.random()
        t = threading.Timer(random_time, request_permission, [i, devices_list, switch_])
        t.start()
        threads.append(t)
    for thread in threads:
        thread.join()  # for asynchronous generation and obtaining


def handle_responses(devices_list, switch_):
    current_device = devices_list[result.pop(0)[2] - 1]
    switch_.receive_data_packet(current_device.generate_data_packet())
    current_packet = switch_.packet
    receiver = devices_list[current_packet[1] - 1]
    switch_.send_packet_to_device(receiver)

    return [current_device, receiver, current_packet]


elapsed_time = 0  # pseudo time
max_devices = 0
for i in range(len(number_of_devices)):
    try:
        elapsed_time = 0
        max_devices = number_of_devices[i]
        devices = [device.Device() for i in range(number_of_devices[i])]
        Switch = switch.Switch(devices)
        constants.DEVICE_COUNTER = 0
        constants.DEVICES_NUMBER = number_of_devices[i]
        print('TEST NO {n}, devices: {number_of_devices}'
        .format(n=i+1, number_of_devices=constants.DEVICES_NUMBER))
        obtain_responses(devices, Switch)
        print('*********************[Beginning of exchange cycle]***************\n')
        elapsed_time += len(devices)*1*10**-5  # time to obtain data from N devices
        elapsed_time += 2*10**-4  # switch receives data
        elapsed_time += 5*10**-4  # switch processes data
        elapsed_time += 2*10**-4  # switch sends data
        while len(result) > 0:
            data = handle_responses(devices, Switch)
            receiver = data[1]
            packet = data[2]
            
            print('Packet : {packet} has been received by {receiver}'
            .format(packet=str(packet), receiver=receiver.device_name))
            print('[elapsed time: {0:.5f} sec.]'.format(elapsed_time))
            print()
            elapsed_time += 2*10**-4
        if elapsed_time > 5 * 10**-3:
            max_devices = number_of_devices[i] - 1
            break
        print('*********************[End of exchange cycle]*********************\n')
    except KeyboardInterrupt:
        print('\nProgram has been terminated')
print('Maximum devices in network: {max_devices}'.format(max_devices=max_devices))


