import random
import numpy as np
import matplotlib.pyplot as plt
from collections import deque

service_policy = 'FIFO'
X = 2
Y = 0.2
T = 100
PROCESSORS_NUM = 3
processors_times = list()
for i in range(PROCESSORS_NUM):
    processors_times.append([0, 0])
LENGTH_LIMIT = [3]
high_weight = 3
medium_weight = 2
low_weight = 1
packets = list()
dropped = 0
time = 0
total_len_queue = 0
wait = 0
proc_use = list()
for i in range(PROCESSORS_NUM):
    proc_use.append(0)


def generate_random_priority():
    need = random.random()
    if need < 0.5:
        result = "Low Priority"
    elif 0.5 <= need < 0.8:
        result = "Medium Priority"
    else:
        result = "High Priority"
    return result


packets.append((0, generate_random_priority()))
while time < T:
    packet_time_between_arrival = np.random.exponential(1 / X)
    process_time = np.random.exponential(Y)
    time += packet_time_between_arrival
    packets.append((time, process_time, generate_random_priority()))

packets = ((0, 4), (1, 4), (2, 4), (3, 5), (4, 6), (5, 7), (6, 6), (7, 10), (8, 12), (12, 7))
t = 0
old_t = 0
o = 0
check = 0
index = 1
iter = 0
if service_policy == "FIFO":
    queue = deque()
    packet = packets[0]
    while iter != len(packets):
        iter += 1
        z = t
        for i in range(len(processors_times)):
            if processors_times[i][1] == 0:
                o += 1
                continue
            else:
                z = processors_times[i][1]
            if o == len(processors_times) - 1:
                z = processors_times[i][1]
        total_len_queue += (t - old_t) * len(queue)
        print(total_len_queue)
        old_t = t
        t = min(packet[0], z)
        print("t: ", end=" ")
        print(t)
        print(processors_times)
        print(queue)
        time, priority = packet
        if len(queue) <= LENGTH_LIMIT[0]:
            for i in range(len(queue)):
                least = list()
                for j in range(PROCESSORS_NUM):
                    if time < processors_times[j][1]:
                        continue
                    else:
                        least.append((j, processors_times[j][1]))
                if len(least) == 0:
                    queue.append(packet)
                    packet = packets[index]
                    index += 1
                    if index == len(packets):
                        index = len(packets) - 1
                        check = 1
                    break
                else:
                    mini = [-1, T + 100]
                    for k in range(len(least)):
                        if least[k][1] <= mini[1]:
                            mini = [least[k][0], least[k][1]]
                    need = mini[0]

                    start = processors_times[need][1]
                    wait += start - queue[0][0]
                    end = processors_times[need][1] + queue[0][1]
                    processors_times[need][0] = start
                    processors_times[need][1] = end
                    proc_use[need] += end - start
                    print(processors_times)
                    queue.popleft()
                    print(queue)
            if len(queue) == 0:
                least = list()
                for j in range(PROCESSORS_NUM):
                    if time < processors_times[j][1]:
                        continue
                    else:
                        least.append((j, processors_times[j][1]))
                if len(least) == 0:
                    queue.append(packet)
                    packet = packets[index]
                    index += 1
                    if index == len(packets):
                        index = len(packets) - 1
                        check = 1
                    continue
                else:
                    mini = [-1, T + 100]
                    for k in range(len(least)):
                        if least[k][1] <= mini[1]:
                            mini = [least[k][0], least[k][1]]

                    need = mini[0]
                    start = packet[0]
                    end = packet[0] + packet[1]
                    processors_times[need] = [start, end]
                    proc_use[need] += end - start
                    packet = packets[index]
                    index += 1
                    if index == len(packets):
                        index = len(packets) - 1
                        check = 1

        if len(queue) > LENGTH_LIMIT[0]:
            dropped += 1
            print(dropped)
            continue
    while len(queue) > 0:
        print(queue)
        mini = [-1, T + 100]

        for k in range(len(processors_times)):
            if processors_times[k][1] <= mini[1]:
                mini = [k, processors_times[k][1]]
        need = mini[0]

        start = processors_times[need][1]
        total_len_queue += start - queue[0][0]
        wait = total_len_queue
        end = processors_times[need][1] + queue[0][1]
        proc_use[need] += end - start
        processors_times[need][0] = start
        processors_times[need][1] = end
        print(processors_times)

        queue.popleft()
    max_end = 0
    for i in range(len(processors_times)):
        if processors_times[i][1] > max_end:
            max_end = processors_times[i][1]
    mean_queue = total_len_queue / max_end
    mean_time_queue = wait / len(packets)
    print(mean_queue)
    print(mean_time_queue)
    for i in range(PROCESSORS_NUM):
        proc_use[i] /= max_end
    print(proc_use)
    print(dropped)
    print(queue)



elif service_policy == "NPPS":
    queue = deque()
    packet = packets[0]
    while iter != len(packets):
        iter += 1
        z = t
        for i in range(len(processors_times)):
            if processors_times[i][1] == 0:
                o += 1
                continue
            else:
                z = processors_times[i][1]
            if o == len(processors_times) - 1:
                z = processors_times[i][1]
        total_len_queue += (t - old_t) * len(queue)
        print(total_len_queue)
        old_t = t
        t = min(packet[0], z)
        print("t: ", end=" ")
        print(t)
        print(processors_times)
        print(queue)
        time, priority = packet
        if len(queue) <= LENGTH_LIMIT[0]:
            for i in range(len(queue)):
                least = list()
                for j in range(PROCESSORS_NUM):
                    if time < processors_times[j][1]:
                        continue
                    else:
                        least.append((j, processors_times[j][1]))
                if len(least) == 0:
                    queue.append(packet)
                    z = len(queue) - 1
                    while z >= 0:
                        if packet[2] == "High Priority" and (
                                queue[z - 1][2] == "Low Priority" or queue[z - 1][2] == "Medium Priority"):
                            need = queue[z - 1]
                            queue[z] = need
                            queue[z - 1] = packet
                            z -= 1
                            continue
                        elif packet[2] == "Medium Priority" and queue[z - 1][2] == "Low Priority":
                            need = queue[z - 1]
                            queue[z] = need
                            queue[z - 1] = packet
                            z -= 1
                            continue
                        break
                    packet = packets[index]
                    index += 1
                    if index == len(packets):
                        index = len(packets) - 1
                        check = 1
                    break
                else:
                    mini = [-1, T + 100]
                    for k in range(len(least)):
                        if least[k][1] <= mini[1]:
                            mini = [least[k][0], least[k][1]]
                    need = mini[0]

                    start = processors_times[need][1]
                    wait += start - queue[0][0]
                    end = processors_times[need][1] + queue[0][1]
                    processors_times[need][0] = start
                    processors_times[need][1] = end
                    proc_use[need] += end - start
                    print(processors_times)
                    queue.popleft()
                    print(queue)
            if len(queue) == 0:
                least = list()
                for j in range(PROCESSORS_NUM):
                    if time < processors_times[j][1]:
                        continue
                    else:
                        least.append((j, processors_times[j][1]))
                if len(least) == 0:
                    queue.append(packet)
                    packet = packets[index]
                    index += 1
                    if index == len(packets):
                        index = len(packets) - 1
                        check = 1
                    continue
                else:
                    mini = [-1, T + 100]
                    for k in range(len(least)):
                        if least[k][1] <= mini[1]:
                            mini = [least[k][0], least[k][1]]

                    need = mini[0]
                    start = packet[0]
                    end = packet[0] + packet[1]
                    processors_times[need] = [start, end]
                    proc_use[need] += end - start
                    packet = packets[index]
                    index += 1
                    if index == len(packets):
                        index = len(packets) - 1
                        check = 1

        if len(queue) > LENGTH_LIMIT[0]:
            dropped += 1
            print(dropped)
            continue
    while len(queue) > 0:
        print(queue)
        mini = [-1, T + 100]

        for k in range(len(processors_times)):
            if processors_times[k][1] <= mini[1]:
                mini = [k, processors_times[k][1]]
        need = mini[0]

        start = processors_times[need][1]
        total_len_queue += start - queue[0][0]
        wait = total_len_queue
        end = processors_times[need][1] + queue[0][1]
        proc_use[need] += end - start
        processors_times[need][0] = start
        processors_times[need][1] = end
        print(processors_times)

        queue.popleft()
    max_end = 0
    for i in range(len(processors_times)):
        if processors_times[i][1] > max_end:
            max_end = processors_times[i][1]
    mean_queue = total_len_queue / max_end
    mean_time_queue = wait / len(packets)
    print(mean_queue)
    print(mean_time_queue)
    for i in range(PROCESSORS_NUM):
        proc_use[i] /= max_end
    print(proc_use)
    print(queue)
    print(dropped)

else:
    weight = 10
    high_queue = deque()
    medium_queue = deque()
    low_queue = deque()
    packet = packets[0]
    while iter != len(packets):
        iter += 1
        z = t
        for i in range(len(processors_times)):
            if processors_times[i][1] == 0:
                o += 1
                continue
            else:
                z = processors_times[i][1]
            if o == len(processors_times) - 1:
                z = processors_times[i][1]
        # total_len_queue += (t - old_t) * len(queue)
        print(total_len_queue)
        old_t = t
        t = min(packet[0], z)
        print("t: ", end=" ")
        print(t)
        print(processors_times)
        time, priority = packet
        if priority == "High Priority" and weight > 5:
            if len(high_queue) <= LENGTH_LIMIT[0]:
                for i in range(len(high_queue)):
                    least = list()
                    for j in range(PROCESSORS_NUM):
                        if time < processors_times[j][1]:
                            continue
                        else:
                            least.append((j, processors_times[j][1]))
                    if len(least) == 0:
                        high_queue.append(packet)
                        packet = packets[index]
                        index += 1
                        if index == len(packets):
                            index = len(packets) - 1
                            check = 1
                        break
                    mini = [-1, T + 100]
                    for k in range(len(least)):
                        if least[k][1] <= mini[1]:
                            mini = [least[k][0], least[k][1]]
                    need = mini[0]

                    start = processors_times[need][1]
                    wait += start - high_queue[0][0]
                    end = processors_times[need][1] + high_queue[0][1]
                    processors_times[need][0] = start
                    processors_times[need][1] = end
                    proc_use[need] += end - start
                    print(processors_times)
                    high_queue.popleft()
                    weight -= 1
                    print(high_queue)
                if len(high_queue) == 0 and weight > 5:
                    least = list()
                    for j in range(PROCESSORS_NUM):
                        if time < processors_times[j][1]:
                            continue
                        else:
                            least.append((j, processors_times[j][1]))
                    if len(least) == 0:
                        high_queue.append(packet)
                        packet = packets[index]
                        index += 1
                        if index == len(packets):
                            index = len(packets) - 1
                            check = 1
                        continue
                    else:
                        mini = [-1, T + 100]
                        for k in range(len(least)):
                            if least[k][1] <= mini[1]:
                                mini = [least[k][0], least[k][1]]

                        need = mini[0]
                        start = packet[0]
                        end = packet[0] + packet[1]
                        processors_times[need] = [start, end]
                        proc_use[need] += end - start
                        packet = packets[index]
                        index += 1
                        if index == len(packets):
                            index = len(packets) - 1
                            check = 1
                elif len(high_queue) == 0 and weight <= 5:
                    high_queue.append(packet)
                    packet = packets[index]
                    index += 1
                    if index == len(packets):
                        index = len(packets) - 1
                    break

            else:
                dropped += 1
                continue

        elif priority == "High Priority" and weight <= 5:
            if len(high_queue) <= LENGTH_LIMIT[0]:
                high_queue.append(packet)
                packet = packets[index]
                index += 1
                if index == len(packets):
                    index = len(packets) - 1
                    check = 1
                break
            else:
                dropped += 1
                continue
        if priority == "Medium Priority" and 2 < weight <= 5:
            if len(medium_queue) <= LENGTH_LIMIT[1]:
                for i in range(len(medium_queue)):
                    least = list()
                    for j in range(PROCESSORS_NUM):
                        if time < processors_times[j][1]:
                            continue
                        else:
                            least.append((j, processors_times[j][1]))
                    if len(least) == 0:
                        medium_queue.append(packet)
                        packet = packets[index]
                        index += 1
                        if index == len(packets):
                            index = len(packets) - 1
                            check = 1
                        break
                    mini = [-1, T + 100]
                    for k in range(len(least)):
                        if least[k][1] <= mini[1]:
                            mini = [least[k][0], least[k][1]]
                    need = mini[0]

                    start = processors_times[need][1]
                    wait += start - high_queue[0][0]
                    end = processors_times[need][1] + high_queue[0][1]
                    processors_times[need][0] = start
                    processors_times[need][1] = end
                    proc_use[need] += end - start
                    print(processors_times)
                    medium_queue.popleft()
                    weight -= 1
                    print(high_queue)
                if len(medium_queue) == 0 and 2 < weight <= 5:
                    least = list()
                    for j in range(PROCESSORS_NUM):
                        if time < processors_times[j][1]:
                            continue
                        else:
                            least.append((j, processors_times[j][1]))
                    if len(least) == 0:
                        medium_queue.append(packet)
                        packet = packets[index]
                        index += 1
                        if index == len(packets):
                            index = len(packets) - 1
                            check = 1
                        continue
                    else:
                        mini = [-1, T + 100]
                        for k in range(len(least)):
                            if least[k][1] <= mini[1]:
                                mini = [least[k][0], least[k][1]]

                        need = mini[0]
                        start = packet[0]
                        end = packet[0] + packet[1]
                        processors_times[need] = [start, end]
                        proc_use[need] += end - start
                        packet = packets[index]
                        index += 1
                        if index == len(packets):
                            index = len(packets) - 1
                            check = 1
                elif len(medium_queue) == 0 and (weight <= 2 or weight > 5):
                    high_queue.append(packet)
                    packet = packets[index]
                    index += 1
                    if index == len(packets):
                        index = len(packets) - 1
                    break

            else:
                dropped += 1
                continue

        elif priority == "Medium Priority" and weight <= 2 or weight > 5:
            if len(medium_queue) <= LENGTH_LIMIT[1]:
                medium_queue.append(packet)
                packet = packets[index]
                index += 1
                if index == len(packets):
                    index = len(packets) - 1
                    check = 1
                break
            else:
                dropped += 1
                continue
        if priority == "Low Priority" and 0 < weight <= 2:
            if len(low_queue) <= LENGTH_LIMIT[2]:
                for i in range(len(low_queue)):
                    least = list()
                    for j in range(PROCESSORS_NUM):
                        if time < processors_times[j][1]:
                            continue
                        else:
                            least.append((j, processors_times[j][1]))
                    if len(least) == 0:
                        low_queue.append(packet)
                        packet = packets[index]
                        index += 1
                        if index == len(packets):
                            index = len(packets) - 1
                            check = 1
                        break
                    mini = [-1, T + 100]
                    for k in range(len(least)):
                        if least[k][1] <= mini[1]:
                            mini = [least[k][0], least[k][1]]
                    need = mini[0]

                    start = processors_times[need][1]
                    wait += start - high_queue[0][0]
                    end = processors_times[need][1] + high_queue[0][1]
                    processors_times[need][0] = start
                    processors_times[need][1] = end
                    proc_use[need] += end - start
                    print(processors_times)
                    low_queue.popleft()
                    weight -= 1
                    if weight == 0:
                        weight = 10
                    print(high_queue)
                if len(low_queue) == 0 and 0 < weight <= 2:
                    least = list()
                    for j in range(PROCESSORS_NUM):
                        if time < processors_times[j][1]:
                            continue
                        else:
                            least.append((j, processors_times[j][1]))
                    if len(least) == 0:
                        low_queue.append(packet)
                        packet = packets[index]
                        index += 1
                        if index == len(packets):
                            index = len(packets) - 1
                            check = 1
                        continue
                    else:
                        mini = [-1, T + 100]
                        for k in range(len(least)):
                            if least[k][1] <= mini[1]:
                                mini = [least[k][0], least[k][1]]

                        need = mini[0]
                        start = packet[0]
                        end = packet[0] + packet[1]
                        processors_times[need] = [start, end]
                        proc_use[need] += end - start
                        packet = packets[index]
                        index += 1
                        if index == len(packets):
                            index = len(packets) - 1
                            check = 1
                elif len(low_queue) == 0 and weight > 2:
                    low_queue.append(packet)
                    packet = packets[index]
                    index += 1
                    if index == len(packets):
                        index = len(packets) - 1
                    break

            else:
                dropped += 1
                continue

        elif priority == "Low Priority" and weight > 2:
            if len(low_queue) <= LENGTH_LIMIT[2]:
                low_queue.append(packet)
                packet = packets[index]
                index += 1
                if index == len(packets):
                    index = len(packets) - 1
                    check = 1
                break
            else:
                dropped += 1
                continue
