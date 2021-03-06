import device
import switch
import constants
import random
import threading
import datetime
import os

number_of_devices = [i for i in range(5, 25, 1)]
result = []  # stores list of responses, device names, device numbers
path = os.getcwd() + '/results.txt'
print(path)


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
    message1 = switch_.receive_data_packet(current_device.generate_data_packet())
    current_packet = switch_.packet
    recipient = devices_list[current_packet[1] - 1]
    message2 = switch_.send_packet_to_device(recipient)

    return [current_device, recipient, current_packet, message1, message2]


elapsed_time = 0  # pseudo time
max_devices = 0

results_file = open(path, 'w')
results_file.write('Время проведения теста: {time}'.format(time=str(datetime.datetime.now())).split('.')[0])
results_file.write('\n')

for i in range(len(number_of_devices)):
    try:
        elapsed_time = 0
        max_devices = number_of_devices[i]
        devices = [device.Device() for i in range(number_of_devices[i])]
        Switch = switch.Switch(devices)
        constants.DEVICE_COUNTER = 0
        constants.DEVICES_NUMBER = number_of_devices[i]
        test_string = 'ТЕСТ # {n}, абонентов: {number_of_devices}'.format(n=i+1,
                                                                         number_of_devices=constants.DEVICES_NUMBER)
        results_file.write(test_string)
        print(test_string)
        results_file.write('\n')
        obtain_responses(devices, Switch)
        begin = '*********************[Начало цикла обмена]***************\n'
        print(begin)
        results_file.write(begin)
        elapsed_time += len(devices)*1*10**-5  # time to obtain data from N devices
        elapsed_time += 2*10**-4  # switch receives data
        elapsed_time += 5*10**-4  # switch processes data
        elapsed_time += 2*10**-4  # switch sends data
        while len(result) > 0:
            data = handle_responses(devices, Switch)
            results_file.write(data[3])
            results_file.write('\n')
            results_file.write(data[4])
            results_file.write('\n')
            receiver = data[1]
            packet = data[2]
            
            received_str = 'Пакет : {packet} был принят абонентом: {receiver}'.format(packet=str(packet),
                                                                                      receiver=receiver.device_name)
            print(received_str)
            results_file.write(received_str)
            results_file.write('\n')
            elapsed_time_in_msecs = elapsed_time * 1000
            elapsed_str = '[Затраченное время: {0:1.2f} мс.]\n'.format(elapsed_time_in_msecs)
            print(elapsed_str)
            print()
            results_file.write(elapsed_str)
            results_file.write('\n')
            elapsed_time += 2*10**-4
        end = '*********************[Конец цикла обмена]*********************\n'
        print(end)
        results_file.write(end)
        results_file.write('\n')
        if elapsed_time > 5 * 10**-3:
            max_devices = number_of_devices[i]
            break
        
    except KeyboardInterrupt:
        print('\nProgram has been terminated')
maximum_devices_str = 'Максимальное количество абонентов в сети: {max_devices}'.format(max_devices=max_devices)
print(maximum_devices_str)
results_file.write(maximum_devices_str)
results_file.write('\n')
results_file.close()


