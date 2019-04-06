import device
import switch

import random
import threading

devices = [device.Device() for i in range(2)]

Switch = switch.Switch(devices)

result = []


def request_permission(device_number):
    result.append(Switch.receive_service_packet(devices[device_number].generate_service_packet()))
    print(devices[device_number].device_type)


for i in range(len(devices)):
    random_time = 0.01*random.random()
    print(random_time)
    t = threading.Timer(random_time, request_permission, [i])
    t.start()
    t.join()

print(result)





#Switch.receive_data_packet(devices[0].generate_data_packet())
#Switch.send_packet_to_device(Switch.packet)
#print(str(Switch.packet) + ' sent')
