import time
import os
# from typing import Dict, List
import csv
from operator import index

import pandas as pd
import keyboard

from typing import Dict

import lanconnection
import statistics
import statsmodels.api as sm
# from patsy import dmatrices
import statsmodels.formula.api as smf

import matplotlib.pyplot as plt

import keithley_util
from enum import Enum, auto



# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

class SipmType(Enum):
    MASTER = auto()
    SLAVE = auto()


epsilon = 0.000001
ip = '10.2.0.209'
port = 5555
bar_id = 12
time_interval = 60

a_master_set_AFE_12 = -260.002
b_master_set_AFE_12 = 16535.2

a_master_measured_AFE_12 = 0.0184174
b_master_measured_AFE_12 = -1.6745

a_slave_set_AFE_12 = -260.2817
b_slave_set_AFE_12 = 16626.31

a_slave_measured_AFE_12 = 0.0184290  # Tu chyba zamieniono współczynniki a z b - później poprawiono
b_slave_measured_AFE_12 = -1.591  # Tu chyba zamieniono współczynniki a z b - później poprawiono

a_master_set_AFE_12_new_measurement = -260.601
b_master_set_AFE_12_new_measurement = 16535.8

a_master_set_AFE_12_new_measurement2 = -259.6249
b_master_set_AFE_12_new_measurement2 = 16537.08

a_master_measured_AFE_12_new_measurement = 0.0184224
b_master_measured_AFE_12_new_measurement = -1.634

a_master_measured_AFE_12_new_measurement2 = 0.0184107
b_master_measured_AFE_12_new_measurement2 = -1.5966

a_slave_set_AFE_12_new_measurement = -259.840
b_slave_set_AFE_12_new_measurement = 16605.1

a_slave_set_AFE_12_new_measurement2 = -260.1
b_slave_set_AFE_12_new_measurement2 = 16429

a_slave_set_AFE_12_new_measurement3 = -259.975
b_slave_set_AFE_12_new_measurement3 = 16616.82

a_slave_measured_AFE_12_new_measurement = 0.0184600
b_slave_measured_AFE_12_new_measurement = -1.637

a_slave_measured_AFE_12_new_measurement2 = 0.018432
b_slave_measured_AFE_12_new_measurement2 = -2.29

a_slave_measured_AFE_12_new_measurement3 = 0.0184475
b_slave_measured_AFE_12_new_measurement3 = -1.5912

a_master_set_AFE_14 = -259.1475
b_master_set_AFE_14 = 16536.67

a_master_measured_AFE_14 = 0.0183954
b_master_measured_AFE_14 = -1.691

a_master_set_AFE_11 = -259.1845
b_master_set_AFE_11 = 16498.42

a_master_measured_AFE_11 = 0.018360
b_master_measured_AFE_11 = -1.664

a_master_set_AFE_10 = -258.1665
b_master_set_AFE_10 = 16509.26

a_master_measured_AFE_10 = 0.0185317
b_master_measured_AFE_10 = -1.644

a_slave_set_AFE_10 = -257.838
b_slave_set_AFE_10 = 16357.38

a_slave_measured_AFE_10 = 0.0184845
b_slave_measured_AFE_10 = -1.718

a_master_set_AFE_15 = -260.648
b_master_set_AFE_15 = 16553.25

a_master_measured_AFE_15 = 0.0184272
b_master_measured_AFE_15 = -1.666

a_master_set_AFE_32 = -259.848
b_master_set_AFE_32 = 16521.54

a_master_measured_AFE_32 = 0.0184781
b_master_measured_AFE_32 = -1.635

a_slave_set_AFE_32 = -259.6294
b_slave_set_AFE_32 = 16585.79

a_slave_measured_AFE_32 = 0.0184407
b_slave_measured_AFE_32 = -1.623

a_master_set_AFE_34 = -259.137
b_master_set_AFE_34 = 16439.47

a_master_measured_AFE_34 = 0.0184015
b_master_measured_AFE_34 = -1.705

a_slave_set_AFE_34 = -258.374
b_slave_set_AFE_34 = 16537.90

a_slave_measured_AFE_34 = 0.0183964
b_slave_measured_AFE_34 = -1.619

a_master_set_AFE_35 = -258.026
b_master_set_AFE_35 = 16462.59

a_master_measured_AFE_35 = 0.0184305
b_master_measured_AFE_35 = -1.682

a_slave_set_AFE_35 = -260.156
b_slave_set_AFE_35 = 16541.05

a_slave_measured_AFE_35 = 0.0184310
b_slave_measured_AFE_35 = -1.622

a_master_set_AFE_36 = -259.680
b_master_set_AFE_36 = 16606.33

a_master_measured_AFE_36 = 0.0183569
b_master_measured_AFE_36 = -1.775

a_slave_set_AFE_36 = -260.141
b_slave_set_AFE_36 = 16475.48

a_slave_measured_AFE_36 = 0.0184000
b_slave_measured_AFE_36 = -1.672

a_master_set_AFE_37 = -259.150
b_master_set_AFE_37 = 16491.67

a_master_measured_AFE_37 = 0.0185747
b_master_measured_AFE_37 = -1.640

a_slave_set_AFE_37 = -257.971
b_slave_set_AFE_37 = 16435.59

a_slave_measured_AFE_37 = 0.0185053
b_slave_measured_AFE_37 = -1.710

a_master_set_AFE_38 = -259.133
b_master_set_AFE_38 = 16462.61

a_master_measured_AFE_38 = 0.0183927
b_master_measured_AFE_38 = -1.686

a_slave_set_AFE_38 = -259.3731
b_slave_set_AFE_38 = 16452.52

a_slave_measured_AFE_38 = 0.0184203
b_slave_measured_AFE_38 = -1.683

a_master_set_AFE_39 = -259.354
b_master_set_AFE_39 = 16488.71

a_master_measured_AFE_39 = 0.0184947
b_master_measured_AFE_39 = -1.604

a_slave_set_AFE_39 = -259.7150
b_slave_set_AFE_39 = 16523.57

a_slave_measured_AFE_39 = 0.0184252
b_slave_measured_AFE_39 = -1.691

a_master_set_AFE_33 = -260.361
b_master_set_AFE_33 = 16459.86

a_master_measured_AFE_33 = 0.0184607
b_master_measured_AFE_33 = -1.809

a_slave_set_AFE_33 = -259.333
b_slave_set_AFE_33 = 16548.57

a_slave_measured_AFE_33 = 0.0183954
b_slave_measured_AFE_33 = -1.792

a_master_set_AFE_11_nowe = -259.123
b_master_set_AFE_11_nowe = 16537.65

a_master_measured_AFE_11_nowe = 0.0183569
b_master_measured_AFE_11_nowe = -1.775

a_slave_set_AFE_11_new = -258.8401
b_slave_set_AFE_11_new = 16427.83

a_slave_measured_AFE_11_new = 0.0184518
b_slave_measured_AFE_11_new = -1.909

a_master_set_AFE_14_new = -258.171
b_master_set_AFE_14_new = 16377.88

a_master_measured_AFE_14_new = 0.0184723
b_master_measured_AFE_14_new = -1.966

a_slave_set_AFE_14_new = -257.9886
b_slave_set_AFE_14_new = 16327.93

a_slave_measured_AFE_14_new = 0.0185965
b_slave_measured_AFE_14_new = -1.952

a_master_set_AFE_16_new = -260.751
b_master_set_AFE_16_new = 16480.84

a_master_measured_AFE_16_new = 0.01850040
b_master_measured_AFE_16_new = -1.767

a_slave_set_AFE_16_new = -258.6866
b_slave_set_AFE_16_new = 16526.47

a_slave_measured_AFE_16_new = 0.0183961
b_slave_measured_AFE_16_new = -1.713

a_master_set_AFE_15_new = -259.6153
b_master_set_AFE_15_new = 16416.93

a_master_measured_AFE_15_new = 0.0184353
b_master_measured_AFE_15_new = -1.668

a_slave_set_AFE_15_new = -260.037
b_slave_set_AFE_15_new = 16532.82

a_slave_measured_AFE_15_new = 0.0183981
b_slave_measured_AFE_15_new = -1.633

a_master_set_AFE_12_new = -259.283
b_master_set_AFE_12_new = 16596.25

a_master_measured_AFE_12_new = 0.0183460
b_master_measured_AFE_12_new = -1.563

a_slave_set_AFE_12_new = -261.318
b_slave_set_AFE_12_new = 16630.39

a_slave_measured_AFE_12_new = 0.0183945
b_slave_measured_AFE_12_new = -1.669

a_master_set_AFE_17_new = -259.020
b_master_set_AFE_17_new = 16471.26

a_master_measured_AFE_17_new = 0.0185293
b_master_measured_AFE_17_new = -1.688

a_slave_set_AFE_17_new = -259.521
b_slave_set_AFE_17_new = 16445.62

a_slave_measured_AFE_17_new = 0.0184359
b_slave_measured_AFE_17_new = -1.687

a_master_set_AFE_13_new = -258.557
b_master_set_AFE_13_new = 16431.29

a_master_measured_AFE_13_new = 0.0184654
b_master_measured_AFE_13_new = -1.776

a_slave_set_AFE_13_new = -259.796
b_slave_set_AFE_13_new = 16538.18

a_slave_measured_AFE_13_new = 0.0184515
b_slave_measured_AFE_13_new = -1.708

a_master_set_AFE_18_new = -260.261
b_master_set_AFE_18_new = 16618.88

a_master_measured_AFE_18_new = 0.01834383
b_master_measured_AFE_18_new = -1.524

a_slave_set_AFE_18_new = -259.8389
b_slave_set_AFE_18_new = 16599.77

a_slave_measured_AFE_18_new = 0.0183593
b_slave_measured_AFE_18_new = -1.572

a_master_set_AFE_12_again = -259.5404
b_master_set_AFE_12_again = 16535.50

a_master_measured_AFE_12_again = 0.0184202
b_master_measured_AFE_12_again = -1.603

# a_master_set_AFE_0 = -258.8401 #pomylka - dane spisane nie z tego pliku, co trzeba z AFE 11 new slave
# b_master_set_AFE_0 = 16427.83
#
# a_master_measured_AFE_0 = 0.0184518
# b_master_measured_AFE_0 = -1.909

a_master_set_AFE_0 = -260.194
b_master_set_AFE_0 = 16578.43

a_master_measured_AFE_0 = 0.0184417
b_master_measured_AFE_0 = -1.656

a_slave_set_AFE_0 = -260.148
b_slave_set_AFE_0 = 16570.76

a_slave_measured_AFE_0 = 0.0183922
b_slave_measured_AFE_0 = -1.590

a_master_set_AFE_1 = -260.402
b_master_set_AFE_1 = 16593.85

a_master_measured_AFE_1 = 0.0182541
b_master_measured_AFE_1 = -1.577

a_slave_set_AFE_1 = -258.732
b_slave_set_AFE_1 = 16621.75

a_slave_measured_AFE_1 = 0.0184320
b_slave_measured_AFE_1 = -1.628

a_master_set_AFE_22_without_capacitors = -258.9043
b_master_set_AFE_22_without_capacitors = 16507.21

a_master_measured_AFE_22_without_capacitors = 0.0185088
b_master_measured_AFE_22_without_capacitors = -1.7196

a_slave_set_AFE_22_without_capacitors = -258.573
b_slave_set_AFE_22_without_capacitors = 16434.77

a_slave_measured_AFE_22_without_capacitors = 0.0184794
b_slave_measured_AFE_22_without_capacitors = -1.7886

resistance = 10.48 * 10 ** 6


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


def set_bit_voltage(voltage_bit: float, connection: lanconnection.LanConnection) \
        -> str:
    result = connection.do_cmd(['setrawdac', bar_id, voltage_bit, voltage_bit])
    return result[0]

def set_bit_voltage2(voltage_bit_master: float, voltage_bit_slave: float, connection: lanconnection.LanConnection) -> str:
    result = connection.do_cmd(['setrawdac', bar_id, voltage_bit_master, voltage_bit_slave])
    return result[0]

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
# def measure_AFE_voltage(voltage: float, connection: lanconnection.LanConnection, step_time: float)\
#         -> (float, int, int, float, int, int):
#     result = connection.do_cmd(['setdac', bar_id, voltage, voltage])
#     set_master = None
#     set_slave = None
#     if result[0] == 'ERR':
#         print('Error when setdac')
#     else:
#         set_master = result[1][0]
#         set_slave = result[1][1]
#     time.sleep(step_time)
#     measured_master = connection.do_cmd(['adc', bar_id, 3])[1]
#     measured_slave = connection.do_cmd(['adc', bar_id, 4])[1]
#     return voltage, set_master, measured_master, voltage, set_slave, measured_slave


def measure_AFE_voltage_master(connection: lanconnection.LanConnection):
    return connection.do_cmd(['adc', bar_id, 3])[1]


def measure_AFE_voltage_slave(connection: lanconnection.LanConnection):
    return connection.do_cmd(['adc', bar_id, 4])[1]


def measure_AFE_all(connection: lanconnection.LanConnection) -> (int, int, int, int, int, int):
    measured_master_voltage = connection.do_cmd(['adc', bar_id, 3])[1]
    measured_slave_voltage = connection.do_cmd(['adc', bar_id, 4])[1]
    measured_master_current = connection.do_cmd(['adc', bar_id, 5])[1]
    measured_slave_current = connection.do_cmd(['adc', bar_id, 6])[1]
    return measured_master_voltage, measured_slave_voltage, measured_master_current, measured_slave_current


def measure_AFE_temp(connection: lanconnection.LanConnection) -> (int, int):
    return connection.do_cmd(['gettemp', bar_id])[1]


def measure_AFE_temp_avg_master(avg_number: int, connection: lanconnection.LanConnection) -> (float, float):
    number = 0
    measured_master_temp_list = []
    while number < avg_number:
        measured_master_temp_list.append(connection.do_cmd(['gettemp', bar_id])[1][0])
        number += 1
    return statistics.mean(measured_master_temp_list), statistics.stdev(measured_master_temp_list)


def measure_AFE_temp_avg_slave(avg_number: int, connection: lanconnection.LanConnection) -> (float, float):
    number = 0
    measured_master_temp_list = []
    while number < avg_number:
        measured_master_temp_list.append(connection.do_cmd(['gettemp', bar_id])[1][1])
        number += 1
    return statistics.mean(measured_master_temp_list), statistics.stdev(measured_master_temp_list)


def stability(end_date: float, step: float, step_keithley: float, set_voltage: float, waiting_time: float,
              file_name: str):
    connection = lanconnection.LanConnection(ip, port)
    try:
        result = connection.do_cmd(['init', bar_id])
        if result[0] == 'ERR':
            print("Error when init")
        print("init OK")

        result = connection.do_cmd(['hvon', bar_id])
        if result[0] == 'ERR':
            print("Error when hvon")
        print("hvon OK")

        if os.path.exists(file_name):
            raise Exception("File already exists!")

        _headers = ('date UTC since epoch [s]', 'date from Keithley', 'Voltage AFE U[V]', 'Voltage AFE U[bit]',
                    'Voltage Keithley [V]', 'master measured voltage U[bit]', 'slave measured voltage U[bit]',
                    'master measured current U[bit]', 'slave measured current U[bit]')

        with open(file_name, mode='w', newline='') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=_headers)
            writer.writeheader()
            current_time = time.time()
            print(current_time)
            voltage_result = connection.do_cmd(['setdac', bar_id, set_voltage, set_voltage])
            time.sleep(waiting_time)
            print(voltage_result)
            keithley = keithley_util.Keithley6517()
            while current_time < end_date:
                measure_dict = {}
                time.sleep(step)
                result = measure_AFE_all(connection)
                result_keithley = keithley.measure()
                r_num = result_keithley['rNum']
                while result_keithley['rNum'] == r_num:
                    r_num = result_keithley['rNum']
                    time.sleep(step_keithley)
                    result_keithley = keithley.measure()

                current_time = time.time()
                measure_dict[_headers[0]] = current_time
                measure_dict[_headers[1]] = result_keithley['date'] + ' ' + result_keithley['time']
                measure_dict[_headers[2]] = set_voltage
                measure_dict[_headers[3]] = voltage_result[1][0]
                measure_dict[_headers[4]] = result_keithley['voltage']
                measure_dict[_headers[5]] = result[0]
                measure_dict[_headers[6]] = result[1]
                measure_dict[_headers[7]] = result[2]
                measure_dict[_headers[8]] = result[3]
                writer.writerow(measure_dict)
                print(current_time)

        result = connection.do_cmd(['hvoff', bar_id])
        if result[0] == 'ERR':
            print("Error when hvoff")
        connection.close_connection()

    except Exception as exc:
        result = connection.do_cmd(['hvoff', bar_id])
        if result[0] == 'ERR':
            print("Error when hvoff")
        connection.close_connection()
        print(exc)


def stability2_slave(a_slave_measured: float, b_slave_measured: float, set_voltage: float, waiting_sec: int, step_keithley: float,
              file_name: str):
    connection = lanconnection.LanConnection(ip, port)
    try:
        result = connection.do_cmd(['init', bar_id])
        if result[0] == 'ERR':
            print("Error when init")
        print("init OK")

        result = connection.do_cmd(['hvon', bar_id])
        if result[0] == 'ERR':
            print("Error when hvon")
        print("hvon OK")

        if os.path.exists(file_name):
            raise Exception("File already exists!")

        _headers = ('cycle no', 'time keithley', 'computer time begin', 'computer time AFE end', 'Voltage set AFE U[V]', 'Voltage set AFE U[bit]',
                    'Voltage Keithley [V]', 'slave AFE measured voltage U[bit]', 'slave AFE measured voltage U[V]')

        with open(file_name, mode='w', newline='') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=_headers)
            writer.writeheader()
            start_time = time.time()
            voltage_result = connection.do_cmd(['setdac', bar_id, set_voltage, set_voltage])
            print(print("Start time:", time.ctime(start_time)))
            print(voltage_result)
            keithley = keithley_util.Keithley6517()
            cycl_no = 0
            while not keyboard.is_pressed("q"):
                measure_dict = {}
                current_time_start = time.time()
                result = measure_AFE_voltage_slave(connection)
                result_keithley = keithley.measure()
                r_num = result_keithley['rNum']
                while result_keithley['rNum'] == r_num:
                    r_num = result_keithley['rNum']
                    time.sleep(step_keithley)
                    result_keithley = keithley.measure()

                current_time_end = time.time()
                measure_dict[_headers[0]] = cycl_no
                measure_dict[_headers[1]] = result_keithley['date'] + ' ' + result_keithley['time']
                measure_dict[_headers[2]] = current_time_start
                measure_dict[_headers[3]] = current_time_end
                measure_dict[_headers[4]] = set_voltage
                measure_dict[_headers[5]] = voltage_result[1][1]
                measure_dict[_headers[6]] = result_keithley['voltage']
                measure_dict[_headers[7]] = result
                measure_dict[_headers[8]] = a_slave_measured * measure_AFE_voltage_slave(connection) + b_slave_measured

                writer.writerow(measure_dict)
                time.sleep(waiting_sec - (current_time_end - current_time_start))
                print(result_keithley['time'])
                cycl_no = cycl_no + 1

        result = connection.do_cmd(['hvoff', bar_id])
        if result[0] == 'ERR':
            print("Error when hvoff")
        connection.close_connection()

    except Exception as exc:
        result = connection.do_cmd(['hvoff', bar_id])
        if result[0] == 'ERR':
            print("Error when hvoff")
        connection.close_connection()
        print(exc)


def stability2_slave_many_voltage(a_slave_measured: float, b_slave_measured: float,
                                  set_voltage1: float, delta_time1: float, set_voltage2: float, delta_time2:float,
                                  set_voltage3: float, delta_time3: float,
                                  waiting_sec: int, step_keithley: float,
                                  file_name: str):
    connection = lanconnection.LanConnection(ip, port)
    try:
        result = connection.do_cmd(['init', bar_id])
        if result[0] == 'ERR':
            print("Error when init")
        print("init OK")

        result = connection.do_cmd(['hvon', bar_id])
        if result[0] == 'ERR':
            print("Error when hvon")
        print("hvon OK")

        if os.path.exists(file_name):
            raise Exception("File already exists!")

        _headers = ('cycle no', 'time keithley', 'computer time begin', 'computer time AFE end', 'Voltage set AFE U[V]', 'Voltage set AFE U[bit]',
                    'Voltage Keithley [V]', 'slave AFE measured voltage U[bit]', 'slave AFE measured voltage U[V]')

        with open(file_name, mode='w', newline='') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=_headers)
            writer.writeheader()
            start_time = time.time()
            print(print("Start time:", time.ctime(start_time)))
            keithley = keithley_util.Keithley6517()
            cycl_no = 0
            current_delta_time = 0
            voltage_result1 = connection.do_cmd(['setdac', bar_id, set_voltage1, set_voltage1])
            print(voltage_result1)
            while current_delta_time < delta_time1:
                measure_dict = {}
                current_time_start = time.time()
                result = measure_AFE_voltage_slave(connection)
                result_keithley = keithley.measure()
                r_num = result_keithley['rNum']
                while result_keithley['rNum'] == r_num:
                    r_num = result_keithley['rNum']
                    time.sleep(step_keithley)
                    result_keithley = keithley.measure()

                current_time_end = time.time()
                measure_dict[_headers[0]] = cycl_no
                measure_dict[_headers[1]] = result_keithley['date'] + ' ' + result_keithley['time']
                measure_dict[_headers[2]] = current_time_start
                measure_dict[_headers[3]] = current_time_end
                measure_dict[_headers[4]] = set_voltage1
                measure_dict[_headers[5]] = voltage_result1[1][1]
                measure_dict[_headers[6]] = result_keithley['voltage']
                measure_dict[_headers[7]] = result
                measure_dict[_headers[8]] = a_slave_measured * measure_AFE_voltage_slave(connection) + b_slave_measured

                writer.writerow(measure_dict)
                time.sleep(waiting_sec - (current_time_end - current_time_start))
                print(result_keithley['time'])
                cycl_no = cycl_no + 1
                current_delta_time += (time.time() - current_time_start)

            current_delta_time = 0
            voltage_result2 = connection.do_cmd(['setdac', bar_id, set_voltage2, set_voltage2])
            print(voltage_result2)
            while current_delta_time < delta_time2:
                measure_dict = {}
                current_time_start = time.time()
                result = measure_AFE_voltage_slave(connection)
                result_keithley = keithley.measure()
                r_num = result_keithley['rNum']
                while result_keithley['rNum'] == r_num:
                    r_num = result_keithley['rNum']
                    time.sleep(step_keithley)
                    result_keithley = keithley.measure()

                current_time_end = time.time()
                measure_dict[_headers[0]] = cycl_no
                measure_dict[_headers[1]] = result_keithley['date'] + ' ' + result_keithley['time']
                measure_dict[_headers[2]] = current_time_start
                measure_dict[_headers[3]] = current_time_end
                measure_dict[_headers[4]] = set_voltage2
                measure_dict[_headers[5]] = voltage_result2[1][1]
                measure_dict[_headers[6]] = result_keithley['voltage']
                measure_dict[_headers[7]] = result
                measure_dict[_headers[8]] = a_slave_measured * measure_AFE_voltage_slave(connection) + b_slave_measured

                writer.writerow(measure_dict)
                time.sleep(waiting_sec - (current_time_end - current_time_start))
                print(result_keithley['time'])
                cycl_no = cycl_no + 1
                current_delta_time += (time.time() - current_time_start)

            current_delta_time = 0
            voltage_result3 = connection.do_cmd(['setdac', bar_id, set_voltage3, set_voltage3])
            print(voltage_result3)
            while current_delta_time < delta_time3:
                measure_dict = {}
                current_time_start = time.time()
                result = measure_AFE_voltage_slave(connection)
                result_keithley = keithley.measure()
                r_num = result_keithley['rNum']
                while result_keithley['rNum'] == r_num:
                    r_num = result_keithley['rNum']
                    time.sleep(step_keithley)
                    result_keithley = keithley.measure()

                current_time_end = time.time()
                measure_dict[_headers[0]] = cycl_no
                measure_dict[_headers[1]] = result_keithley['date'] + ' ' + result_keithley['time']
                measure_dict[_headers[2]] = current_time_start
                measure_dict[_headers[3]] = current_time_end
                measure_dict[_headers[4]] = set_voltage3
                measure_dict[_headers[5]] = voltage_result3[1][1]
                measure_dict[_headers[6]] = result_keithley['voltage']
                measure_dict[_headers[7]] = result
                measure_dict[_headers[8]] = a_slave_measured * measure_AFE_voltage_slave(connection) + b_slave_measured

                writer.writerow(measure_dict)
                time.sleep(waiting_sec - (current_time_end - current_time_start))
                print(result_keithley['time'])
                cycl_no = cycl_no + 1
                current_delta_time += (time.time() - current_time_start)

        result = connection.do_cmd(['hvoff', bar_id])
        if result[0] == 'ERR':
            print("Error when hvoff")
        connection.close_connection()

    except Exception as exc:
        result = connection.do_cmd(['hvoff', bar_id])
        if result[0] == 'ERR':
            print("Error when hvoff")
        connection.close_connection()
        print(exc)


def stability_temp(end_date: float, step: float, step_keithley: float, set_voltage: float, waiting_time: float,
                   file_name: str):
    connection = lanconnection.LanConnection(ip, port)
    try:
        result = connection.do_cmd(['init', bar_id])
        if result[0] == 'ERR':
            print("Error when init")
        print("init OK")

        result = connection.do_cmd(['hvon', bar_id])
        if result[0] == 'ERR':
            print("Error when hvon")
        print("hvon OK")

        if os.path.exists(file_name):
            raise Exception("File already exists!")

        _headers = ('date UTC since epoch [s]', 'date from Keithley', 'Voltage AFE U[V]',
                    'Temperature SiPM master [bit]', 'Temperature SiPM slave [bit]',
                    'Temperature keithley [centigrade]')

        with open(file_name, mode='w', newline='') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=_headers)
            writer.writeheader()
            time.sleep(waiting_time)
            current_time = time.time()
            print(current_time)
            voltage_result = connection.do_cmd(['setdac', bar_id, set_voltage, set_voltage])
            print(voltage_result)
            keithley = keithley_util.Keithley6517()
            while current_time < end_date:
                measure_dict = {}
                time.sleep(step)
                result = measure_AFE_temp(connection)
                result_keithley = keithley.measure()
                r_num = result_keithley['rNum']
                while result_keithley['rNum'] == r_num:
                    r_num = result_keithley['rNum']
                    time.sleep(step_keithley)
                    result_keithley = keithley.measure()

                current_time = time.time()
                measure_dict[_headers[0]] = current_time
                measure_dict[_headers[1]] = result_keithley['date'] + ' ' + result_keithley['time']
                measure_dict[_headers[2]] = set_voltage
                measure_dict[_headers[3]] = result[0]
                measure_dict[_headers[4]] = result[1]
                measure_dict[_headers[5]] = result_keithley['temp']

                writer.writerow(measure_dict)
                print(current_time)

        result = connection.do_cmd(['hvoff', bar_id])
        if result[0] == 'ERR':
            print("Error when hvoff")
        connection.close_connection()

    except Exception as exc:
        result = connection.do_cmd(['hvoff', bar_id])
        if result[0] == 'ERR':
            print("Error when hvoff")
        connection.close_connection()
        print(exc)


def stability_temp2(end_date: float, step: float, step_keithley: float, set_voltage: float, waiting_time: float,
                    file_name: str):
    connection = lanconnection.LanConnection(ip, port)
    try:
        result = connection.do_cmd(['init', bar_id])
        if result[0] == 'ERR':
            print("Error when init")
        else:
            print("init OK")

        result = connection.do_cmd(['hvoff', bar_id])
        if result[0] == 'ERR':
            print("Error when hvoff")
        else:
            print("hvoff OK")

        if os.path.exists(file_name):
            raise Exception("File already exists!")

        _headers = ('date UTC since epoch [s]', 'date from Keithley', 'Voltage AFE U[V]',
                    'Temperature SiPM master [bit]', 'Temperature SiPM slave [bit]',
                    'Temperature keithley [centigrade]')

        with open(file_name, mode='w', newline='') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=_headers)
            writer.writeheader()
            time.sleep(waiting_time)
            current_time = time.time()
            print(current_time)
            voltage_result = connection.do_cmd(['setdac', bar_id, set_voltage, set_voltage])
            print(voltage_result)
            keithley = keithley_util.Keithley6517()
            while current_time < end_date:
                measure_dict = {}
                time.sleep(step)
                result = measure_AFE_temp(connection)
                result_keithley = keithley.measure()
                r_num = result_keithley['rNum']
                while result_keithley['rNum'] == r_num:
                    r_num = result_keithley['rNum']
                    time.sleep(step_keithley)
                    result_keithley = keithley.measure()

                current_time = time.time()
                measure_dict[_headers[0]] = current_time
                measure_dict[_headers[1]] = result_keithley['date'] + ' ' + result_keithley['time']
                measure_dict[_headers[2]] = set_voltage
                measure_dict[_headers[3]] = result[0]
                measure_dict[_headers[4]] = result[1]
                measure_dict[_headers[5]] = result_keithley['temp']

                writer.writerow(measure_dict)
                print(current_time)

        result = connection.do_cmd(['hvoff', bar_id])
        if result[0] == 'ERR':
            print("Error when hvoff")
        connection.close_connection()

    except Exception as exc:
        result = connection.do_cmd(['hvoff', bar_id])
        if result[0] == 'ERR':
            print("Error when hvoff")
        connection.close_connection()
        print(exc)


def stability_temp_keithley(end_date: float, step: float, step_keithley: float, file_name: str):
    try:
        _headers = ('date UTC since epoch [s]', 'date from Keithley',
                    'Temperature keithley [centigrade]')

        with open(file_name, mode='w', newline='') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=_headers)
            writer.writeheader()
            current_time = time.time()
            keithley = keithley_util.Keithley6517()
            result_keithley = keithley.measure()
            print(result_keithley['time'])

            while current_time < end_date:
                measure_dict = {}
                time.sleep(step)
                result_keithley = keithley.measure()
                r_num = result_keithley['rNum']
                while result_keithley['rNum'] == r_num:
                    r_num = result_keithley['rNum']
                    time.sleep(step_keithley)
                    result_keithley = keithley.measure()
                current_time = time.time()
                measure_dict[_headers[0]] = current_time
                measure_dict[_headers[1]] = result_keithley['date'] + ' ' + result_keithley['time']
                measure_dict[_headers[2]] = result_keithley['temp']

                writer.writerow(measure_dict)
                print(result_keithley['time'])
                print(result_keithley['temp'])

    except Exception as exc:
        print(exc)


def stability_only_AFE_temp(end_date: float, waiting_time: float, file_name: str):
    connection = lanconnection.LanConnection(ip, port)
    try:
        result = connection.do_cmd(['init', bar_id])
        if result[0] == 'ERR':
            print("Error when init")
        else:
            print("init OK")

        result = connection.do_cmd(['hvoff', bar_id])

        if result[0] == 'ERR':
            print("Error when hvoff")
        else:
            print("hvoff OK")

        if os.path.exists(file_name):
            raise Exception("File already exists!")

        _headers = ('date UTC since epoch [s]', 'Temperature SiPM master [bit]', 'Temperature SiPM slave [bit]')

        with open(file_name, mode='w', newline='') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=_headers)
            writer.writeheader()
            time.sleep(waiting_time)
            current_time = time.time()
            print(current_time)

            while current_time < end_date:
                measure_dict = {}
                result = measure_AFE_temp(connection)

                current_time = time.time()
                measure_dict[_headers[0]] = current_time
                measure_dict[_headers[1]] = result[0]
                measure_dict[_headers[2]] = result[1]
                writer.writerow(measure_dict)
                print(current_time)

            result = connection.do_cmd(['hvoff', bar_id])
            if result[0] == 'ERR':
                print("Error when hvoff")
            connection.close_connection()

    except Exception as exc:
        result = connection.do_cmd(['hvoff', bar_id])
        if result[0] == 'ERR':
            print("Error when hvoff")
        connection.close_connection()
        print(exc)


def stability_only_AFE_temp_on(end_date: float, waiting_time: float, file_name: str):
    connection = lanconnection.LanConnection(ip, port)
    try:
        result = connection.do_cmd(['init', bar_id])
        if result[0] == 'ERR':
            print("Error when init")
        else:
            print("init OK")

        result = connection.do_cmd(['hvon', bar_id])
        if result[0] == 'ERR':
            print("Error when hvon")
        else:
            print("hvon OK")

        if os.path.exists(file_name):
            raise Exception("File already exists!")

        _headers = ('date UTC since epoch [s]', 'Temperature SiPM master [bit]', 'Temperature SiPM slave [bit]')

        with open(file_name, mode='w', newline='') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=_headers)
            writer.writeheader()
            time.sleep(waiting_time)
            current_time = time.time()
            print(current_time)

            while current_time < end_date:
                measure_dict = {}
                result = measure_AFE_temp(connection)

                current_time = time.time()
                measure_dict[_headers[0]] = current_time
                measure_dict[_headers[1]] = result[0]
                measure_dict[_headers[2]] = result[1]
                writer.writerow(measure_dict)
                print(current_time)

            result = connection.do_cmd(['hvoff', bar_id])
            if result[0] == 'ERR':
                print("Error when hvoff")
            connection.close_connection()

    except Exception as exc:
        result = connection.do_cmd(['hvoff', bar_id])
        if result[0] == 'ERR':
            print("Error when hvoff")
        connection.close_connection()
        print(exc)


def measure_avg_current(avg_number: int, sipm_type: SipmType, connection: lanconnection.LanConnection) -> float:
    number = 0
    sum = 0
    while number < avg_number:
        if sipm_type == SipmType.MASTER:
            measured_current = connection.do_cmd(['adc', bar_id, 5])[1]
        else:
            measured_current = connection.do_cmd(['adc', bar_id, 6])[1]
        sum += measured_current
        number += 1
    return sum / number

def measure_avg_current2(avg_number: int, sipm_type: SipmType, connection: lanconnection.LanConnection) -> (float, float):
    number = 0
    measured_current_list = []
    while number < avg_number:
        if sipm_type == SipmType.MASTER:
            measured_current = connection.do_cmd(['adc', bar_id, 5])[1]
        else:
            measured_current = connection.do_cmd(['adc', bar_id, 6])[1]
        measured_current_list.append(measured_current)
        number += 1
    return statistics.mean(measured_current_list), statistics.stdev(measured_current_list)

def measure_avg_current2_time(avg_number: int, sipm_type: SipmType, connection: lanconnection.LanConnection) -> (float, float):
    number = 0
    measured_current_list = []
    t1_start = time.time()
    while number < avg_number:
        if sipm_type == SipmType.MASTER:
            measured_current = connection.do_cmd(['adc', bar_id, 5])[1]
        else:
            measured_current = connection.do_cmd(['adc', bar_id, 6])[1]
        measured_current_list.append(measured_current)
        number += 1
    t1_stop = time.time()
    print("Elapsed time during the current measurment in seconds: ", t1_stop - t1_start)
    return statistics.mean(measured_current_list), statistics.stdev(measured_current_list)

def measure_avg_current2_bar_id(avg_number: int, sipm_type: SipmType, bar_id: int, connection: lanconnection.LanConnection) -> (float, float):
    number = 0
    measured_current_list = []
    while number < avg_number:
        if sipm_type == SipmType.MASTER:
            measured_current = connection.do_cmd(['adc', bar_id, 5])[1]
        else:
            measured_current = connection.do_cmd(['adc', bar_id, 6])[1]
        measured_current_list.append(measured_current)
        number += 1
    return statistics.mean(measured_current_list), statistics.stdev(measured_current_list)

def measure_avg_current3(avg_number: int, sipm_type: SipmType, connection: lanconnection.LanConnection) -> (
float, float):
    number = 0
    measured_current_list = []
    while number < avg_number:
        if sipm_type == SipmType.MASTER:
            measured_current = connection.do_cmd(['adc', bar_id, 5])[1]
        else:
            measured_current = connection.do_cmd(['adc', bar_id, 6])[1]
        measured_current_list.append(measured_current)
        number += 1
    return measured_current_list, statistics.mean(measured_current_list), statistics.stdev(measured_current_list)


def current_calibration_SiPM_master(a_master_set: float, b_master_set: float, a_master_measured: float,
                                    b_master_measured: float, waiting_time: float, start_voltage: float,
                                    stop_voltage: float, step: float, avg_number: int, step_time: float,
                                    file_name: str):
    if os.path.exists(file_name):
        raise Exception("File already exists!")

    with open(file_name, mode='w', newline='') as csv_file:
        try:
            connection = lanconnection.LanConnection(ip, port)

            result = connection.do_cmd(['init', bar_id])
            if result[0] == 'ERR':
                print("Error when init")
                raise ConnectionError(f"Unable to get connection to bar #{bar_id}")

            result = connection.do_cmd(['hvon', bar_id])
            if result[0] == 'ERR':
                print("Error when hvon")
                raise ConnectionError(f"Unable to get connection to bar #{bar_id}")
            voltage = start_voltage
            voltage_bit = int(a_master_set * start_voltage + b_master_set)
            _headers_master = ('master set U[V]', 'master measured U[V]', 'calculated master set amperage',
                               'calculated master measured amperage', 'master current measured I[bit]')
            # _headers_slave = ('slave set U[V]', 'master measured U[V]', 'calculated master set amperage', 'calculated master measured amperage', 'master current measured I[bit]')
            writer = csv.DictWriter(csv_file, fieldnames=_headers_master)
            writer.writeheader()
            time.sleep(waiting_time)

            while voltage < stop_voltage:
                print(voltage)
                set_bit_voltage(voltage_bit, connection)
                time.sleep(step_time)
                measured_voltage = a_master_measured * measure_AFE_voltage_master(connection) + b_master_measured

                measure_dict = {_headers_master[0]: voltage,
                                _headers_master[1]: measured_voltage,
                                _headers_master[2]: voltage / resistance,
                                _headers_master[3]: measured_voltage / resistance,
                                _headers_master[4]: measure_avg_current(avg_number, SipmType.MASTER, connection)}

                writer.writerow(measure_dict)
                voltage += step
                voltage_bit = int(a_master_set * voltage + b_master_set)

        except Exception as exc:
            result = connection.do_cmd(['hvoff', bar_id])
            if result[0] == 'ERR':
                print("Error when hvoff")
            connection.close_connection()
            print(exc)

        finally:
            result = connection.do_cmd(['hvoff', bar_id])
            if result[0] == 'ERR':
                print("Error when hvoff")
            connection.close_connection()


def current_voltage_dependence_master(a_master_set: float, b_master_set: float, a_master_measured: float,
                                      b_master_measured: float, waiting_time: float, start_voltage: float,
                                      stop_voltage: float, step: float, avg_number: int, step_time: float,
                                      file_name: str):
    if os.path.exists(file_name):
        raise Exception("File already exists!")

    with open(file_name, mode='w', newline='') as csv_file:
        try:
            connection = lanconnection.LanConnection(ip, port)
            keithley = keithley_util.Keithley6517()
            result = connection.do_cmd(['init', bar_id])
            if result[0] == 'ERR':
                print("Error when init")
                raise ConnectionError(f"Unable to get connection to bar #{bar_id}")

            result = connection.do_cmd(['hvon', bar_id])
            if result[0] == 'ERR':
                print("Error when hvon")
                raise ConnectionError(f"Unable to get connection to bar #{bar_id}")
            voltage = start_voltage
            voltage_bit = int(a_master_set * start_voltage + b_master_set)
            _headers_master = ('master set U[V]',
                               'master measured U[V]',
                               'master current measured I[bit]',
                               'master stddev measured current [bit]',
                               'number of measurements',
                               'Keithley temp [C]')
            writer = csv.DictWriter(csv_file, fieldnames=_headers_master)
            writer.writeheader()
            time.sleep(waiting_time)

            while voltage < stop_voltage:
                print(voltage)
                set_bit_voltage(voltage_bit, connection)
                time.sleep(step_time)
                measured_voltage = a_master_measured * measure_AFE_voltage_master(connection) + b_master_measured
                current, stddev_current = measure_avg_current2(avg_number, SipmType.MASTER, connection)

                result_keithley = keithley.measure()

                measure_dict = {
                    _headers_master[0]: voltage,
                    _headers_master[1]: measured_voltage,
                    _headers_master[2]: current,
                    _headers_master[3]: stddev_current,
                    _headers_master[4]: avg_number,
                    _headers_master[5]: result_keithley['temp']
                }

                writer.writerow(measure_dict)
                voltage += step
                voltage_bit = int(a_master_set * voltage + b_master_set)

        except Exception as exc:
            result = connection.do_cmd(['hvoff', bar_id])
            if result[0] == 'ERR':
                print("Error when hvoff")
            connection.close_connection()
            print(exc)

        # finally:
        #     result = connection.do_cmd(['hvoff', bar_id])
        #     if result[0] == 'ERR':
        #         print("Error when hvoff")
        #     connection.close_connection()


def current_voltage_dependence_slave(a_slave_set: float, b_slave_set: float, a_slave_measured: float,
                                     b_slave_measured: float, waiting_time: float, start_voltage: float,
                                     stop_voltage: float, step: float, avg_number: int, step_time: float,
                                     file_name: str):
    if os.path.exists(file_name):
        raise Exception("File already exists!")

    with open(file_name, mode='w', newline='') as csv_file:
        try:
            connection = lanconnection.LanConnection(ip, port)
            keithley = keithley_util.Keithley6517()
            result = connection.do_cmd(['init', bar_id])
            if result[0] == 'ERR':
                print("Error when init")
                raise ConnectionError(f"Unable to get connection to bar #{bar_id}")

            result = connection.do_cmd(['hvon', bar_id])
            if result[0] == 'ERR':
                print("Error when hvon")
                raise ConnectionError(f"Unable to get connection to bar #{bar_id}")
            voltage = start_voltage
            voltage_bit = int(a_slave_set * start_voltage + b_slave_set)
            _headers_master = ('slave set U[V]',
                               'slave measured U[V]',
                               'slave current measured I[bit]',
                               'slave stddev measured current [bit]',
                               'number of measurements',
                               'Keithley temp [C]')
            writer = csv.DictWriter(csv_file, fieldnames=_headers_master)
            writer.writeheader()
            time.sleep(waiting_time)

            while voltage < stop_voltage:
                print(voltage)
                set_bit_voltage(voltage_bit, connection)
                time.sleep(step_time)
                measured_voltage = a_slave_measured * measure_AFE_voltage_slave(connection) + b_slave_measured
                current, stddev_current = measure_avg_current2(avg_number, SipmType.SLAVE, connection)

                result_keithley = keithley.measure()

                measure_dict = {
                    _headers_master[0]: voltage,
                    _headers_master[1]: measured_voltage,
                    _headers_master[2]: current,
                    _headers_master[3]: stddev_current,
                    _headers_master[4]: avg_number,
                    _headers_master[5]: result_keithley['temp']
                }

                writer.writerow(measure_dict)
                voltage += step
                voltage_bit = int(a_slave_set * voltage + b_slave_set)

        except Exception as exc:
            result = connection.do_cmd(['hvoff', bar_id])
            if result[0] == 'ERR':
                print("Error when hvoff")
            connection.close_connection()
            print(exc)


results = Dict[str, float]


def current_voltage_dependence_multi_slabs(parameters_dict: Dict[int, results],
                                           waiting_time: float, start_voltage: float,
                                           stop_voltage: float, step: float, avg_number: int, step_time: float,
                                           file_name: str):
    if os.path.exists(file_name):
        raise Exception("File already exists!")

    with open(file_name, mode='w', newline='') as csv_file:
        try:
            connection = lanconnection.LanConnection(ip, port)
            _headers = ['set U[V]',
                        'number of measurements']
            voltage = start_voltage
            counter = 0
            voltage_bit_master = {}
            voltage_bit_slave = {}

            for bar_id, slab_parameters in parameters_dict.items():
                result = connection.do_cmd(['init', bar_id])
                if result[0] == 'ERR':
                    print("Error when init")
                    raise ConnectionError(f"Unable to get connection to bar #{bar_id}")

                result = connection.do_cmd(['hvon', bar_id])
                if result[0] == 'ERR':
                    print("Error when hvon")
                    raise ConnectionError(f"Unable to get connection to bar #{bar_id}")

                _headers.insert(counter * 6 + 1, f"master measured U[V] {bar_id}")
                _headers.insert(counter * 6 + 2, f"master measured current I[bit] {bar_id}")
                _headers.insert(counter * 6 + 3, f"master stddev measured current [bit] {bar_id}")
                _headers.insert(counter * 6 + 4, f"slave measured U[V] {bar_id}")
                _headers.insert(counter * 6 + 5, f"slave measured current I[bit] {bar_id}")
                _headers.insert(counter * 6 + 6, f"slave stddev measured current [bit] {bar_id}")

                voltage_bit_master[bar_id] = int(slab_parameters["set_master_a"] * start_voltage + slab_parameters["set_master_b"])
                voltage_bit_slave[bar_id] = int(slab_parameters["set_slave_a"] * start_voltage + slab_parameters["set_slave_b"])

                counter += 1

            writer = csv.DictWriter(csv_file, fieldnames=_headers)
            writer.writeheader()

            while waiting_time > 0:
                for bar_id, slab_parameters in parameters_dict.items():
                    result = connection.do_cmd(['adc', bar_id, 4])
                    if(result[0] == 'OK'):
                        print(f"Connected", end=" ")
                    else:
                        print("Connection error")
                        raise ConnectionError(f"Unable to get connection to bar #{bar_id}")
                print(f'left {waiting_time:5} seconds', end="")
                time.sleep(time_interval)
                print('\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b', end='')
                waiting_time = waiting_time - time_interval

            while voltage <= stop_voltage:
                print(voltage)

                counter = 0

                measure_dict = {
                    _headers[0]: voltage,
                    _headers[-1]: avg_number
                }

                for bar_id, slab_parameters in parameters_dict.items():
                    set_bit_voltage2(voltage_bit_master[bar_id], voltage_bit_slave[bar_id], connection)
                    time.sleep(step_time)
                    measured_voltage_master = slab_parameters["measured_master_a"] * measure_AFE_voltage_master(connection) \
                                              + slab_parameters["measured_master_b"]
                    measured_voltage_slave = slab_parameters["measured_slave_a"] * measure_AFE_voltage_slave(connection) \
                                             + slab_parameters["measured_slave_b"]

                    current_master, stddev_current_master = measure_avg_current2_bar_id(avg_number, SipmType.MASTER, bar_id, connection)
                    current_slave, stddev_current_slave = measure_avg_current2_bar_id(avg_number, SipmType.SLAVE, bar_id, connection)

                    measure_dict[_headers[counter * 6 + 1]] = measured_voltage_master
                    measure_dict[_headers[counter * 6 + 2]] = current_master
                    measure_dict[_headers[counter * 6 + 3]] = stddev_current_master
                    measure_dict[_headers[counter * 6 + 4]] = measured_voltage_slave
                    measure_dict[_headers[counter * 6 + 5]] = current_slave
                    measure_dict[_headers[counter * 6 + 6]] = stddev_current_slave

                    voltage_bit_master[bar_id] = int(slab_parameters["set_master_a"] * voltage + slab_parameters["set_master_b"])
                    voltage_bit_slave[bar_id] = int(slab_parameters["set_slave_a"] * voltage + slab_parameters["set_slave_b"])

                    counter += 1

                writer.writerow(measure_dict)
                voltage += step

            for bar_id, slab_parameters in parameters_dict.items():
                result = connection.do_cmd(['hvoff', bar_id])
                if result[0] == 'ERR':
                    print(f"Error when hvoff {bar_id}")
            connection.close_connection()

        except Exception as exc:
            for bar_id, slab_parameters in parameters_dict.items():
                result = connection.do_cmd(['hvoff', bar_id])
                if result[0] == 'ERR':
                    print(f"Error when hvoff {bar_id}")
            connection.close_connection()
            print(exc)

def current_voltage_dependence_slave2(a_slave_set: float, b_slave_set: float, a_slave_measured: float,
                                      b_slave_measured: float, waiting_time: float, start_voltage: float,
                                      stop_voltage: float, step: float, avg_number: int, step_time: float,
                                      file_name: str):
    if os.path.exists(file_name):
        raise Exception("File already exists!")

    with open(file_name, mode='w', newline='') as csv_file:
        try:
            connection = lanconnection.LanConnection(ip, port)
            keithley = keithley_util.Keithley6517()
            result = connection.do_cmd(['init', bar_id])
            if result[0] == 'ERR':
                print("Error when init")
                raise ConnectionError(f"Unable to get connection to bar #{bar_id}")

            result = connection.do_cmd(['hvon', bar_id])
            if result[0] == 'ERR':
                print("Error when hvon")
                raise ConnectionError(f"Unable to get connection to bar #{bar_id}")
            voltage = start_voltage
            voltage_bit = int(a_slave_set * start_voltage + b_slave_set)
            _headers_master = ('slave set U[V]',
                               'slave measured U[V]',
                               'slave current measured I[bit]',
                               'slave stddev measured current [bit]',
                               'number of measurements',
                               'Keithley temp [C]')
            writer = csv.DictWriter(csv_file, fieldnames=_headers_master)
            writer.writeheader()

            while waiting_time > 0:
                result = connection.do_cmd(['adc', bar_id, 4])
                if(result[0] == 'OK'):
                    print("Connected,", end=" ")
                else:
                    print("Connection error")
                    raise ConnectionError(f"Unable to get connection to bar #{bar_id}")
                print(f'left {waiting_time:5} seconds', end="")
                time.sleep(time_interval)
                print('\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b', end='')
                waiting_time = waiting_time - time_interval


            while voltage < stop_voltage:
                print(voltage)
                set_bit_voltage(voltage_bit, connection)
                time.sleep(step_time)
                measured_voltage = a_slave_measured * measure_AFE_voltage_slave(connection) + b_slave_measured
                current, stddev_current = measure_avg_current2(avg_number, SipmType.SLAVE, connection)

                result_keithley = keithley.measure()

                measure_dict = {
                    _headers_master[0]: voltage,
                    _headers_master[1]: measured_voltage,
                    _headers_master[2]: current,
                    _headers_master[3]: stddev_current,
                    _headers_master[4]: avg_number,
                    _headers_master[5]: result_keithley['temp']
                }

                writer.writerow(measure_dict)
                voltage += step
                voltage_bit = int(a_slave_set * voltage + b_slave_set)

            result = connection.do_cmd(['hvoff', bar_id])
            if result[0] == 'ERR':
                print("Error when hvoff")
            connection.close_connection()

        except Exception as exc:
            result = connection.do_cmd(['hvoff', bar_id])
            if result[0] == 'ERR':
                print("Error when hvoff")
            connection.close_connection()
            print(exc)


def current_voltage_dependence_slave2_without_Keithley(a_slave_set: float, b_slave_set: float, a_slave_measured: float,
                                      b_slave_measured: float, waiting_time: float, start_voltage: float,
                                      stop_voltage: float, step: float, avg_number: int, step_time: float,
                                      file_name: str):
    if os.path.exists(file_name):
        raise Exception("File already exists!")

    with open(file_name, mode='w', newline='') as csv_file:
        try:
            connection = lanconnection.LanConnection(ip, port)
            result = connection.do_cmd(['init', bar_id])
            if result[0] == 'ERR':
                print("Error when init")
                raise ConnectionError(f"Unable to get connection to bar #{bar_id}")

            result = connection.do_cmd(['hvon', bar_id])
            if result[0] == 'ERR':
                print("Error when hvon")
                raise ConnectionError(f"Unable to get connection to bar #{bar_id}")
            voltage = start_voltage
            voltage_bit = int(a_slave_set * start_voltage + b_slave_set)
            _headers_slave = ('slave set U[V]',
                              'slave measured U[V]',
                              'slave current measured I[bit]',
                              'slave stddev measured current [bit]',
                              'number of measurements')
            writer = csv.DictWriter(csv_file, fieldnames=_headers_slave)
            writer.writeheader()

            while waiting_time > 0:
                result = connection.do_cmd(['adc', bar_id, 4])
                if(result[0] == 'OK'):
                    print("Connected,", end=" ")
                else:
                    print("Connection error")
                    raise ConnectionError(f"Unable to get connection to bar #{bar_id}")
                print(f'left {waiting_time:5} seconds', end="")
                time.sleep(time_interval)
                print('\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b', end='')
                waiting_time = waiting_time - time_interval


            while voltage < stop_voltage:
                print(voltage)
                set_bit_voltage(voltage_bit, connection)
                time.sleep(step_time)
                measured_voltage = a_slave_measured * measure_AFE_voltage_slave(connection) + b_slave_measured
                current, stddev_current = measure_avg_current2(avg_number, SipmType.SLAVE, connection)

                measure_dict = {
                    _headers_slave[0]: voltage,
                    _headers_slave[1]: measured_voltage,
                    _headers_slave[2]: current,
                    _headers_slave[3]: stddev_current,
                    _headers_slave[4]: avg_number
                }

                writer.writerow(measure_dict)
                voltage += step
                voltage_bit = int(a_slave_set * voltage + b_slave_set)

            result = connection.do_cmd(['hvoff', bar_id])
            if result[0] == 'ERR':
                print("Error when hvoff")
            connection.close_connection()

        except Exception as exc:
            result = connection.do_cmd(['hvoff', bar_id])
            if result[0] == 'ERR':
                print("Error when hvoff")
            connection.close_connection()
            print(exc)


def current_voltage_dependence_slave2_without_Keithley_time(a_slave_set: float, b_slave_set: float, a_slave_measured: float,
                                      b_slave_measured: float, waiting_time: float, start_voltage: float,
                                      stop_voltage: float, step: float, avg_number: int, step_time: float,
                                      file_name: str):
    if os.path.exists(file_name):
        raise Exception("File already exists!")

    with open(file_name, mode='w', newline='') as csv_file:
        try:
            connection = lanconnection.LanConnection(ip, port)
            result = connection.do_cmd(['init', bar_id])
            if result[0] == 'ERR':
                print("Error when init")
                raise ConnectionError(f"Unable to get connection to bar #{bar_id}")

            result = connection.do_cmd(['hvon', bar_id])
            if result[0] == 'ERR':
                print("Error when hvon")
                raise ConnectionError(f"Unable to get connection to bar #{bar_id}")
            voltage = start_voltage
            voltage_bit = int(a_slave_set * start_voltage + b_slave_set)
            _headers_slave = ('slave set U[V]',
                              'slave measured U[V]',
                              'slave current measured I[bit]',
                              'slave stddev measured current [bit]',
                              'number of measurements')
            writer = csv.DictWriter(csv_file, fieldnames=_headers_slave)
            writer.writeheader()

            while waiting_time > 0:
                result = connection.do_cmd(['adc', bar_id, 4])
                if(result[0] == 'OK'):
                    print("Connected,", end=" ")
                else:
                    print("Connection error")
                    raise ConnectionError(f"Unable to get connection to bar #{bar_id}")
                print(f'left {waiting_time:5} seconds', end="")
                time.sleep(time_interval)
                print('\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b', end='')
                waiting_time = waiting_time - time_interval


            while voltage < stop_voltage:
                print(voltage)
                set_bit_voltage(voltage_bit, connection)
                time.sleep(step_time)
                measured_voltage = a_slave_measured * measure_AFE_voltage_slave(connection) + b_slave_measured
                current, stddev_current = measure_avg_current2_time(avg_number, SipmType.SLAVE, connection)

                measure_dict = {
                    _headers_slave[0]: voltage,
                    _headers_slave[1]: measured_voltage,
                    _headers_slave[2]: current,
                    _headers_slave[3]: stddev_current,
                    _headers_slave[4]: avg_number
                }

                writer.writerow(measure_dict)
                voltage += step
                voltage_bit = int(a_slave_set * voltage + b_slave_set)

            result = connection.do_cmd(['hvoff', bar_id])
            if result[0] == 'ERR':
                print("Error when hvoff")
            connection.close_connection()

        except Exception as exc:
            result = connection.do_cmd(['hvoff', bar_id])
            if result[0] == 'ERR':
                print("Error when hvoff")
            connection.close_connection()
            print(exc)

def current_voltage_dependence_master2_without_Keithley(a_master_set: float, b_master_set: float, a_master_measured: float,
                                      b_master_measured: float, waiting_time: float, start_voltage: float,
                                      stop_voltage: float, step: float, avg_number: int, step_time: float,
                                      file_name: str):
    if os.path.exists(file_name):
        raise Exception("File already exists!")

    with open(file_name, mode='w', newline='') as csv_file:
        try:
            connection = lanconnection.LanConnection(ip, port)
            result = connection.do_cmd(['init', bar_id])
            if result[0] == 'ERR':
                print("Error when init")
                raise ConnectionError(f"Unable to get connection to bar #{bar_id}")

            result = connection.do_cmd(['hvon', bar_id])
            if result[0] == 'ERR':
                print("Error when hvon")
                raise ConnectionError(f"Unable to get connection to bar #{bar_id}")
            voltage = start_voltage
            voltage_bit = int(a_master_set * start_voltage + b_master_set)
            _headers_master = ('master set U[V]',
                               'master measured U[V]',
                               'master current measured I[bit]',
                               'master stddev measured current [bit]',
                               'number of measurements')
            writer = csv.DictWriter(csv_file, fieldnames=_headers_master)
            writer.writeheader()

            while waiting_time > 0:
                result = connection.do_cmd(['adc', bar_id, 3])
                if(result[0] == 'OK'):
                    print("Connected,", end=" ")
                else:
                    print("Connection error")
                    raise ConnectionError(f"Unable to get connection to bar #{bar_id}")
                print(f'left {waiting_time:5} seconds', end="")
                time.sleep(time_interval)
                print('\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b', end='')
                waiting_time = waiting_time - time_interval


            while voltage < stop_voltage:
                print(voltage)
                set_bit_voltage(voltage_bit, connection)
                time.sleep(step_time)
                measured_voltage = a_master_measured * measure_AFE_voltage_master(connection) + b_master_measured
                current, stddev_current = measure_avg_current2(avg_number, SipmType.MASTER, connection)

                measure_dict = {
                    _headers_master[0]: voltage,
                    _headers_master[1]: measured_voltage,
                    _headers_master[2]: current,
                    _headers_master[3]: stddev_current,
                    _headers_master[4]: avg_number
                }

                writer.writerow(measure_dict)
                voltage += step
                voltage_bit = int(a_master_set * voltage + b_master_set)

            result = connection.do_cmd(['hvoff', bar_id])
            if result[0] == 'ERR':
                print("Error when hvoff")
            connection.close_connection()

        except Exception as exc:
            result = connection.do_cmd(['hvoff', bar_id])
            if result[0] == 'ERR':
                print("Error when hvoff")
            connection.close_connection()
            print(exc)


def current_calibration_SiPM_master2(a_master_set: float, b_master_set: float, a_master_measured: float,
                                     b_master_measured: float, waiting_time: float, start_voltage: float,
                                     stop_voltage: float, step: float, avg_number: int, step_time: float,
                                     file_name: str):
    if os.path.exists(file_name):
        raise Exception("File already exists!")

    with open(file_name, mode='w', newline='') as csv_file:
        try:
            connection = lanconnection.LanConnection(ip, port)

            result = connection.do_cmd(['init', bar_id])
            if result[0] == 'ERR':
                print("Error when init")
                raise ConnectionError(f"Unable to get connection to bar #{bar_id}")

            result = connection.do_cmd(['hvon', bar_id])
            if result[0] == 'ERR':
                print("Error when hvon")
                raise ConnectionError(f"Unable to get connection to bar #{bar_id}")
            voltage = start_voltage
            voltage_bit = int(a_master_set * start_voltage + b_master_set)
            _headers_master = ('master set U[V]', 'master measured U[V]', 'calculated master set amperage',
                               'calculated master measured amperage', 'master current measured I[bit]',
                               'master stddev measured current [bit]', 'number of measurements')
            # _headers_slave = ('slave set U[V]', 'master measured U[V]', 'calculated master set amperage', 'calculated master measured amperage', 'master current measured I[bit]')
            writer = csv.DictWriter(csv_file, fieldnames=_headers_master)
            writer.writeheader()
            time.sleep(waiting_time)

            while voltage <= stop_voltage:
                print(voltage)
                set_bit_voltage(voltage_bit, connection)
                time.sleep(step_time)
                measured_voltage = a_master_measured * measure_AFE_voltage_master(
                    connection) + b_master_measured
                current, stddev_current = measure_avg_current2(avg_number, SipmType.MASTER, connection)

                measure_dict = {_headers_master[0]: voltage,
                                _headers_master[1]: measured_voltage,
                                _headers_master[2]: voltage / resistance,
                                _headers_master[3]: measured_voltage / resistance,
                                _headers_master[4]: current,
                                _headers_master[5]: stddev_current,
                                _headers_master[6]: avg_number}

                writer.writerow(measure_dict)
                voltage += step
                voltage_bit = int(a_master_set * voltage + b_master_set)

        except Exception as exc:
            result = connection.do_cmd(['hvoff', bar_id])
            if result[0] == 'ERR':
                print("Error when hvoff")
            connection.close_connection()
            print(exc)

        finally:
            result = connection.do_cmd(['hvoff', bar_id])
        if result[0] == 'ERR':
            print("Error when hvoff")
        connection.close_connection()


def current_calibration_SiPM_master2all(a_master_set: float, b_master_set: float, a_master_measured: float,
                                        b_master_measured: float, waiting_time: float, start_voltage: float,
                                        stop_voltage: float, step: float, avg_number: int, step_time: float,
                                        file_name: str):
    if os.path.exists(file_name):
        raise Exception("File already exists!")

    with open(file_name + '_result.csv', mode='w', newline='') as csv_file_result:
        with open(file_name + '_raw.csv', mode='w', newline='') as csv_file_raw:
            try:
                connection = lanconnection.LanConnection(ip, port)

                result = connection.do_cmd(['init', bar_id])
                if result[0] == 'ERR':
                    print("Error when init")
                    raise ConnectionError(f"Unable to get connection to bar #{bar_id}")

                result = connection.do_cmd(['hvon', bar_id])
                if result[0] == 'ERR':
                    print("Error when hvon")
                    raise ConnectionError(f"Unable to get connection to bar #{bar_id}")
                voltage = start_voltage
                voltage_bit = int(a_master_set * start_voltage + b_master_set)
                _headers_master_result = ('master set U[V]',
                                          'master measured U[V]',
                                          'master avg measured current I[bit]',
                                          'master stddev measured current [bit]',
                                          'number of measurements')
                _headers_master_raw = ('master set U[V]',
                                       'master measured U[V]',
                                       'master measured current I[bit]'
                                       )
                writer_result = csv.DictWriter(csv_file_result, fieldnames=_headers_master_result)
                writer_raw = csv.DictWriter(csv_file_raw, fieldnames=_headers_master_raw)
                writer_result.writeheader()
                writer_raw.writeheader()
                time.sleep(waiting_time)

                while voltage <= stop_voltage:
                    print(voltage)
                    set_bit_voltage(voltage_bit, connection)
                    time.sleep(step_time)
                    measured_voltage = a_master_measured * measure_AFE_voltage_master(connection) + b_master_measured
                    current_list, avg_current, stddev_current = measure_avg_current3(avg_number, SipmType.MASTER,
                                                                                     connection)

                    measure_dict_result = {_headers_master_result[0]: voltage,
                                           _headers_master_result[1]: measured_voltage,
                                           _headers_master_result[2]: avg_current,
                                           _headers_master_result[3]: stddev_current,
                                           _headers_master_result[4]: avg_number}
                    for current in current_list:
                        measure_dict_raw = {_headers_master_raw[0]: voltage,
                                            _headers_master_raw[1]: measured_voltage,
                                            _headers_master_raw[2]: current}
                        writer_raw.writerow(measure_dict_raw)

                    writer_result.writerow(measure_dict_result)
                    voltage += step
                    voltage_bit = int(a_master_set * voltage + b_master_set)

            except Exception as exc:
                result = connection.do_cmd(['hvoff', bar_id])
                if result[0] == 'ERR':
                    print("Error when hvoff")
                connection.close_connection()
                print(exc)

            finally:
                result = connection.do_cmd(['hvoff', bar_id])
            if result[0] == 'ERR':
                print("Error when hvoff")
            connection.close_connection()


def current_calibration_SiPM_slave(a_slave_set: float, b_slave_set: float, a_slave_measured: float,
                                   b_slave_measured: float, waiting_time: float, start_voltage: float,
                                   stop_voltage: float, step: float, avg_number: int, step_time: float, file_name: str):
    if os.path.exists(file_name):
        raise Exception("File already exists!")
    with open(file_name, mode='w', newline='') as csv_file:
        try:
            connection = lanconnection.LanConnection(ip, port)

            result = connection.do_cmd(['init', bar_id])
            if result[0] == 'ERR':
                print("Error when init")
                raise ConnectionError(f"Unable to get connection to bar #{bar_id}")

            result = connection.do_cmd(['hvon', bar_id])
            if result[0] == 'ERR':
                print("Error when hvon")
                raise ConnectionError(f"Unable to get connection to bar #{bar_id}")
            voltage = start_voltage
            voltage_bit = int(a_slave_set * start_voltage + b_slave_set)

            _headers_slave = ('slave set U[V]', 'slave measured U[V]', 'calculated slave set amperage',
                              'calculated slave measured amperage', 'slave current measured I[bit]')
            writer = csv.DictWriter(csv_file, fieldnames=_headers_slave)
            writer.writeheader()
            time.sleep(waiting_time)

            while voltage < stop_voltage:
                print(voltage)
                set_bit_voltage(voltage_bit, connection)
                time.sleep(step_time)
                measured_voltage = a_slave_measured * measure_AFE_voltage_slave(connection) + b_slave_measured

                measure_dict = {_headers_slave[0]: voltage,
                                _headers_slave[1]: measured_voltage,
                                _headers_slave[2]: voltage / resistance,
                                _headers_slave[3]: measured_voltage / resistance,
                                _headers_slave[4]: measure_avg_current(avg_number, SipmType.SLAVE, connection)}

                writer.writerow(measure_dict)
                voltage += step
                voltage_bit = int(a_slave_set * voltage + b_slave_set)

        except Exception as exc:
            result = connection.do_cmd(['hvoff', bar_id])
            if result[0] == 'ERR':
                print("Error when hvoff")
            connection.close_connection()
            print(exc)

        finally:
            result = connection.do_cmd(['hvoff', bar_id])
            if result[0] == 'ERR':
                print("Error when hvoff")
            connection.close_connection()


def current_calibration_SiPM_slave2(a_slave_set: float, b_slave_set: float, a_slave_measured: float,
                                    b_slave_measured: float, waiting_time: float, start_voltage: float,
                                    stop_voltage: float, step: float, avg_number: int, step_time: float,
                                    file_name: str):
    if os.path.exists(file_name):
        raise Exception("File already exists!")
    with open(file_name, mode='w', newline='') as csv_file:
        try:
            connection = lanconnection.LanConnection(ip, port)

            result = connection.do_cmd(['init', bar_id])
            if result[0] == 'ERR':
                print("Error when init")
                raise ConnectionError(f"Unable to get connection to bar #{bar_id}")

            result = connection.do_cmd(['hvon', bar_id])
            if result[0] == 'ERR':
                print("Error when hvon")
                raise ConnectionError(f"Unable to get connection to bar #{bar_id}")
            voltage = start_voltage
            voltage_bit = int(a_slave_set * start_voltage + b_slave_set)

            _headers_slave = ('slave set U[V]', 'slave measured U[V]', 'calculated slave set amperage',
                              'calculated slave measured amperage', 'slave current measured I[bit]',
                              'stddev slave current measured I[bit]', 'number of measurements')
            writer = csv.DictWriter(csv_file, fieldnames=_headers_slave)
            writer.writeheader()
            time.sleep(waiting_time)

            while voltage < stop_voltage:
                print(voltage)
                set_bit_voltage(voltage_bit, connection)
                time.sleep(step_time)
                measured_voltage = a_slave_measured * measure_AFE_voltage_slave(connection) + b_slave_measured
                current, stddev_current = measure_avg_current2(avg_number, SipmType.SLAVE, connection)

                measure_dict = {_headers_slave[0]: voltage,
                                _headers_slave[1]: measured_voltage,
                                _headers_slave[2]: voltage / resistance,
                                _headers_slave[3]: measured_voltage / resistance,
                                _headers_slave[4]: current,
                                _headers_slave[5]: stddev_current,
                                _headers_slave[6]: avg_number}

                writer.writerow(measure_dict)
                voltage += step
                voltage_bit = int(a_slave_set * voltage + b_slave_set)

        except Exception as exc:
            result = connection.do_cmd(['hvoff', bar_id])
            if result[0] == 'ERR':
                print("Error when hvoff")
            connection.close_connection()
            print(exc)

        finally:
            result = connection.do_cmd(['hvoff', bar_id])
            if result[0] == 'ERR':
                print("Error when hvoff")
            connection.close_connection()


def current_calibration_SiPM_slave2all(a_slave_set: float, b_slave_set: float, a_slave_measured: float,
                                       b_slave_measured: float, waiting_time: float, start_voltage: float,
                                       stop_voltage: float, step: float, avg_number: int, step_time: float,
                                       file_name: str):
    if os.path.exists(file_name + '_result.csv'):
        raise Exception("File *result.csv already exists!")
    if os.path.exists(file_name + '_raw.csv'):
        raise Exception("File *raw.csv already exists!")
    with open(file_name + '_result.csv', mode='w', newline='') as csv_file_result:
        with open(file_name + '_raw.csv', mode='w', newline='') as csv_file_raw:
            try:
                connection = lanconnection.LanConnection(ip, port)

                result = connection.do_cmd(['init', bar_id])
                if result[0] == 'ERR':
                    print("Error when init")
                    raise ConnectionError(f"Unable to get connection to bar #{bar_id}")

                result = connection.do_cmd(['hvon', bar_id])
                if result[0] == 'ERR':
                    print("Error when hvon")
                    raise ConnectionError(f"Unable to get connection to bar #{bar_id}")
                voltage = start_voltage
                voltage_bit = int(a_slave_set * start_voltage + b_slave_set)

                _headers_slave_result = ('slave set U[V]',
                                         'slave measured U[V]',
                                         'slave avg measured current I[bit]',
                                         'stddev slave current measured I[bit]',
                                         'number of measurements'
                                         )

                _headers_slave_raw = ('slave set U[V]',
                                      'slave measured U[V]',
                                      'slave measured current I[bit]'
                                      )

                writer_result = csv.DictWriter(csv_file_result, fieldnames=_headers_slave_result)
                writer_raw = csv.DictWriter(csv_file_raw, fieldnames=_headers_slave_raw)
                writer_result.writeheader()
                writer_raw.writeheader()
                time.sleep(waiting_time)

                while voltage <= stop_voltage:
                    print(voltage)
                    set_bit_voltage(voltage_bit, connection)
                    time.sleep(step_time)
                    measured_voltage = a_slave_measured * measure_AFE_voltage_slave(connection) + b_slave_measured
                    current_list, avg_current, stddev_current = measure_avg_current3(avg_number, SipmType.SLAVE,
                                                                                     connection)

                    measure_dict_result = {_headers_slave_result[0]: voltage,
                                           _headers_slave_result[1]: measured_voltage,
                                           _headers_slave_result[2]: avg_current,
                                           _headers_slave_result[3]: stddev_current,
                                           _headers_slave_result[4]: avg_number}
                    for current in current_list:
                        measure_dict_raw = {_headers_slave_raw[0]: voltage,
                                            _headers_slave_raw[1]: measured_voltage,
                                            _headers_slave_raw[2]: current}
                        writer_raw.writerow(measure_dict_raw)

                    writer_result.writerow(measure_dict_result)
                    voltage += step
                    voltage_bit = int(a_slave_set * voltage + b_slave_set)

            except Exception as exc:
                result = connection.do_cmd(['hvoff', bar_id])
                if result[0] == 'ERR':
                    print("Error when hvoff")
                connection.close_connection()
                print(exc)

            finally:
                result = connection.do_cmd(['hvoff', bar_id])
                if result[0] == 'ERR':
                    print("Error when hvoff")
                connection.close_connection()


def calibration(waiting_time: float, start: int, stop: int, step_voltage: int, step_time: float,
                step_keithley_time: float, file_name: str, sipm_type: SipmType):
    if os.path.exists(file_name):
        raise Exception("File already exists!")
    with open(file_name, mode='w', newline='') as csv_file:
        try:
            connection = lanconnection.LanConnection(ip, port)

            result = connection.do_cmd(['init', bar_id])
            if result[0] == 'ERR':
                print("Error when init")

            result = connection.do_cmd(['hvon', bar_id])
            if result[0] == 'ERR':
                print("Error when hvon")

            voltage_bit = start
            _headers_master = ('master set U[bit]', 'master measured U[bit]', 'keithley measured U[V]')
            _headers_slave = ('slave set U[bit]', 'slave measured U[bit]', 'keithley measured U[V]')

            if sipm_type == SipmType.MASTER:
                writer = csv.DictWriter(csv_file, fieldnames=_headers_master)
            else:
                writer = csv.DictWriter(csv_file, fieldnames=_headers_slave)
            writer.writeheader()
            keithley = keithley_util.Keithley6517()
            time.sleep(waiting_time)

            while voltage_bit < stop:
                set_bit_voltage(voltage_bit, connection)

                print(voltage_bit)

                measure_dict = {}
                time.sleep(step_time)

                result_keithley = keithley.measure()
                r_num = result_keithley['rNum']
                while result_keithley['rNum'] == r_num:
                    r_num = result_keithley['rNum']
                    time.sleep(step_keithley_time)
                    result_keithley = keithley.measure()

                if sipm_type == SipmType.MASTER:
                    measure_dict[_headers_master[0]] = voltage_bit
                    measure_dict[_headers_master[1]] = measure_AFE_voltage_master(connection)
                else:
                    measure_dict[_headers_slave[0]] = voltage_bit
                    measure_dict[_headers_slave[1]] = measure_AFE_voltage_slave(connection)
                measure_dict[_headers_master[2]] = result_keithley['voltage']

                voltage_bit += step_voltage

                writer.writerow(measure_dict)

            # result = connection.do_cmd(['hvoff', bar_id])
            # if result[0] == 'ERR':
            #     print("Error when hvoff")
            # connection.close_connection()

        except Exception as exc:
            result = connection.do_cmd(['hvoff', bar_id])
            if result[0] == 'ERR':
                print("Error when hvoff")
            connection.close_connection()
            print(exc)

        finally:
            result = connection.do_cmd(['hvoff', bar_id])
            if result[0] == 'ERR':
                print("Error when hvoff")
            connection.close_connection()


def measure_avg_voltage(avg_number: int, sipm_type: SipmType, bar_id: int, connection: lanconnection.LanConnection) -> (float, float):
    number = 0
    measured_voltage_list = []
    while number < avg_number:
        if sipm_type == SipmType.MASTER:
            measured_voltage = connection.do_cmd(['adc', bar_id, 3])[1]
        else:
            measured_voltage = connection.do_cmd(['adc', bar_id, 4])[1]
        measured_voltage_list.append(measured_voltage)
        number += 1
    return statistics.mean(measured_voltage_list), statistics.stdev(measured_voltage_list)


def calibration2(waiting_time: float, start: int, stop: int, step_voltage: int, step_time: float,
                step_keithley_time: float, measurement_no, file_name: str, sipm_type: SipmType):
    if os.path.exists(file_name):
        raise Exception("File already exists!")
    start_time = time.time()
    print("Start time:", time.ctime(start_time))
    with open(file_name, mode='w', newline='') as csv_file:
        try:
            connection = lanconnection.LanConnection(ip, port)

            result = connection.do_cmd(['init', bar_id])
            if result[0] == 'ERR':
                print("Error when init")

            result = connection.do_cmd(['hvon', bar_id])
            if result[0] == 'ERR':
                print("Error when hvon")

            voltage_bit = start
            _headers_master = ('master set U[bit]', 'master measured U[bit]', 'stdev master measured U[bit]', 'measurement no.', 'keithley measured U[V]')
            _headers_slave = ('slave set U[bit]', 'slave measured U[bit]', 'stdev slave measured U[bit]', 'measurement no.', 'keithley measured U[V]')

            if sipm_type == SipmType.MASTER:
                writer = csv.DictWriter(csv_file, fieldnames=_headers_master)
            else:
                writer = csv.DictWriter(csv_file, fieldnames=_headers_slave)
            writer.writeheader()
            keithley = keithley_util.Keithley6517()

            set_bit_voltage(voltage_bit, connection)

            interval = 0
            delta_time = 60
            while interval < waiting_time:
                print('time keithley: ', keithley.measure()['time'])
                if sipm_type == SipmType.MASTER:
                    measured_voltage = connection.do_cmd(['adc', bar_id, 3])[1]
                else:
                    measured_voltage = connection.do_cmd(['adc', bar_id, 4])[1]
                print('voltage AFE[bit]: ', measured_voltage)
                time.sleep(delta_time)
                interval += delta_time

            while voltage_bit < stop:
                set_bit_voltage(voltage_bit, connection)

                print(voltage_bit)

                measure_dict = {}
                time.sleep(step_time)

                result_keithley = keithley.measure()
                r_num = result_keithley['rNum']
                while result_keithley['rNum'] == r_num:
                    r_num = result_keithley['rNum']
                    time.sleep(step_keithley_time)
                    result_keithley = keithley.measure()

                if sipm_type == SipmType.MASTER:
                    measure_dict[_headers_master[0]] = voltage_bit
                    measured_voltage, stddev_measured_voltage = measure_avg_voltage(measurement_no, SipmType.MASTER, bar_id, connection)
                    measure_dict[_headers_master[1]] = measured_voltage
                    measure_dict[_headers_master[2]] = stddev_measured_voltage
                else:
                    measure_dict[_headers_slave[0]] = voltage_bit
                    measured_voltage, stddev_measured_voltage = measure_avg_voltage(measurement_no, SipmType.SLAVE, bar_id, connection)
                    measure_dict[_headers_slave[1]] = measured_voltage
                    measure_dict[_headers_slave[2]] = stddev_measured_voltage
                measure_dict[_headers_master[3]] = measurement_no
                measure_dict[_headers_master[4]] = result_keithley['voltage']

                voltage_bit += step_voltage

                writer.writerow(measure_dict)

            # result = connection.do_cmd(['hvoff', bar_id])
            # if result[0] == 'ERR':
            #     print("Error when hvoff")
            # connection.close_connection()

        except Exception as exc:
            result = connection.do_cmd(['hvoff', bar_id])
            if result[0] == 'ERR':
                print("Error when hvoff")
            connection.close_connection()
            print(exc)

        finally:
            result = connection.do_cmd(['hvoff', bar_id])
            if result[0] == 'ERR':
                print("Error when hvoff")
            connection.close_connection()
            end_time = time.time()
            print("End time:", time.ctime(end_time))
            delta_time = (end_time - start_time) / 60
            print("Delta time:", f"{delta_time:.1}")
            connection.close_connection()


def measure_keithley_avg_voltage(avg_number: int, keithley: keithley_util.Keithley6517, step_keithley_time: float, measurementType: keithley_util.MeasurementType = keithley_util.MeasurementType.VOLTAGE) -> (float, float):
    number = 0
    measured_voltage_list = []
    while number < avg_number:
        result_keithley = keithley.measure()
        r_num = result_keithley['rNum']
        while result_keithley['rNum'] == r_num:
            r_num = result_keithley['rNum']
            time.sleep(step_keithley_time)
            result_keithley = keithley.measure(measurementType)
        measured_voltage_list.append(result_keithley["voltage"])
        number += 1
    return statistics.mean(measured_voltage_list), statistics.stdev(measured_voltage_list)


def calibration3(waiting_time: float, start: int, stop: int, step_voltage: int, step_time: float,
                 step_keithley_time: float, afe_measurement_no: int, keithley_measurement_no: int, file_name: str, sipm_type: SipmType):
    if os.path.exists(file_name):
        raise Exception("File already exists!")
    start_time = time.time()
    print("Start time:", time.ctime(start_time))
    with open(file_name, mode='w', newline='') as csv_file:
        try:
            connection = lanconnection.LanConnection(ip, port)

            result = connection.do_cmd(['init', bar_id])
            if result[0] == 'ERR':
                print("Error when init")

            result = connection.do_cmd(['hvon', bar_id])
            if result[0] == 'ERR':
                print("Error when hvon")

            voltage_bit = start
            _headers_master = ('master set U[bit]', 'master measured U[bit]', 'stdev master measured U[bit]', 'measurement no.', 'keithley measured U[V]', 'std keithley measured U[V]')
            _headers_slave = ('slave set U[bit]', 'slave measured U[bit]', 'stdev slave measured U[bit]', 'measurement no.', 'keithley measured U[V]', 'std keithley measured U[V]')

            if sipm_type == SipmType.MASTER:
                writer = csv.DictWriter(csv_file, fieldnames=_headers_master)
            else:
                writer = csv.DictWriter(csv_file, fieldnames=_headers_slave)
            writer.writeheader()
            keithley = keithley_util.Keithley6517()

            set_bit_voltage(voltage_bit, connection)

            interval = 0
            delta_time = 60
            while interval < waiting_time:
                print('time keithley: ', keithley.measure()['time'])
                if sipm_type == SipmType.MASTER:
                    measured_voltage = connection.do_cmd(['adc', bar_id, 3])[1]
                else:
                    measured_voltage = connection.do_cmd(['adc', bar_id, 4])[1]
                print('voltage AFE[bit]: ', measured_voltage)
                time.sleep(delta_time)
                interval += delta_time

            while voltage_bit < stop:
                set_bit_voltage(voltage_bit, connection)

                print(voltage_bit)

                measure_dict = {}
                time.sleep(step_time)

                keithley_measured_voltage, keithley_stddev_measured_voltage = measure_keithley_avg_voltage(keithley_measurement_no, keithley, step_keithley_time)

                if sipm_type == SipmType.MASTER:
                    measure_dict[_headers_master[0]] = voltage_bit
                    measured_voltage, stddev_measured_voltage = measure_avg_voltage(afe_measurement_no, SipmType.MASTER, bar_id, connection)
                    measure_dict[_headers_master[1]] = measured_voltage
                    measure_dict[_headers_master[2]] = stddev_measured_voltage
                else:
                    measure_dict[_headers_slave[0]] = voltage_bit
                    measured_voltage, stddev_measured_voltage = measure_avg_voltage(afe_measurement_no, SipmType.SLAVE, bar_id, connection)
                    measure_dict[_headers_slave[1]] = measured_voltage
                    measure_dict[_headers_slave[2]] = stddev_measured_voltage
                measure_dict[_headers_master[3]] = afe_measurement_no
                measure_dict[_headers_master[4]] = keithley_measured_voltage
                measure_dict[_headers_master[5]] = keithley_stddev_measured_voltage

                voltage_bit += step_voltage

                writer.writerow(measure_dict)

            # result = connection.do_cmd(['hvoff', bar_id])
            # if result[0] == 'ERR':
            #     print("Error when hvoff")
            # connection.close_connection()

        except Exception as exc:
            result = connection.do_cmd(['hvoff', bar_id])
            if result[0] == 'ERR':
                print("Error when hvoff")
            connection.close_connection()
            print(exc)

        finally:
            result = connection.do_cmd(['hvoff', bar_id])
            if result[0] == 'ERR':
                print("Error when hvoff")
            connection.close_connection()
            end_time = time.time()
            print("End time:", time.ctime(end_time))
            delta_time = (end_time - start_time) / 60
            print("Delta time:", f"{delta_time:.1f}")
            connection.close_connection()


def breakdown_voltage_determination_master(a_master_set: float, b_master_set: float, a_master_measured: float,
                                           b_master_measured: float, waiting_time: float, start_voltage: float,
                                           stop_voltage: float, current_limit: float, voltage_difference: float,
                                           avg_number: int, step_time: float, file_name: str):
    if os.path.exists(file_name):
        raise Exception("File already exists!")
    with open(file_name, mode='w', newline='') as csv_file:
        try:
            connection = lanconnection.LanConnection(ip, port)

            result = connection.do_cmd(['init', bar_id])
            if result[0] == 'ERR':
                print("Error when init")
                raise ConnectionError(f"Unable to get connection to bar #{bar_id}")
            print("Init OK")

            result = connection.do_cmd(['hvon', bar_id])
            if result[0] == 'ERR':
                print("Error when hvon")
                raise ConnectionError(f"Unable to get connection to bar #{bar_id}")
            print("Hvon OK")

            _headers_master = ('master set U[V]', 'master measured U[V]', 'master measured current I[bit]',
                               'master stdev measured current  I[bit]', 'Internal temperature [bit]')

            writer = csv.DictWriter(csv_file, fieldnames=_headers_master)
            writer.writeheader()
            time.sleep(waiting_time)

            voltage_bit = int(a_master_set * start_voltage + b_master_set)
            set_bit_voltage(voltage_bit, connection)
            time.sleep(step_time)

            measured_voltage = a_master_measured * measure_AFE_voltage_master(connection) + b_master_measured
            measured_current, stddev_measured_current = measure_avg_current2(avg_number, SipmType.MASTER, connection)
            temp = measure_AFE_temp(connection)

            measure_dict = {_headers_master[0]: start_voltage,
                            _headers_master[1]: measured_voltage,
                            _headers_master[2]: measured_current,
                            _headers_master[3]: stddev_measured_current,
                            _headers_master[4]: temp[0]}
            writer.writerow(measure_dict)

            voltage_bit = int(a_master_set * stop_voltage + b_master_set)
            set_bit_voltage(voltage_bit, connection)
            time.sleep(step_time)
            measured_voltage = a_master_measured * measure_AFE_voltage_master(connection) + b_master_measured
            measured_current, stddev_measured_current = measure_avg_current2(avg_number, SipmType.MASTER, connection)
            temp = measure_AFE_temp(connection)

            measure_dict = {_headers_master[0]: stop_voltage,
                            _headers_master[1]: measured_voltage,
                            _headers_master[2]: measured_current,
                            _headers_master[3]: stddev_measured_current,
                            _headers_master[4]: temp[0]}
            writer.writerow(measure_dict)

            if measured_current < current_limit:
                print("Error - measured current at the maximum voltage below the limit")
                raise ConnectionError(f"Unable to get connection to bar #{bar_id}")

            delta = stop_voltage - start_voltage
            v_s = start_voltage
            v_e = stop_voltage
            v_m = v_s + delta / 2

            while abs(delta) > voltage_difference:
                print(v_m)
                voltage_bit = int(a_master_set * v_m + b_master_set)
                set_bit_voltage(voltage_bit, connection)

                time.sleep(step_time)

                measured_voltage = a_master_measured * measure_AFE_voltage_master(connection) + b_master_measured
                measured_current, stddev_measured_current = measure_avg_current2(avg_number, SipmType.MASTER,
                                                                                 connection)
                temp = measure_AFE_temp(connection)

                if measured_current > current_limit:
                    v_e = v_m
                else:
                    v_s = v_m
                delta = v_e - v_s

                measure_dict = {_headers_master[0]: v_m,
                                _headers_master[1]: measured_voltage,
                                _headers_master[2]: measured_current,
                                _headers_master[3]: stddev_measured_current,
                                _headers_master[4]: temp[0]}

                writer.writerow(measure_dict)
                v_m = v_s + delta / 2

        except Exception as exc:
            result = connection.do_cmd(['hvoff', bar_id])
            if result[0] == 'ERR':
                print("Error when hvoff")
            connection.close_connection()
            print(exc)

        finally:
            result = connection.do_cmd(['hvoff', bar_id])
            if result[0] == 'ERR':
                print("Error when hvoff")
            connection.close_connection()


def breakdown_voltage_determination_master_temp(a_master_set: float, b_master_set: float, a_master_measured: float,
                                                b_master_measured: float, waiting_time: float, start_voltage: float,
                                                stop_voltage: float, current_limit: float, voltage_difference: float,
                                                avg_current_number: int, avg_temp_number: int, step_time: float,
                                                file_name: str):
    if os.path.exists(file_name):
        raise Exception("File already exists!")
    with open(file_name, mode='w', newline='') as csv_file:
        try:
            connection = lanconnection.LanConnection(ip, port)

            result = connection.do_cmd(['init', bar_id])
            if result[0] == 'ERR':
                print("Error when init")
                raise ConnectionError(f"Unable to get connection to bar #{bar_id}")
            print("Init OK")

            result = connection.do_cmd(['hvon', bar_id])
            if result[0] == 'ERR':
                print("Error when hvon")
                raise ConnectionError(f"Unable to get connection to bar #{bar_id}")
            print("Hvon OK")

            _headers_master = ('master set U[V]', 'master measured U[V]', 'master measured current I[bit]',
                               'master stdev measured current  I[bit]', ',master internal temperature [bit]',
                               'master stdev measured temperature [bit]')

            writer = csv.DictWriter(csv_file, fieldnames=_headers_master)
            writer.writeheader()
            time.sleep(waiting_time)

            voltage_bit = int(a_master_set * start_voltage + b_master_set)
            set_bit_voltage(voltage_bit, connection)
            time.sleep(step_time)

            measured_voltage = a_master_measured * measure_AFE_voltage_master(connection) + b_master_measured
            measured_current, stddev_measured_current = measure_avg_current2(avg_current_number, SipmType.MASTER,
                                                                             connection)
            temp = measure_AFE_temp_avg_master(avg_temp_number, connection)

            measure_dict = {_headers_master[0]: start_voltage,
                            _headers_master[1]: measured_voltage,
                            _headers_master[2]: measured_current,
                            _headers_master[3]: stddev_measured_current,
                            _headers_master[4]: temp[0],
                            _headers_master[5]: temp[1]}
            writer.writerow(measure_dict)

            voltage_bit = int(a_master_set * stop_voltage + b_master_set)
            set_bit_voltage(voltage_bit, connection)
            time.sleep(step_time)
            measured_voltage = a_master_measured * measure_AFE_voltage_master(connection) + b_master_measured
            measured_current, stddev_measured_current = measure_avg_current2(avg_current_number, SipmType.MASTER,
                                                                             connection)
            temp = measure_AFE_temp_avg_master(avg_temp_number, connection)

            measure_dict = {_headers_master[0]: stop_voltage,
                            _headers_master[1]: measured_voltage,
                            _headers_master[2]: measured_current,
                            _headers_master[3]: stddev_measured_current,
                            _headers_master[4]: temp[0],
                            _headers_master[5]: temp[1]}
            writer.writerow(measure_dict)

            if measured_current < current_limit:
                print("Error - measured current at the maximum voltage below the limit")
                raise ConnectionError(f"Unable to get connection to bar #{bar_id}")

            delta = stop_voltage - start_voltage
            v_s = start_voltage
            v_e = stop_voltage
            v_m = v_s + delta / 2

            while abs(delta) > voltage_difference:
                print(v_m)
                voltage_bit = int(a_master_set * v_m + b_master_set)
                set_bit_voltage(voltage_bit, connection)

                time.sleep(step_time)

                measured_voltage = a_master_measured * measure_AFE_voltage_master(connection) + b_master_measured
                measured_current, stddev_measured_current = measure_avg_current2(avg_current_number, SipmType.MASTER,
                                                                                 connection)
                temp = measure_AFE_temp_avg_master(avg_temp_number, connection)

                if measured_current > current_limit:
                    v_e = v_m
                else:
                    v_s = v_m
                delta = v_e - v_s

                measure_dict = {_headers_master[0]: v_m,
                                _headers_master[1]: measured_voltage,
                                _headers_master[2]: measured_current,
                                _headers_master[3]: stddev_measured_current,
                                _headers_master[4]: temp[0],
                                _headers_master[5]: temp[1]}

                writer.writerow(measure_dict)
                v_m = v_s + delta / 2

        except Exception as exc:
            result = connection.do_cmd(['hvoff', bar_id])
            if result[0] == 'ERR':
                print("Error when hvoff")
            connection.close_connection()
            print(exc)

        finally:
            result = connection.do_cmd(['hvoff', bar_id])
            if result[0] == 'ERR':
                print("Error when hvoff")
            connection.close_connection()


def breakdown_voltage_determination_master_temp_keithley(a_master_set: float, b_master_set: float,
                                                         a_master_measured: float, b_master_measured: float,
                                                         waiting_time: float, start_voltage: float,
                                                         stop_voltage: float, current_limit: float,
                                                         voltage_difference: float, avg_current_number: int,
                                                         avg_temp_number: int, step_time: float, file_name: str,
                                                         keithley: keithley_util.Keithley6517):
    if os.path.exists(file_name):
        raise Exception("File already exists!")
    with open(file_name, mode='w', newline='') as csv_file:
        try:
            connection = lanconnection.LanConnection(ip, port)

            result = connection.do_cmd(['init', bar_id])
            if result[0] == 'ERR':
                print("Error when init")
                raise ConnectionError(f"Unable to get connection to bar #{bar_id}")
            print("Init OK")

            result = connection.do_cmd(['hvon', bar_id])
            if result[0] == 'ERR':
                print("Error when hvon")
                raise ConnectionError(f"Unable to get connection to bar #{bar_id}")
            print("Hvon OK")

            _headers_master = ('master set U[V]', 'master measured U[V]', 'master measured current I[bit]',
                               'master stdev measured current  I[bit]', ',master internal temperature [bit]',
                               'master stdev measured temperature [bit]', 'temp Keithley [C]')

            writer = csv.DictWriter(csv_file, fieldnames=_headers_master)
            writer.writeheader()
            time.sleep(waiting_time)

            voltage_bit = int(a_master_set * start_voltage + b_master_set)
            set_bit_voltage(voltage_bit, connection)
            time.sleep(step_time)

            measured_voltage = a_master_measured * measure_AFE_voltage_master(connection) + b_master_measured
            measured_current, stddev_measured_current = measure_avg_current2(avg_current_number, SipmType.MASTER,
                                                                             connection)
            temp = measure_AFE_temp_avg_master(avg_temp_number, connection)
            keithley_temp = keithley.measure()['temp']

            measure_dict = {_headers_master[0]: start_voltage,
                            _headers_master[1]: measured_voltage,
                            _headers_master[2]: measured_current,
                            _headers_master[3]: stddev_measured_current,
                            _headers_master[4]: temp[0],
                            _headers_master[5]: temp[1],
                            _headers_master[6]: keithley_temp}
            writer.writerow(measure_dict)

            voltage_bit = int(a_master_set * stop_voltage + b_master_set)
            set_bit_voltage(voltage_bit, connection)
            time.sleep(step_time)
            measured_voltage = a_master_measured * measure_AFE_voltage_master(connection) + b_master_measured
            measured_current, stddev_measured_current = measure_avg_current2(avg_current_number, SipmType.MASTER,
                                                                             connection)
            temp = measure_AFE_temp_avg_master(avg_temp_number, connection)
            keithley_temp = keithley.measure()['temp']

            measure_dict = {_headers_master[0]: stop_voltage,
                            _headers_master[1]: measured_voltage,
                            _headers_master[2]: measured_current,
                            _headers_master[3]: stddev_measured_current,
                            _headers_master[4]: temp[0],
                            _headers_master[5]: temp[1],
                            _headers_master[6]: keithley_temp}
            writer.writerow(measure_dict)

            if measured_current < current_limit:
                print("Error - measured current at the maximum voltage below the limit")
                raise ConnectionError(f"Unable to get connection to bar #{bar_id}")

            delta = stop_voltage - start_voltage
            v_s = start_voltage
            v_e = stop_voltage
            v_m = v_s + delta / 2

            while abs(delta) > voltage_difference:
                print(v_m)
                voltage_bit = int(a_master_set * v_m + b_master_set)
                set_bit_voltage(voltage_bit, connection)

                time.sleep(step_time)

                measured_voltage = a_master_measured * measure_AFE_voltage_master(connection) + b_master_measured
                measured_current, stddev_measured_current = measure_avg_current2(avg_current_number, SipmType.MASTER,
                                                                                 connection)
                temp = measure_AFE_temp_avg_master(avg_temp_number, connection)
                keithley_temp = keithley.measure()['temp']

                if measured_current > current_limit:
                    v_e = v_m
                else:
                    v_s = v_m
                delta = v_e - v_s

                measure_dict = {_headers_master[0]: v_m,
                                _headers_master[1]: measured_voltage,
                                _headers_master[2]: measured_current,
                                _headers_master[3]: stddev_measured_current,
                                _headers_master[4]: temp[0],
                                _headers_master[5]: temp[1],
                                _headers_master[6]: keithley_temp}

                writer.writerow(measure_dict)
                v_m = v_s + delta / 2

        except Exception as exc:
            result = connection.do_cmd(['hvoff', bar_id])
            if result[0] == 'ERR':
                print("Error when hvoff")
            connection.close_connection()
            print(exc)
        #
        # finally:
        #     result = connection.do_cmd(['hvoff', bar_id])
        #     if result[0] == 'ERR':
        #         print("Error when hvoff")
        #     connection.close_connection()


def breakdown_voltage_determination_master_temp_keithley2(a_master_set: float, b_master_set: float,
                                                          a_master_measured: float, b_master_measured: float,
                                                          start_voltage: float,
                                                          stop_voltage: float, current_limit: float,
                                                          voltage_difference: float, avg_current_number: int,
                                                          avg_temp_number: int, step_time: float,
                                                          keithley: keithley_util.Keithley6517,
                                                          connection: lanconnection.LanConnection, writer,
                                                          headers: [str], start_time: float, iter_number: int):
    try:
        voltage_bit = int(a_master_set * start_voltage + b_master_set)
        set_bit_voltage(voltage_bit, connection)
        time.sleep(step_time)

        measured_voltage = a_master_measured * measure_AFE_voltage_master(connection) + b_master_measured
        measured_current, stddev_measured_current = measure_avg_current2(avg_current_number, SipmType.MASTER,
                                                                         connection)
        temp, stddev_temp = measure_AFE_temp_avg_master(avg_temp_number, connection)
        keithley_temp = keithley.measure()['temp']

        measure_dict = {headers[0]: start_voltage,
                        headers[1]: measured_voltage,
                        headers[2]: measured_current,
                        headers[3]: stddev_measured_current,
                        headers[4]: temp,
                        headers[5]: stddev_temp,
                        headers[6]: keithley_temp,
                        headers[7]: start_time,
                        headers[8]: iter_number}
        writer.writerow(measure_dict)

        voltage_bit = int(a_master_set * stop_voltage + b_master_set)
        set_bit_voltage(voltage_bit, connection)
        time.sleep(step_time)
        measured_voltage = a_master_measured * measure_AFE_voltage_master(connection) + b_master_measured
        measured_current, stddev_measured_current = measure_avg_current2(avg_current_number, SipmType.MASTER,
                                                                         connection)
        temp, stddev_temp = measure_AFE_temp_avg_master(avg_temp_number, connection)
        keithley_temp = keithley.measure()['temp']

        measure_dict = {headers[0]: stop_voltage,
                        headers[1]: measured_voltage,
                        headers[2]: measured_current,
                        headers[3]: stddev_measured_current,
                        headers[4]: temp,
                        headers[5]: stddev_temp,
                        headers[6]: keithley_temp,
                        headers[7]: start_time,
                        headers[8]: iter_number}
        writer.writerow(measure_dict)

        if measured_current < current_limit:
            print("Error - measured current at the maximum voltage below the limit")
            raise ConnectionError(f"Unable to get connection to bar #{bar_id}")

        delta = stop_voltage - start_voltage
        v_s = start_voltage
        v_e = stop_voltage
        v_m = v_s + delta / 2

        while abs(delta) > voltage_difference:
            print(v_m)
            voltage_bit = int(a_master_set * v_m + b_master_set)
            set_bit_voltage(voltage_bit, connection)

            time.sleep(step_time)

            measured_voltage = a_master_measured * measure_AFE_voltage_master(connection) + b_master_measured
            measured_current, stddev_measured_current = measure_avg_current2(avg_current_number, SipmType.MASTER,
                                                                             connection)
            temp, stddev_temp = measure_AFE_temp_avg_master(avg_temp_number, connection)
            keithley_temp = keithley.measure()['temp']

            if measured_current > current_limit:
                v_e = v_m
            else:
                v_s = v_m
            delta = v_e - v_s

            measure_dict = {headers[0]: v_m,
                            headers[1]: measured_voltage,
                            headers[2]: measured_current,
                            headers[3]: stddev_measured_current,
                            headers[4]: temp,
                            headers[5]: stddev_temp,
                            headers[6]: keithley_temp,
                            headers[7]: start_time,
                            headers[8]: iter_number
                            }

            writer.writerow(measure_dict)
            v_m = v_s + delta / 2

    except Exception as exc:
        result = connection.do_cmd(['hvoff', bar_id])
        if result[0] == 'ERR':
            print("Error when hvoff")
        connection.close_connection()
        print(exc)


def breakdown_voltage_determination_master_temp_keithley2_alone(a_master_set: float,
                                                                b_master_set: float,
                                                                a_master_measured: float,
                                                                b_master_measured: float,
                                                                waiting_time: float,
                                                                start_voltage: float,
                                                                stop_voltage: float,
                                                                current_limit: float,
                                                                voltage_difference: float,
                                                                avg_current_number: int,
                                                                step_time: float,
                                                                file_name: str):
    with open(file_name, mode='w', newline='') as csv_file:
        connection = lanconnection.LanConnection(ip, port)
        try:
            voltage_bit = int(a_master_set * start_voltage + b_master_set)
            set_bit_voltage(voltage_bit, connection)
            time.sleep(waiting_time)

            measured_voltage = a_master_measured * measure_AFE_voltage_master(connection) + b_master_measured
            measured_current, stddev_measured_current = measure_avg_current2(avg_current_number, SipmType.MASTER,
                                                                             connection)
            keithley = keithley_util.Keithley6517()
            keithley_temp = keithley.measure()['temp']

            headers = ('master set U[V]', 'master measured U[V]', 'master measured current I[bit]',
                       'master stdev measured current  I[bit]', 'averaging number ', 'temp Keithley [C]')

            measure_dict = {headers[0]: start_voltage,
                            headers[1]: measured_voltage,
                            headers[2]: measured_current,
                            headers[3]: stddev_measured_current,
                            headers[4]: avg_current_number,
                            headers[5]: keithley_temp
                            }

            writer = csv.DictWriter(csv_file, fieldnames=headers)
            writer.writerow(measure_dict)

            voltage_bit = int(a_master_set * stop_voltage + b_master_set)
            set_bit_voltage(voltage_bit, connection)
            time.sleep(step_time)
            measured_voltage = a_master_measured * measure_AFE_voltage_master(connection) + b_master_measured
            measured_current, stddev_measured_current = measure_avg_current2(avg_current_number, SipmType.MASTER,
                                                                             connection)
            keithley_temp = keithley.measure()['temp']

            measure_dict = {headers[0]: stop_voltage,
                            headers[1]: measured_voltage,
                            headers[2]: measured_current,
                            headers[3]: stddev_measured_current,
                            headers[4]: avg_current_number,
                            headers[5]: keithley_temp
                            }
            writer.writerow(measure_dict)

            if measured_current < current_limit:
                print("Error - measured current at the maximum voltage below the limit")
                raise ConnectionError(f"Unable to get connection to bar #{bar_id}")

            delta = stop_voltage - start_voltage
            v_s = start_voltage
            v_e = stop_voltage
            v_m = v_s + delta / 2

            while abs(delta) > voltage_difference:
                print(v_m)
                voltage_bit = int(a_master_set * v_m + b_master_set)
                set_bit_voltage(voltage_bit, connection)

                time.sleep(step_time)

                measured_voltage = a_master_measured * measure_AFE_voltage_master(connection) + b_master_measured
                measured_current, stddev_measured_current = measure_avg_current2(avg_current_number,
                                                                                 SipmType.MASTER,
                                                                                 connection)
                keithley_temp = keithley.measure()['temp']

                if measured_current > current_limit:
                    v_e = v_m
                else:
                    v_s = v_m
                delta = v_e - v_s

                measure_dict = {headers[0]: stop_voltage,
                                headers[1]: measured_voltage,
                                headers[2]: measured_current,
                                headers[3]: stddev_measured_current,
                                headers[4]: avg_current_number,
                                headers[5]: keithley_temp
                                }

                writer.writerow(measure_dict)
                v_m = v_s + delta / 2

        except Exception as exc:
            result = connection.do_cmd(['hvoff', bar_id])
            if result[0] == 'ERR':
                print("Error when hvoff")
            connection.close_connection()
            print(exc)

        finally:
            result = connection.do_cmd(['hvoff', bar_id])
            if result[0] == 'ERR':
                print("Error when hvoff")
            connection.close_connection()


def breakdown_voltage_determination_slave_temp_keithley2(a_slave_set: float, b_slave_set: float,
                                                         a_slave_measured: float, b_slave_measured: float,
                                                         start_voltage: float,
                                                         stop_voltage: float, current_limit: float,
                                                         voltage_difference: float, avg_current_number: int,
                                                         avg_temp_number: int, step_time: float,
                                                         keithley: keithley_util.Keithley6517,
                                                         connection: lanconnection.LanConnection, writer,
                                                         headers: [str], start_time: float, iter_number: int):
    try:
        voltage_bit = int(a_slave_set * start_voltage + b_slave_set)
        set_bit_voltage(voltage_bit, connection)
        time.sleep(step_time)

        measured_voltage = a_slave_measured * measure_AFE_voltage_slave(connection) + b_slave_measured
        measured_current, stddev_measured_current = measure_avg_current2(avg_current_number, SipmType.SLAVE,
                                                                         connection)
        temp, stddev_temp = measure_AFE_temp_avg_slave(avg_temp_number, connection)
        keithley_temp = keithley.measure()['temp']

        measure_dict = {headers[0]: start_voltage,
                        headers[1]: measured_voltage,
                        headers[2]: measured_current,
                        headers[3]: stddev_measured_current,
                        headers[4]: temp,
                        headers[5]: stddev_temp,
                        headers[6]: keithley_temp,
                        headers[7]: start_time,
                        headers[8]: iter_number}
        writer.writerow(measure_dict)

        voltage_bit = int(a_slave_set * stop_voltage + b_slave_set)
        set_bit_voltage(voltage_bit, connection)
        time.sleep(step_time)
        measured_voltage = a_slave_measured * measure_AFE_voltage_master(connection) + b_slave_measured
        measured_current, stddev_measured_current = measure_avg_current2(avg_current_number, SipmType.SLAVE,
                                                                         connection)
        temp, stddev_temp = measure_AFE_temp_avg_slave(avg_temp_number, connection)
        keithley_temp = keithley.measure()['temp']

        measure_dict = {headers[0]: stop_voltage,
                        headers[1]: measured_voltage,
                        headers[2]: measured_current,
                        headers[3]: stddev_measured_current,
                        headers[4]: temp,
                        headers[5]: stddev_temp,
                        headers[6]: keithley_temp,
                        headers[7]: start_time,
                        headers[8]: iter_number}
        writer.writerow(measure_dict)

        if measured_current < current_limit:
            print("Error - measured current at the maximum voltage below the limit")
            raise ConnectionError(f"Unable to get connection to bar #{bar_id}")

        delta = stop_voltage - start_voltage
        v_s = start_voltage
        v_e = stop_voltage
        v_m = v_s + delta / 2

        while abs(delta) > voltage_difference:
            print(v_m)
            voltage_bit = int(a_slave_set * v_m + b_slave_set)
            set_bit_voltage(voltage_bit, connection)

            time.sleep(step_time)

            measured_voltage = a_slave_measured * measure_AFE_voltage_master(connection) + b_slave_measured
            measured_current, stddev_measured_current = measure_avg_current2(avg_current_number, SipmType.SLAVE,
                                                                             connection)
            temp, stddev_temp = measure_AFE_temp_avg_slave(avg_temp_number, connection)
            keithley_temp = keithley.measure()['temp']

            if measured_current > current_limit:
                v_e = v_m
            else:
                v_s = v_m
            delta = v_e - v_s

            measure_dict = {headers[0]: v_m,
                            headers[1]: measured_voltage,
                            headers[2]: measured_current,
                            headers[3]: stddev_measured_current,
                            headers[4]: temp,
                            headers[5]: stddev_temp,
                            headers[6]: keithley_temp,
                            headers[7]: start_time,
                            headers[8]: iter_number
                            }

            writer.writerow(measure_dict)
            v_m = v_s + delta / 2

    except Exception as exc:
        result = connection.do_cmd(['hvoff', bar_id])
        if result[0] == 'ERR':
            print("Error when hvoff")
        connection.close_connection()
        print(exc)


def breakdown_voltage_temp_master_time_dependence(end_date: float, waiting_time: float, a_master_set, b_master_set,
                                                  a_master_measured, b_master_measured, start_voltage,
                                                  stop_voltage, current_limit, voltage_difference, avg_current_number,
                                                  avg_temp_number, step_time, file_name: str):
    if os.path.exists(file_name):
        raise Exception("File already exists!")
    with open(file_name, mode='w', newline='') as csv_file:
        try:
            connection = lanconnection.LanConnection(ip, port)
            result = connection.do_cmd(['init', bar_id])
            if result[0] == 'ERR':
                print("Error when init")
                raise ConnectionError(f"Unable to get connection to bar #{bar_id}")
            print("Init OK")
            result = connection.do_cmd(['hvon', bar_id])
            if result[0] == 'ERR':
                print("Error when hvon")
                raise ConnectionError(f"Unable to get connection to bar #{bar_id}")
            print("Hvon OK")

            _headers_master = ('master set U[V]', 'master measured U[V]', 'master measured current I[bit]',
                               'master stdev measured current  I[bit]', 'master internal temperature [bit]',
                               'master stdev internal temperature [bit]', 'temp Keithley [C]', 'current time',
                               'iter_number')
            writer = csv.DictWriter(csv_file, fieldnames=_headers_master)
            keithley = keithley_util.Keithley6517()
            writer.writeheader()
            time.sleep(waiting_time)
            current_time = time.time()
            iter_number = 0
            print(current_time, iter_number)
            while current_time < end_date:
                breakdown_voltage_determination_master_temp_keithley2(a_master_set, b_master_set, a_master_measured,
                                                                      b_master_measured, start_voltage,
                                                                      stop_voltage, current_limit, voltage_difference,
                                                                      avg_current_number, avg_temp_number, step_time,
                                                                      keithley, connection, writer, _headers_master,
                                                                      current_time, iter_number)
                current_time = time.time()
                iter_number += 1

        except Exception as exc:
            result = connection.do_cmd(['hvoff', bar_id])
            if result[0] == 'ERR':
                print("Error when hvoff")
            connection.close_connection()
            print(exc)

        finally:
            result = connection.do_cmd(['hvoff', bar_id])
            if result[0] == 'ERR':
                print("Error when hvoff")
            connection.close_connection()


def stability_temp3(end_date: float, step: float, step_keithley: float, set_voltage: float, waiting_time: float,
                    file_name: str):
    connection = lanconnection.LanConnection(ip, port)
    try:
        result = connection.do_cmd(['init', bar_id])
        if result[0] == 'ERR':
            print("Error when init")
        else:
            print("init OK")

        result = connection.do_cmd(['hvoff', bar_id])
        if result[0] == 'ERR':
            print("Error when hvoff")
        else:
            print("hvoff OK")

        if os.path.exists(file_name):
            raise Exception("File already exists!")

        _headers = ('date UTC since epoch [s]', 'date from Keithley', 'Voltage AFE U[V]',
                    'Temperature SiPM master [bit]', 'Temperature SiPM slave [bit]',
                    'Temperature keithley [centigrade]')

        with open(file_name, mode='w', newline='') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=_headers)
            writer.writeheader()
            time.sleep(waiting_time)
            current_time = time.time()
            print(current_time)
            voltage_result = connection.do_cmd(['setdac', bar_id, set_voltage, set_voltage])
            print(voltage_result)
            keithley = keithley_util.Keithley6517()
            i = 0
            while current_time < end_date:
                measure_dict = {}
                time.sleep(step)
                result = measure_AFE_temp(connection)
                result_keithley = keithley.measure()
                r_num = result_keithley['rNum']
                while result_keithley['rNum'] == r_num:
                    r_num = result_keithley['rNum']
                    time.sleep(step_keithley)
                    result_keithley = keithley.measure()

                current_time = time.time()
                measure_dict[_headers[0]] = current_time
                measure_dict[_headers[1]] = result_keithley['date'] + ' ' + result_keithley['time']
                measure_dict[_headers[2]] = set_voltage
                measure_dict[_headers[3]] = result[0]
                measure_dict[_headers[4]] = result[1]
                measure_dict[_headers[5]] = result_keithley['temp']

                writer.writerow(measure_dict)
                print(current_time)
                if i % 5:
                    csv_file.flush()
                i = i + 1

        result = connection.do_cmd(['hvoff', bar_id])
        if result[0] == 'ERR':
            print("Error when hvoff")
        connection.close_connection()

    except Exception as exc:
        result = connection.do_cmd(['hvoff', bar_id])
        if result[0] == 'ERR':
            print("Error when hvoff")
        connection.close_connection()
        print(exc)

#Testowa funkcja dla pomiarów AFE master
def new_current_callibration(waiting_time: float, start_voltage: float,
                                 stop_voltage: float, step: float, afe_avg_number: int, step_time: float,
                                 file_name: str):
        if os.path.exists(file_name):
            raise Exception("File already exists!")

        with open(file_name, mode='w', newline='') as csv_file:
            try:
                connection = lanconnection.LanConnection(ip, port)

                result = connection.do_cmd(['init', bar_id])
                if result[0] == 'ERR':
                    print("Error when init")
                    raise ConnectionError(f"Unable to get connection to bar #{bar_id}")

                result = connection.do_cmd(['hvon', bar_id])
                if result[0] == 'ERR':
                    print("Error when hvon")
                    raise ConnectionError(f"Unable to get connection to bar #{bar_id}")
                voltage = start_voltage
                keithley = keithley_util.Keithley6517()
                keithley.setVoltage(voltage)
                _headers_master = ('keithley master set U[V]', 'keithley measured current[A]', 'AFE master measured current [bit]',
                               'AFE master stddev measured current [bit]', 'AFE number of measurements')
                writer = csv.DictWriter(csv_file, fieldnames=_headers_master)
                writer.writeheader()
                time.sleep(waiting_time)
                while voltage <= stop_voltage:
                    print(voltage)

                    keithley_measure = keithley.measure(keithley_util.MeasurementType.CURRENT)
                    afe_current, afe_stddev_current = measure_avg_current2(afe_avg_number, SipmType.MASTER, connection)

                    measure_dict = {_headers_master[0]: voltage,
                                    _headers_master[1]: keithley_measure["current"],
                                    _headers_master[2]: afe_current,
                                    _headers_master[3]: afe_stddev_current,
                                    _headers_master[4]: afe_avg_number}


                    writer.writerow(measure_dict)
                    voltage += step
                    voltage = round(voltage, 2)
                    keithley.setVoltage(voltage)
                    time.sleep(step_time)
                result = connection.do_cmd(['hvoff', bar_id])
                if result[0] == 'ERR':
                    print("Error when hvon")
                    raise ConnectionError(f"Unable to get connection to bar #{bar_id}")
            except Exception as exc:
                result = connection.do_cmd(['hvoff', bar_id])
                if result[0] == 'ERR':
                    print("Error when hvoff")
                connection.close_connection()
                print(exc)

            finally:
                result = connection.do_cmd(['hvoff', bar_id])
                if result[0] == 'ERR':
                    print("Error when hvoff")
                connection.close_connection()

#Testowa funkcja dla pomiarów AFE master
def new_current_callibration_reverse(waiting_time: float, start_voltage: float,
                             stop_voltage: float, step: float, afe_avg_number: int, step_time: float,
                             file_name: str):
    if os.path.exists(file_name):
        raise Exception("File already exists!")
    start_time = time.time()
    print("Start time:", time.ctime(start_time))
    with open(file_name, mode='w', newline='') as csv_file:
        try:
            connection = lanconnection.LanConnection(ip, port)

            result = connection.do_cmd(['init', bar_id])
            if result[0] == 'ERR':
                print("Error when init")
                raise ConnectionError(f"Unable to get connection to bar #{bar_id}")

            result = connection.do_cmd(['hvon', bar_id])
            if result[0] == 'ERR':
                print("Error when hvon")
                raise ConnectionError(f"Unable to get connection to bar #{bar_id}")
            voltage = start_voltage
            keithley = keithley_util.Keithley6517()
            keithley.setVoltage(voltage)
            _headers_master = (
            'keithley master set U[V]', 'keithley measured current[A]', 'stddev keithley measured current[A]', 'AFE master measured current [bit]',
            'AFE master stddev measured current [bit]', 'AFE number of measurements', 'time')
            writer = csv.DictWriter(csv_file, fieldnames=_headers_master)
            writer.writeheader()
            time.sleep(waiting_time)
            while stop_voltage <= voltage:
                print(voltage)

                keithley_measure1 = keithley.measure(keithley_util.MeasurementType.CURRENT)
                afe_current, afe_stddev_current = measure_avg_current2(afe_avg_number, SipmType.MASTER, connection)
                keithley_measure2 = keithley.measure(keithley_util.MeasurementType.CURRENT)
                keithley_measured_current_list = [keithley_measure1["current"], keithley_measure2["current"]]
                avg_keithley_measured_current = statistics.mean(keithley_measured_current_list)
                stdev_keithley_measured_current = statistics.stdev(keithley_measured_current_list)

                measure_dict = {_headers_master[0]: voltage,
                                _headers_master[1]: avg_keithley_measured_current,
                                _headers_master[2]: stdev_keithley_measured_current,
                                _headers_master[3]: afe_current,
                                _headers_master[4]: afe_stddev_current,
                                _headers_master[5]: afe_avg_number,
                                _headers_master[6]: keithley_measure1["time"]}

                writer.writerow(measure_dict)
                voltage -= step
                voltage = round(voltage, 2)
                keithley.setVoltage(voltage)
                time.sleep(step_time)
            connection.do_cmd(['hvoff', bar_id])
        except Exception as exc:
            result = connection.do_cmd(['hvoff', bar_id])
            if result[0] == 'ERR':
                print("Error when hvoff")
            connection.close_connection()
            print(exc)

        finally:
            result = connection.do_cmd(['hvoff', bar_id])
        if result[0] == 'ERR':
            print("Error when hvoff")
        end_time = time.time()
        print("End time:", time.ctime(end_time))
        delta_time = (end_time - start_time)/60
        print("Delta time:", f"{delta_time:.1}")
        connection.close_connection()

#Testowa funkcja dla pomiarów AFE master
def new_current_callibration2(a_master_set, b_master_set,
                              a_master_measured, b_master_measured, waiting_time: float, start_voltage: float,
                              stop_voltage: float, step: float, afe_avg_number: int, step_time: float,
                              file_name: str):
    if os.path.exists(file_name):
        raise Exception("File already exists!")
    start_time = time.time()
    print("Start time:", time.ctime(start_time))
    with open(file_name, mode='w', newline='') as csv_file:
        try:
            connection = lanconnection.LanConnection(ip, port)

            result = connection.do_cmd(['init', bar_id])
            if result[0] == 'ERR':
                print("Error when init")
                raise ConnectionError(f"Unable to get connection to bar #{bar_id}")

            result = connection.do_cmd(['hvon', bar_id])
            if result[0] == 'ERR':
                print("Error when hvon")
                raise ConnectionError(f"Unable to get connection to bar #{bar_id}")
            set_voltage = start_voltage
            voltage_bit = int(a_master_set * start_voltage + b_master_set)
            keithley = keithley_util.Keithley6517()
            _headers_master = (
                'AFE master set U[V]', 'AFE master measured U[V]', 'keithley measured Voltage[V]', 'stddev keithley measured Voltage[V]',
                'AFE master measured current [bit]',
                'AFE master stddev measured current [bit]', 'AFE number of measurements', 'time')
            writer = csv.DictWriter(csv_file, fieldnames=_headers_master)
            writer.writeheader()
            time.sleep(waiting_time)
            while set_voltage <= stop_voltage:
                print(set_voltage)
                set_bit_voltage(voltage_bit, connection)
                keithley_measure1 = keithley.measure(keithley_util.MeasurementType.VOLTAGE)
                afe_measured_voltage = a_master_measured * measure_AFE_voltage_master(connection) + b_master_measured
                afe_current, afe_stddev_current = measure_avg_current2(afe_avg_number, SipmType.MASTER, connection)
                keithley_measure2 = keithley.measure(keithley_util.MeasurementType.VOLTAGE)
                keithley_measured_voltage_list = [keithley_measure1["voltage"], keithley_measure2["voltage"]]
                avg_keithley_measured_voltage = statistics.mean(keithley_measured_voltage_list)
                stdev_keithley_measured_voltage = statistics.stdev(keithley_measured_voltage_list)

                measure_dict = {_headers_master[0]: set_voltage,
                                _headers_master[1]: afe_measured_voltage,
                                _headers_master[2]: avg_keithley_measured_voltage,
                                _headers_master[3]: stdev_keithley_measured_voltage,
                                _headers_master[4]: afe_current,
                                _headers_master[5]: afe_stddev_current,
                                _headers_master[6]: afe_avg_number,
                                _headers_master[7]: keithley_measure1["time"]}
                writer.writerow(measure_dict)
                set_voltage += step
                time.sleep(step_time)
                voltage_bit = int(a_master_set * set_voltage + b_master_set)
        except Exception as exc:
            result = connection.do_cmd(['hvoff', bar_id])
            if result[0] == 'ERR':
                print("Error when hvoff")
            connection.close_connection()
            print(exc)

        finally:
            result = connection.do_cmd(['hvoff', bar_id])
            if result[0] == 'ERR':
                print("Error when hvoff")
            end_time = time.time()
            print("End time:", time.ctime(end_time))
            delta_time = (end_time - start_time)/60
            print("Delta time:", f"{delta_time:.1}")
            connection.close_connection()

#Testowa funkcja dla pomiarów AFE master
def new_current_callibration3(a_master_set, b_master_set,
                              a_master_measured, b_master_measured, waiting_time: float, start_voltage: float,
                              stop_voltage: float, step: float, afe_avg_number: int, step_time: float,
                              file_name: str):
    if os.path.exists(file_name):
        raise Exception("File already exists!")
    start_time = time.time()
    print("Start time:", time.ctime(start_time))
    with open(file_name, mode='w', newline='') as csv_file:
        try:
            connection = lanconnection.LanConnection(ip, port)

            result = connection.do_cmd(['init', bar_id])
            if result[0] == 'ERR':
                print("Error when init")
                raise ConnectionError(f"Unable to get connection to bar #{bar_id}")

            result = connection.do_cmd(['hvon', bar_id])
            if result[0] == 'ERR':
                print("Error when hvon")
                raise ConnectionError(f"Unable to get connection to bar #{bar_id}")
            set_voltage = start_voltage
            voltage_bit = int(a_master_set * start_voltage + b_master_set)
            keithley = keithley_util.Keithley6517()
            _headers_master = (
                'AFE master set U[V]', 'AFE master measured U[V]', 'keithley measured Voltage[V]', 'stddev keithley measured Voltage[V]',
                'AFE master measured current [bit]',
                'AFE master stddev measured current [bit]', 'AFE number of measurements', 'keithley measured Current[A]', 'stddev keithley measured Current[A]',  'time')
            writer = csv.DictWriter(csv_file, fieldnames=_headers_master)
            writer.writeheader()
            time.sleep(waiting_time)
            while set_voltage <= stop_voltage:
                print(set_voltage)
                set_bit_voltage(voltage_bit, connection)
                keithley_measure_voltage1 = keithley.measure(keithley_util.MeasurementType.VOLTAGE)
                afe_measured_voltage = a_master_measured * measure_AFE_voltage_master(connection) + b_master_measured
                afe_current, afe_stddev_current = measure_avg_current2(afe_avg_number, SipmType.MASTER, connection)
                keithley_measure_current1 = keithley.measure(keithley_util.MeasurementType.CURRENT)
                keithley_measure_voltage2 = keithley.measure(keithley_util.MeasurementType.VOLTAGE)
                keithley_measure_current2 = keithley.measure(keithley_util.MeasurementType.CURRENT)
                keithley_measured_voltage_list = [keithley_measure_voltage1["voltage"], keithley_measure_voltage2["voltage"]]
                keithley_measured_current_list = [keithley_measure_current1["current"], keithley_measure_current2["current"]]
                avg_keithley_measured_voltage = statistics.mean(keithley_measured_voltage_list)
                stdev_keithley_measured_voltage = statistics.stdev(keithley_measured_voltage_list)
                avg_keithley_measured_current = statistics.mean(keithley_measured_current_list)
                stdev_keithley_measured_current = statistics.stdev(keithley_measured_current_list)

                measure_dict = {_headers_master[0]: set_voltage,
                                _headers_master[1]: afe_measured_voltage,
                                _headers_master[2]: avg_keithley_measured_voltage,
                                _headers_master[3]: stdev_keithley_measured_voltage,
                                _headers_master[4]: afe_current,
                                _headers_master[5]: afe_stddev_current,
                                _headers_master[6]: afe_avg_number,
                                _headers_master[7]: avg_keithley_measured_current,
                                _headers_master[8]: stdev_keithley_measured_current,
                                _headers_master[9]: keithley_measure_voltage1["time"]}
                writer.writerow(measure_dict)
                set_voltage += step
                time.sleep(step_time)
                voltage_bit = int(a_master_set * set_voltage + b_master_set)
        except Exception as exc:
            result = connection.do_cmd(['hvoff', bar_id])
            if result[0] == 'ERR':
                print("Error when hvoff")
            connection.close_connection()
            print(exc)

        finally:
            result = connection.do_cmd(['hvoff', bar_id])
            if result[0] == 'ERR':
                print("Error when hvoff")
            end_time = time.time()
            print("End time:", time.ctime(end_time))
            delta_time = (end_time - start_time)/60
            print("Delta time:", f"{delta_time:.1}")
            connection.close_connection()


def new_current_callibration4(sipmType: SipmType, a_set, b_set,
                              a_measured, b_measured, waiting_time: float, start_voltage: float,
                              stop_voltage: float, step: float, afe_avg_number: int, step_time: float,
                              file_name: str):
    if os.path.exists(file_name):
        raise Exception("File already exists!")
    start_time = time.time()
    print("Start time:", time.ctime(start_time))
    with open(file_name, mode='w', newline='') as csv_file:
        try:
            connection = lanconnection.LanConnection(ip, port)

            result = connection.do_cmd(['init', bar_id])
            if result[0] == 'ERR':
                print("Error when init")
                raise ConnectionError(f"Unable to get connection to bar #{bar_id}")

            result = connection.do_cmd(['hvon', bar_id])
            if result[0] == 'ERR':
                print("Error when hvon")
                raise ConnectionError(f"Unable to get connection to bar #{bar_id}")
            set_voltage = start_voltage
            voltage_bit = int(a_set * start_voltage + b_set)
            keithley = keithley_util.Keithley6517()
            _headers_master = (
                'AFE master set U[V]', 'AFE master measured U[V]', 'keithley measured Voltage[V]', 'stddev keithley measured Voltage[V]',
                'AFE master measured current [bit]',
                'AFE master stddev measured current [bit]', 'AFE number of measurements', 'time')
            writer = csv.DictWriter(csv_file, fieldnames=_headers_master)
            writer.writeheader()
            time.sleep(waiting_time)
            while set_voltage <= stop_voltage:
                print(set_voltage)
                set_bit_voltage(voltage_bit, connection)
                keithley_measure1 = keithley.measure(keithley_util.MeasurementType.VOLTAGE)
                if sipmType == SipmType.MASTER:
                    afe_measured_voltage = a_measured * measure_AFE_voltage_master(connection) + b_measured
                else:
                    afe_measured_voltage = a_measured * measure_AFE_voltage_slave(connection) + b_measured
                afe_current, afe_stddev_current = measure_avg_current2(afe_avg_number, sipmType, connection)
                keithley_measure2 = keithley.measure(keithley_util.MeasurementType.VOLTAGE)
                keithley_measured_voltage_list = [keithley_measure1["voltage"], keithley_measure2["voltage"]]
                avg_keithley_measured_voltage = statistics.mean(keithley_measured_voltage_list)
                stdev_keithley_measured_voltage = statistics.stdev(keithley_measured_voltage_list)

                measure_dict = {_headers_master[0]: set_voltage,
                                _headers_master[1]: afe_measured_voltage,
                                _headers_master[2]: avg_keithley_measured_voltage,
                                _headers_master[3]: stdev_keithley_measured_voltage,
                                _headers_master[4]: afe_current,
                                _headers_master[5]: afe_stddev_current,
                                _headers_master[6]: afe_avg_number,
                                _headers_master[7]: keithley_measure1["time"]}
                writer.writerow(measure_dict)
                set_voltage += step
                time.sleep(step_time)
                voltage_bit = int(a_set * set_voltage + b_set)
        except Exception as exc:
            result = connection.do_cmd(['hvoff', bar_id])
            if result[0] == 'ERR':
                print("Error when hvoff")
            connection.close_connection()
            print(exc)

        finally:
            result = connection.do_cmd(['hvoff', bar_id])
            if result[0] == 'ERR':
                print("Error when hvoff")
            end_time = time.time()
            print("End time:", time.ctime(end_time))
            delta_time = (end_time - start_time)/60
            print("Delta time:", f"{delta_time:.1}")
            connection.close_connection()

def new_current_callibration5(sipmType: SipmType, a_set, b_set,
                              a_measured, b_measured, waiting_time: float, start_voltage: float,
                              stop_voltage: float, step: float, afe_avg_number: int, step_time: float,
                              file_name: str):
    if os.path.exists(file_name):
        raise Exception("File already exists!")
    start_time = time.time()
    print("Start time:", time.ctime(start_time))
    with open(file_name, mode='w', newline='') as csv_file:
        try:
            connection = lanconnection.LanConnection(ip, port)

            result = connection.do_cmd(['init', bar_id])
            if result[0] == 'ERR':
                print("Error when init")
                raise ConnectionError(f"Unable to get connection to bar #{bar_id}")

            result = connection.do_cmd(['hvon', bar_id])
            if result[0] == 'ERR':
                print("Error when hvon")
                raise ConnectionError(f"Unable to get connection to bar #{bar_id}")
            set_voltage = start_voltage
            voltage_bit = int(a_set * start_voltage + b_set)
            keithley = keithley_util.Keithley6517()
            _headers_master = (
                'AFE master expected set U[V]', 'AFE master real set U[V]', 'AFE master measured U[V]', 'keithley measured Voltage[V]', 'stddev keithley measured Voltage[V]',
                'AFE master measured current [bit]',
                'AFE master stddev measured current [bit]', 'AFE number of measurements', 'time')
            writer = csv.DictWriter(csv_file, fieldnames=_headers_master)
            writer.writeheader()
            time.sleep(waiting_time)
            while set_voltage <= stop_voltage:
                print(set_voltage)
                set_bit_voltage(voltage_bit, connection)
                keithley_measure1 = keithley.measure(keithley_util.MeasurementType.VOLTAGE)
                if sipmType == SipmType.MASTER :
                    afe_measured_voltage = a_measured * measure_AFE_voltage_master(connection) + b_measured
                else:
                    afe_measured_voltage = a_measured * measure_AFE_voltage_slave(connection) + b_measured
                afe_current, afe_stddev_current = measure_avg_current2(afe_avg_number, sipmType, connection)
                keithley_measure2 = keithley.measure(keithley_util.MeasurementType.VOLTAGE)
                keithley_measured_voltage_list = [keithley_measure1["voltage"], keithley_measure2["voltage"]]
                avg_keithley_measured_voltage = statistics.mean(keithley_measured_voltage_list)
                stdev_keithley_measured_voltage = statistics.stdev(keithley_measured_voltage_list)

                measure_dict = {_headers_master[0]: set_voltage,
                                _headers_master[1]: (int(a_set * set_voltage + b_set) - b_set)/a_set,
                                _headers_master[2]: afe_measured_voltage,
                                _headers_master[3]: avg_keithley_measured_voltage,
                                _headers_master[4]: stdev_keithley_measured_voltage,
                                _headers_master[5]: afe_current,
                                _headers_master[6]: afe_stddev_current,
                                _headers_master[7]: afe_avg_number,
                                _headers_master[8]: keithley_measure1["time"]}
                writer.writerow(measure_dict)
                set_voltage += step
                time.sleep(step_time)
                voltage_bit = int(a_set * set_voltage + b_set)
        except Exception as exc:
            result = connection.do_cmd(['hvoff', bar_id])
            if result[0] == 'ERR':
                print("Error when hvoff")
            connection.close_connection()
            print(exc)

        finally:
            result = connection.do_cmd(['hvoff', bar_id])
            if result[0] == 'ERR':
                print("Error when hvoff")
            end_time = time.time()
            print("End time:", time.ctime(end_time))
            delta_time = (end_time - start_time)/60
            print("Delta time:", f"{delta_time:.1}")
            connection.close_connection()



def new_current_callibration6(sipmType: SipmType, a_set, b_set, a_measured, b_measured, waiting_time: float,
                              keithley_voltage1: float, waiting_time_keithley1: float, start_voltage1: float, stop_voltage1: float, step1: float,
                              keithley_voltage2: float, waiting_time_keithley2: float, start_voltage2: float, stop_voltage2: float, step2: float,
                              keithley_voltage3: float, waiting_time_keithley3: float, start_voltage3: float, stop_voltage3: float, step3: float,
                              keithley_voltage4: float, waiting_time_keithley4: float, start_voltage4: float, stop_voltage4: float, step4: float,
                              keithley_voltage5: float, waiting_time_keithley5: float, start_voltage5: float, stop_voltage5: float, step5: float,
                              afe_avg_number: int, keithley_avg_number: int, step_time: float, keithley_waiting_time: float, file_name: str):
    if os.path.exists(file_name):
        raise Exception("File already exists!")
    start_time = time.time()
    print("Start time:", time.ctime(start_time))
    with open(file_name, mode='w', newline='') as csv_file:
        try:
            connection = lanconnection.LanConnection(ip, port)

            result = connection.do_cmd(['init', bar_id])
            if result[0] == 'ERR':
                print("Error when init")
                raise ConnectionError(f"Unable to get connection to bar #{bar_id}")

            result = connection.do_cmd(['hvon', bar_id])
            if result[0] == 'ERR':
                print("Error when hvon")
                raise ConnectionError(f"Unable to get connection to bar #{bar_id}")
            keithley = keithley_util.Keithley6517(keithley_util.MeasurementType.CURRENT_VOLTAGE)

            voltage_bit = int(a_set * start_voltage1 + b_set)
            set_bit_voltage(voltage_bit, connection)
            keithley.setVoltage(keithley_voltage1)
            # time.sleep(waiting_time)
            interval = 0
            delta_time = 60
            while interval < waiting_time:
                print('time keithley: ', keithley.measure()['time'])
                if sipmType == SipmType.MASTER:
                    measured_voltage = connection.do_cmd(['adc', bar_id, 3])[1]
                else:
                    measured_voltage = connection.do_cmd(['adc', bar_id, 4])[1]
                print('voltage AFE[bit]: ', measured_voltage)
                time.sleep(delta_time)
                interval += delta_time

            _headers_master = (
                'AFE master expected set U[V]', 'AFE master real set U[V]', 'AFE master measured U[V]', 'keithley measured Voltage[V]', 'stddev keithley measured Voltage[V]',
                'AFE master measured current [bit]',
                'AFE master stddev measured current [bit]', 'AFE number of measurements', 'time')
            _headers_slave = (
                'AFE slave expected set U[V]', 'AFE slave real set U[V]', 'AFE slave measured U[V]', 'keithley measured Voltage[V]', 'stddev keithley measured Voltage[V]',
                'AFE slave measured current [bit]',
                'AFE slave stddev measured current [bit]', 'AFE number of measurements', 'time')
            if sipmType == SipmType.MASTER:
                writer = csv.DictWriter(csv_file, fieldnames=_headers_master)
            else:
                writer = csv.DictWriter(csv_file, fieldnames=_headers_slave)
            writer.writeheader()

            set_voltage = start_voltage1
            voltage_bit = int(a_set * start_voltage1 + b_set)
            keithley.setVoltage(keithley_voltage1)
            time.sleep(waiting_time_keithley1)
            while set_voltage <= stop_voltage1:
                print(set_voltage)
                set_bit_voltage(voltage_bit, connection)
                keithley_measured_voltage, keithley_stddev_measured_voltage = measure_keithley_avg_voltage(
                    keithley_avg_number, keithley, keithley_waiting_time, keithley_util.MeasurementType.CURRENT_VOLTAGE)
                if sipmType == SipmType.MASTER:
                    afe_measured_voltage = a_measured * measure_AFE_voltage_master(connection) + b_measured
                else:
                    afe_measured_voltage = a_measured * measure_AFE_voltage_slave(connection) + b_measured
                afe_current, afe_stddev_current = measure_avg_current2(afe_avg_number, sipmType, connection)
                if sipmType == SipmType.MASTER:
                    measure_dict = {_headers_master[0]: set_voltage,
                                    _headers_master[1]: (int(a_set * set_voltage + b_set) - b_set)/a_set,
                                    _headers_master[2]: afe_measured_voltage,
                                    _headers_master[3]: keithley_measured_voltage,
                                    _headers_master[4]: keithley_stddev_measured_voltage,
                                    _headers_master[5]: afe_current,
                                    _headers_master[6]: afe_stddev_current,
                                    _headers_master[7]: afe_avg_number,
                                    _headers_master[8]: time.ctime(time.time())}
                else:
                    measure_dict = {_headers_slave[0]: set_voltage,
                                    _headers_slave[1]: (int(a_set * set_voltage + b_set) - b_set)/a_set,
                                    _headers_slave[2]: afe_measured_voltage,
                                    _headers_slave[3]: keithley_measured_voltage,
                                    _headers_slave[4]: keithley_stddev_measured_voltage,
                                    _headers_slave[5]: afe_current,
                                    _headers_slave[6]: afe_stddev_current,
                                    _headers_slave[7]: afe_avg_number,
                                    _headers_slave[8]: time.ctime(time.time())}
                writer.writerow(measure_dict)
                set_voltage += step1
                time.sleep(step_time)
                voltage_bit = int(a_set * set_voltage + b_set)

            set_voltage = start_voltage2
            voltage_bit = int(a_set * start_voltage2 + b_set)
            keithley.setVoltage(keithley_voltage2)
            time.sleep(waiting_time_keithley2)
            while set_voltage <= stop_voltage2:
                print(set_voltage)
                set_bit_voltage(voltage_bit, connection)
                keithley_measured_voltage, keithley_stddev_measured_voltage = measure_keithley_avg_voltage(
                    keithley_avg_number, keithley, keithley_waiting_time,
                    keithley_util.MeasurementType.CURRENT_VOLTAGE)
                if sipmType == SipmType.MASTER:
                    afe_measured_voltage = a_measured * measure_AFE_voltage_master(connection) + b_measured
                else:
                    afe_measured_voltage = a_measured * measure_AFE_voltage_slave(connection) + b_measured
                afe_current, afe_stddev_current = measure_avg_current2(afe_avg_number, sipmType, connection)
                if sipmType == SipmType.MASTER:
                    measure_dict = {_headers_master[0]: set_voltage,
                                    _headers_master[1]: (int(a_set * set_voltage + b_set) - b_set) / a_set,
                                    _headers_master[2]: afe_measured_voltage,
                                    _headers_master[3]: keithley_measured_voltage,
                                    _headers_master[4]: keithley_stddev_measured_voltage,
                                    _headers_master[5]: afe_current,
                                    _headers_master[6]: afe_stddev_current,
                                    _headers_master[7]: afe_avg_number,
                                    _headers_master[8]: time.ctime(time.time())}
                else:
                    measure_dict = {_headers_slave[0]: set_voltage,
                                    _headers_slave[1]: (int(a_set * set_voltage + b_set) - b_set) / a_set,
                                    _headers_slave[2]: afe_measured_voltage,
                                    _headers_slave[3]: keithley_measured_voltage,
                                    _headers_slave[4]: keithley_stddev_measured_voltage,
                                    _headers_slave[5]: afe_current,
                                    _headers_slave[6]: afe_stddev_current,
                                    _headers_slave[7]: afe_avg_number,
                                    _headers_slave[8]: time.ctime(time.time())}
                writer.writerow(measure_dict)
                set_voltage += step2
                time.sleep(step_time)
                voltage_bit = int(a_set * set_voltage + b_set)

            set_voltage = start_voltage3
            voltage_bit = int(a_set * start_voltage3 + b_set)
            keithley.setVoltage(keithley_voltage3)
            time.sleep(waiting_time_keithley3)
            while set_voltage <= stop_voltage3:
                print(set_voltage)
                set_bit_voltage(voltage_bit, connection)
                keithley_measured_voltage, keithley_stddev_measured_voltage = measure_keithley_avg_voltage(
                    keithley_avg_number, keithley, keithley_waiting_time,
                    keithley_util.MeasurementType.CURRENT_VOLTAGE)
                if sipmType == SipmType.MASTER:
                    afe_measured_voltage = a_measured * measure_AFE_voltage_master(connection) + b_measured
                else:
                    afe_measured_voltage = a_measured * measure_AFE_voltage_slave(connection) + b_measured
                afe_current, afe_stddev_current = measure_avg_current2(afe_avg_number, sipmType, connection)
                if sipmType == SipmType.MASTER:
                    measure_dict = {_headers_master[0]: set_voltage,
                                    _headers_master[1]: (int(a_set * set_voltage + b_set) - b_set) / a_set,
                                    _headers_master[2]: afe_measured_voltage,
                                    _headers_master[3]: keithley_measured_voltage,
                                    _headers_master[4]: keithley_stddev_measured_voltage,
                                    _headers_master[5]: afe_current,
                                    _headers_master[6]: afe_stddev_current,
                                    _headers_master[7]: afe_avg_number,
                                    _headers_master[8]: time.ctime(time.time())}
                else:
                    measure_dict = {_headers_slave[0]: set_voltage,
                                    _headers_slave[1]: (int(a_set * set_voltage + b_set) - b_set) / a_set,
                                    _headers_slave[2]: afe_measured_voltage,
                                    _headers_slave[3]: keithley_measured_voltage,
                                    _headers_slave[4]: keithley_stddev_measured_voltage,
                                    _headers_slave[5]: afe_current,
                                    _headers_slave[6]: afe_stddev_current,
                                    _headers_slave[7]: afe_avg_number,
                                    _headers_slave[8]: time.ctime(time.time())}
                writer.writerow(measure_dict)
                set_voltage += step3
                time.sleep(step_time)
                voltage_bit = int(a_set * set_voltage + b_set)

            set_voltage = start_voltage4
            voltage_bit = int(a_set * start_voltage4 + b_set)
            keithley.setVoltage(keithley_voltage4)
            time.sleep(waiting_time_keithley4)
            while set_voltage <= stop_voltage4:
                print(set_voltage)
                set_bit_voltage(voltage_bit, connection)
                keithley_measured_voltage, keithley_stddev_measured_voltage = measure_keithley_avg_voltage(
                    keithley_avg_number, keithley, keithley_waiting_time,
                    keithley_util.MeasurementType.CURRENT_VOLTAGE)
                if sipmType == SipmType.MASTER:
                    afe_measured_voltage = a_measured * measure_AFE_voltage_master(connection) + b_measured
                else:
                    afe_measured_voltage = a_measured * measure_AFE_voltage_slave(connection) + b_measured
                afe_current, afe_stddev_current = measure_avg_current2(afe_avg_number, sipmType, connection)
                if sipmType == SipmType.MASTER:
                    measure_dict = {_headers_master[0]: set_voltage,
                                    _headers_master[1]: (int(a_set * set_voltage + b_set) - b_set) / a_set,
                                    _headers_master[2]: afe_measured_voltage,
                                    _headers_master[3]: keithley_measured_voltage,
                                    _headers_master[4]: keithley_stddev_measured_voltage,
                                    _headers_master[5]: afe_current,
                                    _headers_master[6]: afe_stddev_current,
                                    _headers_master[7]: afe_avg_number,
                                    _headers_master[8]: time.ctime(time.time())}
                else:
                    measure_dict = {_headers_slave[0]: set_voltage,
                                    _headers_slave[1]: (int(a_set * set_voltage + b_set) - b_set) / a_set,
                                    _headers_slave[2]: afe_measured_voltage,
                                    _headers_slave[3]: keithley_measured_voltage,
                                    _headers_slave[4]: keithley_stddev_measured_voltage,
                                    _headers_slave[5]: afe_current,
                                    _headers_slave[6]: afe_stddev_current,
                                    _headers_slave[7]: afe_avg_number,
                                    _headers_slave[8]: time.ctime(time.time())}
                writer.writerow(measure_dict)
                set_voltage += step4
                time.sleep(step_time)
                voltage_bit = int(a_set * set_voltage + b_set)

            set_voltage = start_voltage5
            voltage_bit = int(a_set * start_voltage5 + b_set)
            keithley.setVoltage(keithley_voltage5)
            time.sleep(waiting_time_keithley5)
            while set_voltage <= stop_voltage5:
                print(set_voltage)
                set_bit_voltage(voltage_bit, connection)
                keithley_measured_voltage, keithley_stddev_measured_voltage = measure_keithley_avg_voltage(
                    keithley_avg_number, keithley, keithley_waiting_time,
                    keithley_util.MeasurementType.CURRENT_VOLTAGE)
                if sipmType == SipmType.MASTER:
                    afe_measured_voltage = a_measured * measure_AFE_voltage_master(connection) + b_measured
                else:
                    afe_measured_voltage = a_measured * measure_AFE_voltage_slave(connection) + b_measured
                afe_current, afe_stddev_current = measure_avg_current2(afe_avg_number, sipmType, connection)
                if sipmType == SipmType.MASTER:
                    measure_dict = {_headers_master[0]: set_voltage,
                                    _headers_master[1]: (int(a_set * set_voltage + b_set) - b_set) / a_set,
                                    _headers_master[2]: afe_measured_voltage,
                                    _headers_master[3]: keithley_measured_voltage,
                                    _headers_master[4]: keithley_stddev_measured_voltage,
                                    _headers_master[5]: afe_current,
                                    _headers_master[6]: afe_stddev_current,
                                    _headers_master[7]: afe_avg_number,
                                    _headers_master[8]: time.ctime(time.time())}
                else:
                    measure_dict = {_headers_slave[0]: set_voltage,
                                    _headers_slave[1]: (int(a_set * set_voltage + b_set) - b_set) / a_set,
                                    _headers_slave[2]: afe_measured_voltage,
                                    _headers_slave[3]: keithley_measured_voltage,
                                    _headers_slave[4]: keithley_stddev_measured_voltage,
                                    _headers_slave[5]: afe_current,
                                    _headers_slave[6]: afe_stddev_current,
                                    _headers_slave[7]: afe_avg_number,
                                    _headers_slave[8]: time.ctime(time.time())}
                writer.writerow(measure_dict)
                set_voltage += step5
                time.sleep(step_time)
                voltage_bit = int(a_set * set_voltage + b_set)

        except Exception as exc:
            result = connection.do_cmd(['hvoff', bar_id])
            if result[0] == 'ERR':
                print("Error when hvoff")
            connection.close_connection()
            print(exc)

        finally:
            result = connection.do_cmd(['hvoff', bar_id])
            if result[0] == 'ERR':
                print("Error when hvoff")
            end_time = time.time()
            print("End time:", time.ctime(end_time))
            delta_time = (end_time - start_time)/60
            print("Delta time:", f"{delta_time:.1}")
            connection.close_connection()


def new_current_callibration7(sipmType: SipmType, a_set, b_set, a_measured, b_measured, waiting_time: float,
                              keithley_voltage1: float, waiting_time_keithley1: float, start_voltage1: float, stop_voltage1: float, step1: float,
                              keithley_voltage2: float, waiting_time_keithley2: float, start_voltage2: float, stop_voltage2: float, step2: float,
                              keithley_voltage3: float, waiting_time_keithley3: float, start_voltage3: float, stop_voltage3: float, step3: float,
                              keithley_voltage4: float, waiting_time_keithley4: float, start_voltage4: float, stop_voltage4: float, step4: float,
                              keithley_voltage5: float, waiting_time_keithley5: float, start_voltage5: float, stop_voltage5: float, step5: float,
                              keithley_voltage6: float, waiting_time_keithley6: float, start_voltage6: float, stop_voltage6: float, step6: float,
                              afe_avg_number: int, keithley_avg_number: int, step_time: float, keithley_waiting_time: float, file_name: str):
    if os.path.exists(file_name):
        raise Exception("File already exists!")
    start_time = time.time()
    print("Start time:", time.ctime(start_time))
    with open(file_name, mode='w', newline='') as csv_file:
        try:
            connection = lanconnection.LanConnection(ip, port)

            result = connection.do_cmd(['init', bar_id])
            if result[0] == 'ERR':
                print("Error when init")
                raise ConnectionError(f"Unable to get connection to bar #{bar_id}")

            result = connection.do_cmd(['hvon', bar_id])
            if result[0] == 'ERR':
                print("Error when hvon")
                raise ConnectionError(f"Unable to get connection to bar #{bar_id}")
            keithley = keithley_util.Keithley6517(keithley_util.MeasurementType.CURRENT_VOLTAGE)

            voltage_bit = int(a_set * start_voltage1 + b_set)
            set_bit_voltage(voltage_bit, connection)
            keithley.setVoltage(keithley_voltage1)
            # time.sleep(waiting_time)
            interval = 0
            delta_time = 60
            while interval < waiting_time:
                print('time keithley: ', keithley.measure()['time'])
                if sipmType == SipmType.MASTER:
                    measured_voltage = connection.do_cmd(['adc', bar_id, 3])[1]
                else:
                    measured_voltage = connection.do_cmd(['adc', bar_id, 4])[1]
                print('voltage AFE[bit]: ', measured_voltage)
                time.sleep(delta_time)
                interval += delta_time

            _headers_master = (
                'AFE master expected set U[V]', 'AFE master real set U[V]', 'AFE master measured U[V]', 'keithley measured Voltage[V]', 'stddev keithley measured Voltage[V]',
                'AFE master measured current [bit]',
                'AFE master stddev measured current [bit]', 'AFE number of measurements', 'time')
            _headers_slave = (
                'AFE slave expected set U[V]', 'AFE slave real set U[V]', 'AFE slave measured U[V]', 'keithley measured Voltage[V]', 'stddev keithley measured Voltage[V]',
                'AFE slave measured current [bit]',
                'AFE slave stddev measured current [bit]', 'AFE number of measurements', 'time')
            if sipmType == SipmType.MASTER:
                writer = csv.DictWriter(csv_file, fieldnames=_headers_master)
            else:
                writer = csv.DictWriter(csv_file, fieldnames=_headers_slave)
            writer.writeheader()

            set_voltage = start_voltage1
            voltage_bit = int(a_set * start_voltage1 + b_set)
            keithley.setVoltage(keithley_voltage1)
            time.sleep(waiting_time_keithley1)
            while set_voltage >= stop_voltage1:
                print(set_voltage)
                set_bit_voltage(voltage_bit, connection)
                keithley_measured_voltage, keithley_stddev_measured_voltage = measure_keithley_avg_voltage(
                    keithley_avg_number, keithley, keithley_waiting_time, keithley_util.MeasurementType.CURRENT_VOLTAGE)
                if sipmType == SipmType.MASTER:
                    afe_measured_voltage = a_measured * measure_AFE_voltage_master(connection) + b_measured
                else:
                    afe_measured_voltage = a_measured * measure_AFE_voltage_slave(connection) + b_measured
                afe_current, afe_stddev_current = measure_avg_current2(afe_avg_number, sipmType, connection)
                if sipmType == SipmType.MASTER:
                    measure_dict = {_headers_master[0]: set_voltage,
                                    _headers_master[1]: (int(a_set * set_voltage + b_set) - b_set)/a_set,
                                    _headers_master[2]: afe_measured_voltage,
                                    _headers_master[3]: keithley_measured_voltage,
                                    _headers_master[4]: keithley_stddev_measured_voltage,
                                    _headers_master[5]: afe_current,
                                    _headers_master[6]: afe_stddev_current,
                                    _headers_master[7]: afe_avg_number,
                                    _headers_master[8]: time.ctime(time.time())}
                else:
                    measure_dict = {_headers_slave[0]: set_voltage,
                                    _headers_slave[1]: (int(a_set * set_voltage + b_set) - b_set)/a_set,
                                    _headers_slave[2]: afe_measured_voltage,
                                    _headers_slave[3]: keithley_measured_voltage,
                                    _headers_slave[4]: keithley_stddev_measured_voltage,
                                    _headers_slave[5]: afe_current,
                                    _headers_slave[6]: afe_stddev_current,
                                    _headers_slave[7]: afe_avg_number,
                                    _headers_slave[8]: time.ctime(time.time())}
                writer.writerow(measure_dict)
                set_voltage -= step1
                time.sleep(step_time)
                voltage_bit = int(a_set * set_voltage + b_set)

            set_voltage = start_voltage2
            voltage_bit = int(a_set * start_voltage2 + b_set)
            keithley.setVoltage(keithley_voltage2)
            time.sleep(waiting_time_keithley2)
            while set_voltage >= stop_voltage2:
                print(set_voltage)
                set_bit_voltage(voltage_bit, connection)
                keithley_measured_voltage, keithley_stddev_measured_voltage = measure_keithley_avg_voltage(
                    keithley_avg_number, keithley, keithley_waiting_time,
                    keithley_util.MeasurementType.CURRENT_VOLTAGE)
                if sipmType == SipmType.MASTER:
                    afe_measured_voltage = a_measured * measure_AFE_voltage_master(connection) + b_measured
                else:
                    afe_measured_voltage = a_measured * measure_AFE_voltage_slave(connection) + b_measured
                afe_current, afe_stddev_current = measure_avg_current2(afe_avg_number, sipmType, connection)
                if sipmType == SipmType.MASTER:
                    measure_dict = {_headers_master[0]: set_voltage,
                                    _headers_master[1]: (int(a_set * set_voltage + b_set) - b_set) / a_set,
                                    _headers_master[2]: afe_measured_voltage,
                                    _headers_master[3]: keithley_measured_voltage,
                                    _headers_master[4]: keithley_stddev_measured_voltage,
                                    _headers_master[5]: afe_current,
                                    _headers_master[6]: afe_stddev_current,
                                    _headers_master[7]: afe_avg_number,
                                    _headers_master[8]: time.ctime(time.time())}
                else:
                    measure_dict = {_headers_slave[0]: set_voltage,
                                    _headers_slave[1]: (int(a_set * set_voltage + b_set) - b_set) / a_set,
                                    _headers_slave[2]: afe_measured_voltage,
                                    _headers_slave[3]: keithley_measured_voltage,
                                    _headers_slave[4]: keithley_stddev_measured_voltage,
                                    _headers_slave[5]: afe_current,
                                    _headers_slave[6]: afe_stddev_current,
                                    _headers_slave[7]: afe_avg_number,
                                    _headers_slave[8]: time.ctime(time.time())}
                writer.writerow(measure_dict)
                set_voltage -= step2
                time.sleep(step_time)
                voltage_bit = int(a_set * set_voltage + b_set)

            set_voltage = start_voltage3
            voltage_bit = int(a_set * start_voltage3 + b_set)
            keithley.setVoltage(keithley_voltage3)
            time.sleep(waiting_time_keithley3)
            while set_voltage >= stop_voltage3:
                print(set_voltage)
                set_bit_voltage(voltage_bit, connection)
                keithley_measured_voltage, keithley_stddev_measured_voltage = measure_keithley_avg_voltage(
                    keithley_avg_number, keithley, keithley_waiting_time,
                    keithley_util.MeasurementType.CURRENT_VOLTAGE)
                if sipmType == SipmType.MASTER:
                    afe_measured_voltage = a_measured * measure_AFE_voltage_master(connection) + b_measured
                else:
                    afe_measured_voltage = a_measured * measure_AFE_voltage_slave(connection) + b_measured
                afe_current, afe_stddev_current = measure_avg_current2(afe_avg_number, sipmType, connection)
                if sipmType == SipmType.MASTER:
                    measure_dict = {_headers_master[0]: set_voltage,
                                    _headers_master[1]: (int(a_set * set_voltage + b_set) - b_set) / a_set,
                                    _headers_master[2]: afe_measured_voltage,
                                    _headers_master[3]: keithley_measured_voltage,
                                    _headers_master[4]: keithley_stddev_measured_voltage,
                                    _headers_master[5]: afe_current,
                                    _headers_master[6]: afe_stddev_current,
                                    _headers_master[7]: afe_avg_number,
                                    _headers_master[8]: time.ctime(time.time())}
                else:
                    measure_dict = {_headers_slave[0]: set_voltage,
                                    _headers_slave[1]: (int(a_set * set_voltage + b_set) - b_set) / a_set,
                                    _headers_slave[2]: afe_measured_voltage,
                                    _headers_slave[3]: keithley_measured_voltage,
                                    _headers_slave[4]: keithley_stddev_measured_voltage,
                                    _headers_slave[5]: afe_current,
                                    _headers_slave[6]: afe_stddev_current,
                                    _headers_slave[7]: afe_avg_number,
                                    _headers_slave[8]: time.ctime(time.time())}
                writer.writerow(measure_dict)
                set_voltage -= step3
                time.sleep(step_time)
                voltage_bit = int(a_set * set_voltage + b_set)

            set_voltage = start_voltage4
            voltage_bit = int(a_set * start_voltage4 + b_set)
            keithley.setVoltage(keithley_voltage4)
            time.sleep(waiting_time_keithley4)
            while set_voltage >= stop_voltage4:
                print(set_voltage)
                set_bit_voltage(voltage_bit, connection)
                keithley_measured_voltage, keithley_stddev_measured_voltage = measure_keithley_avg_voltage(
                    keithley_avg_number, keithley, keithley_waiting_time,
                    keithley_util.MeasurementType.CURRENT_VOLTAGE)
                if sipmType == SipmType.MASTER:
                    afe_measured_voltage = a_measured * measure_AFE_voltage_master(connection) + b_measured
                else:
                    afe_measured_voltage = a_measured * measure_AFE_voltage_slave(connection) + b_measured
                afe_current, afe_stddev_current = measure_avg_current2(afe_avg_number, sipmType, connection)
                if sipmType == SipmType.MASTER:
                    measure_dict = {_headers_master[0]: set_voltage,
                                    _headers_master[1]: (int(a_set * set_voltage + b_set) - b_set) / a_set,
                                    _headers_master[2]: afe_measured_voltage,
                                    _headers_master[3]: keithley_measured_voltage,
                                    _headers_master[4]: keithley_stddev_measured_voltage,
                                    _headers_master[5]: afe_current,
                                    _headers_master[6]: afe_stddev_current,
                                    _headers_master[7]: afe_avg_number,
                                    _headers_master[8]: time.ctime(time.time())}
                else:
                    measure_dict = {_headers_slave[0]: set_voltage,
                                    _headers_slave[1]: (int(a_set * set_voltage + b_set) - b_set) / a_set,
                                    _headers_slave[2]: afe_measured_voltage,
                                    _headers_slave[3]: keithley_measured_voltage,
                                    _headers_slave[4]: keithley_stddev_measured_voltage,
                                    _headers_slave[5]: afe_current,
                                    _headers_slave[6]: afe_stddev_current,
                                    _headers_slave[7]: afe_avg_number,
                                    _headers_slave[8]: time.ctime(time.time())}
                writer.writerow(measure_dict)
                set_voltage -= step4
                time.sleep(step_time)
                voltage_bit = int(a_set * set_voltage + b_set)

            set_voltage = start_voltage5
            voltage_bit = int(a_set * start_voltage5 + b_set)
            keithley.setVoltage(keithley_voltage5)
            time.sleep(waiting_time_keithley5)
            while set_voltage >= stop_voltage5:
                print(set_voltage)
                set_bit_voltage(voltage_bit, connection)
                keithley_measured_voltage, keithley_stddev_measured_voltage = measure_keithley_avg_voltage(
                    keithley_avg_number, keithley, keithley_waiting_time,
                    keithley_util.MeasurementType.CURRENT_VOLTAGE)
                if sipmType == SipmType.MASTER:
                    afe_measured_voltage = a_measured * measure_AFE_voltage_master(connection) + b_measured
                else:
                    afe_measured_voltage = a_measured * measure_AFE_voltage_slave(connection) + b_measured
                afe_current, afe_stddev_current = measure_avg_current2(afe_avg_number, sipmType, connection)
                if sipmType == SipmType.MASTER:
                    measure_dict = {_headers_master[0]: set_voltage,
                                    _headers_master[1]: (int(a_set * set_voltage + b_set) - b_set) / a_set,
                                    _headers_master[2]: afe_measured_voltage,
                                    _headers_master[3]: keithley_measured_voltage,
                                    _headers_master[4]: keithley_stddev_measured_voltage,
                                    _headers_master[5]: afe_current,
                                    _headers_master[6]: afe_stddev_current,
                                    _headers_master[7]: afe_avg_number,
                                    _headers_master[8]: time.ctime(time.time())}
                else:
                    measure_dict = {_headers_slave[0]: set_voltage,
                                    _headers_slave[1]: (int(a_set * set_voltage + b_set) - b_set) / a_set,
                                    _headers_slave[2]: afe_measured_voltage,
                                    _headers_slave[3]: keithley_measured_voltage,
                                    _headers_slave[4]: keithley_stddev_measured_voltage,
                                    _headers_slave[5]: afe_current,
                                    _headers_slave[6]: afe_stddev_current,
                                    _headers_slave[7]: afe_avg_number,
                                    _headers_slave[8]: time.ctime(time.time())}
                writer.writerow(measure_dict)
                set_voltage -= step5
                time.sleep(step_time)
                voltage_bit = int(a_set * set_voltage + b_set)

            set_voltage = start_voltage6
            voltage_bit = int(a_set * start_voltage6 + b_set)
            keithley.setVoltage(keithley_voltage6)
            time.sleep(waiting_time_keithley6)
            while set_voltage >= stop_voltage6:
                print(set_voltage)
                set_bit_voltage(voltage_bit, connection)
                keithley_measured_voltage, keithley_stddev_measured_voltage = measure_keithley_avg_voltage(
                    keithley_avg_number, keithley, keithley_waiting_time,
                    keithley_util.MeasurementType.CURRENT_VOLTAGE)
                if sipmType == SipmType.MASTER:
                    afe_measured_voltage = a_measured * measure_AFE_voltage_master(connection) + b_measured
                else:
                    afe_measured_voltage = a_measured * measure_AFE_voltage_slave(connection) + b_measured
                afe_current, afe_stddev_current = measure_avg_current2(afe_avg_number, sipmType, connection)
                if sipmType == SipmType.MASTER:
                    measure_dict = {_headers_master[0]: set_voltage,
                                    _headers_master[1]: (int(a_set * set_voltage + b_set) - b_set) / a_set,
                                    _headers_master[2]: afe_measured_voltage,
                                    _headers_master[3]: keithley_measured_voltage,
                                    _headers_master[4]: keithley_stddev_measured_voltage,
                                    _headers_master[5]: afe_current,
                                    _headers_master[6]: afe_stddev_current,
                                    _headers_master[7]: afe_avg_number,
                                    _headers_master[8]: time.ctime(time.time())}
                else:
                    measure_dict = {_headers_slave[0]: set_voltage,
                                    _headers_slave[1]: (int(a_set * set_voltage + b_set) - b_set) / a_set,
                                    _headers_slave[2]: afe_measured_voltage,
                                    _headers_slave[3]: keithley_measured_voltage,
                                    _headers_slave[4]: keithley_stddev_measured_voltage,
                                    _headers_slave[5]: afe_current,
                                    _headers_slave[6]: afe_stddev_current,
                                    _headers_slave[7]: afe_avg_number,
                                    _headers_slave[8]: time.ctime(time.time())}
                writer.writerow(measure_dict)
                set_voltage -= step6
                time.sleep(step_time)
                voltage_bit = int(a_set * set_voltage + b_set)

        except Exception as exc:
            result = connection.do_cmd(['hvoff', bar_id])
            if result[0] == 'ERR':
                print("Error when hvoff")
            connection.close_connection()
            print(exc)

        finally:
            result = connection.do_cmd(['hvoff', bar_id])
            if result[0] == 'ERR':
                print("Error when hvoff")
            print("Start time:", time.ctime(start_time))
            print("Waiting time:", waiting_time/60)
            end_time = time.time()
            print("End time:", time.ctime(end_time))
            delta_time = (end_time - start_time)/60
            print("Delta time:", f"{delta_time:.1f}")
            connection.close_connection()


def new_current_callibration8(sipmType: SipmType, parameter_file_name: str, waiting_time: float,
                              keithley_voltage1: float, waiting_time_keithley1: float, start_voltage1: float, stop_voltage1: float, step1: float,
                              keithley_voltage2: float, waiting_time_keithley2: float, start_voltage2: float, stop_voltage2: float, step2: float,
                              keithley_voltage3: float, waiting_time_keithley3: float, start_voltage3: float, stop_voltage3: float, step3: float,
                              keithley_voltage4: float, waiting_time_keithley4: float, start_voltage4: float, stop_voltage4: float, step4: float,
                              keithley_voltage5: float, waiting_time_keithley5: float, start_voltage5: float, stop_voltage5: float, step5: float,
                              keithley_voltage6: float, waiting_time_keithley6: float, start_voltage6: float, stop_voltage6: float, step6: float,
                              afe_avg_number: int, keithley_avg_number: int, step_time: float, keithley_waiting_time: float, file_name: str):
    if os.path.exists(file_name):
        raise Exception("File already exists!")
    params = pd.read_csv(parameter_file_name)
    a_set = params.at[0, 'a set']
    b_set = params.at[0, 'b set']
    a_measured = params.at[0, 'a measured']
    b_measured = params.at[0, 'b measured']
    # print(a_set, b_set, a_measured, b_measured)
    start_time = time.time()
    print("Start time:", time.ctime(start_time))
    with open(file_name, mode='w', newline='') as csv_file:
        try:
            connection = lanconnection.LanConnection(ip, port)

            result = connection.do_cmd(['init', bar_id])
            if result[0] == 'ERR':
                print("Error when init")
                raise ConnectionError(f"Unable to get connection to bar #{bar_id}")

            result = connection.do_cmd(['hvon', bar_id])
            if result[0] == 'ERR':
                print("Error when hvon")
                raise ConnectionError(f"Unable to get connection to bar #{bar_id}")
            keithley = keithley_util.Keithley6517(keithley_util.MeasurementType.CURRENT_VOLTAGE)

            voltage_bit = int(a_set * start_voltage1 + b_set)
            set_bit_voltage(voltage_bit, connection)
            keithley.setVoltage(keithley_voltage1)
            # time.sleep(waiting_time)
            interval = 0
            delta_time = 60
            while interval < waiting_time:
                print('time keithley: ', keithley.measure()['time'])
                if sipmType == SipmType.MASTER:
                    measured_voltage = connection.do_cmd(['adc', bar_id, 3])[1]
                else:
                    measured_voltage = connection.do_cmd(['adc', bar_id, 4])[1]
                print('voltage AFE[bit]: ', measured_voltage)
                time.sleep(delta_time)
                interval += delta_time

            _headers_master = (
                'AFE master expected set U[V]', 'AFE master real set U[V]', 'AFE master measured U[V]', 'keithley measured Voltage[V]', 'stddev keithley measured Voltage[V]',
                'AFE master measured current [bit]',
                'AFE master stddev measured current [bit]', 'AFE number of measurements', 'time')
            _headers_slave = (
                'AFE slave expected set U[V]', 'AFE slave real set U[V]', 'AFE slave measured U[V]', 'keithley measured Voltage[V]', 'stddev keithley measured Voltage[V]',
                'AFE slave measured current [bit]',
                'AFE slave stddev measured current [bit]', 'AFE number of measurements', 'time')
            if sipmType == SipmType.MASTER:
                writer = csv.DictWriter(csv_file, fieldnames=_headers_master)
            else:
                writer = csv.DictWriter(csv_file, fieldnames=_headers_slave)
            writer.writeheader()

            set_voltage = start_voltage1
            voltage_bit = int(a_set * start_voltage1 + b_set)
            keithley.setVoltage(keithley_voltage1)
            time.sleep(waiting_time_keithley1)
            while set_voltage >= stop_voltage1:
                print(set_voltage)
                set_bit_voltage(voltage_bit, connection)
                keithley_measured_voltage, keithley_stddev_measured_voltage = measure_keithley_avg_voltage(
                    keithley_avg_number, keithley, keithley_waiting_time, keithley_util.MeasurementType.CURRENT_VOLTAGE)
                if sipmType == SipmType.MASTER:
                    afe_measured_voltage = a_measured * measure_AFE_voltage_master(connection) + b_measured
                else:
                    afe_measured_voltage = a_measured * measure_AFE_voltage_slave(connection) + b_measured
                afe_current, afe_stddev_current = measure_avg_current2(afe_avg_number, sipmType, connection)
                if sipmType == SipmType.MASTER:
                    measure_dict = {_headers_master[0]: set_voltage,
                                    _headers_master[1]: (int(a_set * set_voltage + b_set) - b_set)/a_set,
                                    _headers_master[2]: afe_measured_voltage,
                                    _headers_master[3]: keithley_measured_voltage,
                                    _headers_master[4]: keithley_stddev_measured_voltage,
                                    _headers_master[5]: afe_current,
                                    _headers_master[6]: afe_stddev_current,
                                    _headers_master[7]: afe_avg_number,
                                    _headers_master[8]: time.ctime(time.time())}
                else:
                    measure_dict = {_headers_slave[0]: set_voltage,
                                    _headers_slave[1]: (int(a_set * set_voltage + b_set) - b_set)/a_set,
                                    _headers_slave[2]: afe_measured_voltage,
                                    _headers_slave[3]: keithley_measured_voltage,
                                    _headers_slave[4]: keithley_stddev_measured_voltage,
                                    _headers_slave[5]: afe_current,
                                    _headers_slave[6]: afe_stddev_current,
                                    _headers_slave[7]: afe_avg_number,
                                    _headers_slave[8]: time.ctime(time.time())}
                writer.writerow(measure_dict)
                set_voltage -= step1
                time.sleep(step_time)
                voltage_bit = int(a_set * set_voltage + b_set)

            set_voltage = start_voltage2
            voltage_bit = int(a_set * start_voltage2 + b_set)
            keithley.setVoltage(keithley_voltage2)
            time.sleep(waiting_time_keithley2)
            while set_voltage >= stop_voltage2:
                print(set_voltage)
                set_bit_voltage(voltage_bit, connection)
                keithley_measured_voltage, keithley_stddev_measured_voltage = measure_keithley_avg_voltage(
                    keithley_avg_number, keithley, keithley_waiting_time,
                    keithley_util.MeasurementType.CURRENT_VOLTAGE)
                if sipmType == SipmType.MASTER:
                    afe_measured_voltage = a_measured * measure_AFE_voltage_master(connection) + b_measured
                else:
                    afe_measured_voltage = a_measured * measure_AFE_voltage_slave(connection) + b_measured
                afe_current, afe_stddev_current = measure_avg_current2(afe_avg_number, sipmType, connection)
                if sipmType == SipmType.MASTER:
                    measure_dict = {_headers_master[0]: set_voltage,
                                    _headers_master[1]: (int(a_set * set_voltage + b_set) - b_set) / a_set,
                                    _headers_master[2]: afe_measured_voltage,
                                    _headers_master[3]: keithley_measured_voltage,
                                    _headers_master[4]: keithley_stddev_measured_voltage,
                                    _headers_master[5]: afe_current,
                                    _headers_master[6]: afe_stddev_current,
                                    _headers_master[7]: afe_avg_number,
                                    _headers_master[8]: time.ctime(time.time())}
                else:
                    measure_dict = {_headers_slave[0]: set_voltage,
                                    _headers_slave[1]: (int(a_set * set_voltage + b_set) - b_set) / a_set,
                                    _headers_slave[2]: afe_measured_voltage,
                                    _headers_slave[3]: keithley_measured_voltage,
                                    _headers_slave[4]: keithley_stddev_measured_voltage,
                                    _headers_slave[5]: afe_current,
                                    _headers_slave[6]: afe_stddev_current,
                                    _headers_slave[7]: afe_avg_number,
                                    _headers_slave[8]: time.ctime(time.time())}
                writer.writerow(measure_dict)
                set_voltage -= step2
                time.sleep(step_time)
                voltage_bit = int(a_set * set_voltage + b_set)

            set_voltage = start_voltage3
            voltage_bit = int(a_set * start_voltage3 + b_set)
            keithley.setVoltage(keithley_voltage3)
            time.sleep(waiting_time_keithley3)
            while set_voltage >= stop_voltage3:
                print(set_voltage)
                set_bit_voltage(voltage_bit, connection)
                keithley_measured_voltage, keithley_stddev_measured_voltage = measure_keithley_avg_voltage(
                    keithley_avg_number, keithley, keithley_waiting_time,
                    keithley_util.MeasurementType.CURRENT_VOLTAGE)
                if sipmType == SipmType.MASTER:
                    afe_measured_voltage = a_measured * measure_AFE_voltage_master(connection) + b_measured
                else:
                    afe_measured_voltage = a_measured * measure_AFE_voltage_slave(connection) + b_measured
                afe_current, afe_stddev_current = measure_avg_current2(afe_avg_number, sipmType, connection)
                if sipmType == SipmType.MASTER:
                    measure_dict = {_headers_master[0]: set_voltage,
                                    _headers_master[1]: (int(a_set * set_voltage + b_set) - b_set) / a_set,
                                    _headers_master[2]: afe_measured_voltage,
                                    _headers_master[3]: keithley_measured_voltage,
                                    _headers_master[4]: keithley_stddev_measured_voltage,
                                    _headers_master[5]: afe_current,
                                    _headers_master[6]: afe_stddev_current,
                                    _headers_master[7]: afe_avg_number,
                                    _headers_master[8]: time.ctime(time.time())}
                else:
                    measure_dict = {_headers_slave[0]: set_voltage,
                                    _headers_slave[1]: (int(a_set * set_voltage + b_set) - b_set) / a_set,
                                    _headers_slave[2]: afe_measured_voltage,
                                    _headers_slave[3]: keithley_measured_voltage,
                                    _headers_slave[4]: keithley_stddev_measured_voltage,
                                    _headers_slave[5]: afe_current,
                                    _headers_slave[6]: afe_stddev_current,
                                    _headers_slave[7]: afe_avg_number,
                                    _headers_slave[8]: time.ctime(time.time())}
                writer.writerow(measure_dict)
                set_voltage -= step3
                time.sleep(step_time)
                voltage_bit = int(a_set * set_voltage + b_set)

            set_voltage = start_voltage4
            voltage_bit = int(a_set * start_voltage4 + b_set)
            keithley.setVoltage(keithley_voltage4)
            time.sleep(waiting_time_keithley4)
            while set_voltage >= stop_voltage4:
                print(set_voltage)
                set_bit_voltage(voltage_bit, connection)
                keithley_measured_voltage, keithley_stddev_measured_voltage = measure_keithley_avg_voltage(
                    keithley_avg_number, keithley, keithley_waiting_time,
                    keithley_util.MeasurementType.CURRENT_VOLTAGE)
                if sipmType == SipmType.MASTER:
                    afe_measured_voltage = a_measured * measure_AFE_voltage_master(connection) + b_measured
                else:
                    afe_measured_voltage = a_measured * measure_AFE_voltage_slave(connection) + b_measured
                afe_current, afe_stddev_current = measure_avg_current2(afe_avg_number, sipmType, connection)
                if sipmType == SipmType.MASTER:
                    measure_dict = {_headers_master[0]: set_voltage,
                                    _headers_master[1]: (int(a_set * set_voltage + b_set) - b_set) / a_set,
                                    _headers_master[2]: afe_measured_voltage,
                                    _headers_master[3]: keithley_measured_voltage,
                                    _headers_master[4]: keithley_stddev_measured_voltage,
                                    _headers_master[5]: afe_current,
                                    _headers_master[6]: afe_stddev_current,
                                    _headers_master[7]: afe_avg_number,
                                    _headers_master[8]: time.ctime(time.time())}
                else:
                    measure_dict = {_headers_slave[0]: set_voltage,
                                    _headers_slave[1]: (int(a_set * set_voltage + b_set) - b_set) / a_set,
                                    _headers_slave[2]: afe_measured_voltage,
                                    _headers_slave[3]: keithley_measured_voltage,
                                    _headers_slave[4]: keithley_stddev_measured_voltage,
                                    _headers_slave[5]: afe_current,
                                    _headers_slave[6]: afe_stddev_current,
                                    _headers_slave[7]: afe_avg_number,
                                    _headers_slave[8]: time.ctime(time.time())}
                writer.writerow(measure_dict)
                set_voltage -= step4
                time.sleep(step_time)
                voltage_bit = int(a_set * set_voltage + b_set)

            set_voltage = start_voltage5
            voltage_bit = int(a_set * start_voltage5 + b_set)
            keithley.setVoltage(keithley_voltage5)
            time.sleep(waiting_time_keithley5)
            while set_voltage >= stop_voltage5:
                print(set_voltage)
                set_bit_voltage(voltage_bit, connection)
                keithley_measured_voltage, keithley_stddev_measured_voltage = measure_keithley_avg_voltage(
                    keithley_avg_number, keithley, keithley_waiting_time,
                    keithley_util.MeasurementType.CURRENT_VOLTAGE)
                if sipmType == SipmType.MASTER:
                    afe_measured_voltage = a_measured * measure_AFE_voltage_master(connection) + b_measured
                else:
                    afe_measured_voltage = a_measured * measure_AFE_voltage_slave(connection) + b_measured
                afe_current, afe_stddev_current = measure_avg_current2(afe_avg_number, sipmType, connection)
                if sipmType == SipmType.MASTER:
                    measure_dict = {_headers_master[0]: set_voltage,
                                    _headers_master[1]: (int(a_set * set_voltage + b_set) - b_set) / a_set,
                                    _headers_master[2]: afe_measured_voltage,
                                    _headers_master[3]: keithley_measured_voltage,
                                    _headers_master[4]: keithley_stddev_measured_voltage,
                                    _headers_master[5]: afe_current,
                                    _headers_master[6]: afe_stddev_current,
                                    _headers_master[7]: afe_avg_number,
                                    _headers_master[8]: time.ctime(time.time())}
                else:
                    measure_dict = {_headers_slave[0]: set_voltage,
                                    _headers_slave[1]: (int(a_set * set_voltage + b_set) - b_set) / a_set,
                                    _headers_slave[2]: afe_measured_voltage,
                                    _headers_slave[3]: keithley_measured_voltage,
                                    _headers_slave[4]: keithley_stddev_measured_voltage,
                                    _headers_slave[5]: afe_current,
                                    _headers_slave[6]: afe_stddev_current,
                                    _headers_slave[7]: afe_avg_number,
                                    _headers_slave[8]: time.ctime(time.time())}
                writer.writerow(measure_dict)
                set_voltage -= step5
                time.sleep(step_time)
                voltage_bit = int(a_set * set_voltage + b_set)

            set_voltage = start_voltage6
            voltage_bit = int(a_set * start_voltage6 + b_set)
            keithley.setVoltage(keithley_voltage6)
            time.sleep(waiting_time_keithley6)
            while set_voltage >= stop_voltage6:
                print(set_voltage)
                set_bit_voltage(voltage_bit, connection)
                keithley_measured_voltage, keithley_stddev_measured_voltage = measure_keithley_avg_voltage(
                    keithley_avg_number, keithley, keithley_waiting_time,
                    keithley_util.MeasurementType.CURRENT_VOLTAGE)
                if sipmType == SipmType.MASTER:
                    afe_measured_voltage = a_measured * measure_AFE_voltage_master(connection) + b_measured
                else:
                    afe_measured_voltage = a_measured * measure_AFE_voltage_slave(connection) + b_measured
                afe_current, afe_stddev_current = measure_avg_current2(afe_avg_number, sipmType, connection)
                if sipmType == SipmType.MASTER:
                    measure_dict = {_headers_master[0]: set_voltage,
                                    _headers_master[1]: (int(a_set * set_voltage + b_set) - b_set) / a_set,
                                    _headers_master[2]: afe_measured_voltage,
                                    _headers_master[3]: keithley_measured_voltage,
                                    _headers_master[4]: keithley_stddev_measured_voltage,
                                    _headers_master[5]: afe_current,
                                    _headers_master[6]: afe_stddev_current,
                                    _headers_master[7]: afe_avg_number,
                                    _headers_master[8]: time.ctime(time.time())}
                else:
                    measure_dict = {_headers_slave[0]: set_voltage,
                                    _headers_slave[1]: (int(a_set * set_voltage + b_set) - b_set) / a_set,
                                    _headers_slave[2]: afe_measured_voltage,
                                    _headers_slave[3]: keithley_measured_voltage,
                                    _headers_slave[4]: keithley_stddev_measured_voltage,
                                    _headers_slave[5]: afe_current,
                                    _headers_slave[6]: afe_stddev_current,
                                    _headers_slave[7]: afe_avg_number,
                                    _headers_slave[8]: time.ctime(time.time())}
                writer.writerow(measure_dict)
                set_voltage -= step6
                time.sleep(step_time)
                voltage_bit = int(a_set * set_voltage + b_set)

        except Exception as exc:
            result = connection.do_cmd(['hvoff', bar_id])
            if result[0] == 'ERR':
                print("Error when hvoff")
            connection.close_connection()
            print(exc)

        finally:
            result = connection.do_cmd(['hvoff', bar_id])
            if result[0] == 'ERR':
                print("Error when hvoff")
            print("Start time:", time.ctime(start_time))
            print("Waiting time:", waiting_time/60)
            end_time = time.time()
            print("End time:", time.ctime(end_time))
            delta_time = (end_time - start_time)/60
            print("Delta time:", f"{delta_time:.1f}")
            connection.close_connection()


def current_measurement_to_histogram(sipm_type: SipmType, a_set, b_set, a_measured, b_measured, waiting_time: float,
                                     keithley_voltage: float, afe_voltage: float, afe_avg_number: int, keithley_avg_number: int, keithley_waiting_time: float, file_name: str):
    if os.path.exists(file_name):
        raise Exception("File already exists!")
    start_time = time.time()
    print("Start time:", time.ctime(start_time))
    with open(file_name, mode='w', newline='') as csv_file:
        try:
            connection = lanconnection.LanConnection(ip, port)

            result = connection.do_cmd(['init', bar_id])
            if result[0] == 'ERR':
                print("Error when init")
                raise ConnectionError(f"Unable to get connection to bar #{bar_id}")

            result = connection.do_cmd(['hvon', bar_id])
            if result[0] == 'ERR':
                print("Error when hvon")
                raise ConnectionError(f"Unable to get connection to bar #{bar_id}")
            keithley = keithley_util.Keithley6517(keithley_util.MeasurementType.CURRENT_VOLTAGE)

            voltage_bit = int(a_set * afe_voltage + b_set)
            set_bit_voltage(voltage_bit, connection)
            keithley.setVoltage(keithley_voltage)

            interval = 0
            delta_time = 60
            while interval < waiting_time:
                print('time keithley: ', keithley.measure()['time'])
                if sipm_type == SipmType.MASTER:
                    measured_voltage = connection.do_cmd(['adc', bar_id, 3])[1]
                else:
                    measured_voltage = connection.do_cmd(['adc', bar_id, 4])[1]
                print('voltage AFE[bit]: ', measured_voltage)
                time.sleep(delta_time)
                interval += delta_time

            _headers_master = (
                'AFE master expected set U[V]', 'AFE master real set U[V]', 'AFE master measured U[V]', 'keithley measured Voltage[V]', 'stddev keithley measured Voltage[V]',
                'AFE master measured current [bit]', 'AFE number of measurements', 'time')
            _headers_slave = (
                'AFE slave expected set U[V]', 'AFE slave real set U[V]', 'AFE slave measured U[V]', 'keithley measured Voltage[V]', 'stddev keithley measured Voltage[V]',
                'AFE slave measured current [bit]', 'AFE number of measurements', 'time')
            if sipm_type == SipmType.MASTER:
                writer = csv.DictWriter(csv_file, fieldnames=_headers_master)
            else:
                writer = csv.DictWriter(csv_file, fieldnames=_headers_slave)
            writer.writeheader()


            keithley_measured_voltage, keithley_stddev_measured_voltage = measure_keithley_avg_voltage(
                keithley_avg_number, keithley, keithley_waiting_time, keithley_util.MeasurementType.CURRENT_VOLTAGE)


            number = 0
            # measured_current_list = []
            while number < afe_avg_number:
                if sipm_type == SipmType.MASTER:
                    measured_afe_current = connection.do_cmd(['adc', bar_id, 5])[1]
                    afe_measured_voltage = a_measured * measure_AFE_voltage_master(connection) + b_measured
                    measure_dict = {_headers_master[0]: afe_voltage,
                                    _headers_master[1]: (int(a_set * afe_voltage + b_set) - b_set) / a_set,
                                    _headers_master[2]: afe_measured_voltage,
                                    _headers_master[3]: keithley_measured_voltage,
                                    _headers_master[4]: keithley_stddev_measured_voltage,
                                    _headers_master[5]: measured_afe_current,
                                    _headers_master[6]: afe_avg_number,
                                    _headers_master[7]: time.ctime(time.time())}
                else:
                    measured_afe_current = connection.do_cmd(['adc', bar_id, 6])[1]
                    afe_measured_voltage = a_measured * measure_AFE_voltage_slave(connection) + b_measured
                    measure_dict = {_headers_slave[0]: afe_voltage,
                                    _headers_slave[1]: (int(a_set * afe_voltage + b_set) - b_set) / a_set,
                                    _headers_slave[2]: afe_measured_voltage,
                                    _headers_slave[3]: keithley_measured_voltage,
                                    _headers_slave[4]: keithley_stddev_measured_voltage,
                                    _headers_slave[5]: measured_afe_current,
                                    _headers_slave[6]: afe_avg_number,
                                    _headers_slave[7]: time.ctime(time.time())}
                # measured_current_list.append(measured_afe_current)
                writer.writerow(measure_dict)
                number += 1



        except Exception as exc:
            result = connection.do_cmd(['hvoff', bar_id])
            if result[0] == 'ERR':
                print("Error when hvoff")
            connection.close_connection()
            print(exc)

        finally:
            result = connection.do_cmd(['hvoff', bar_id])
            if result[0] == 'ERR':
                print("Error when hvoff")
            print("Start time:", time.ctime(start_time))
            print("Waiting time:", waiting_time/60)
            end_time = time.time()
            print("End time:", time.ctime(end_time))
            delta_time = (end_time - start_time)/60
            print("Delta time:", f"{delta_time:.1f}")
            connection.close_connection()

def generate_voltage_calibration_parameters_and_plot(sipm_type: SipmType, path_to_file: str, from_set_cal_row: int, to_set_cal_row: int, from_measured_cal_row: int, to_measured_cal_row: int):
    df = pd.read_csv(path_to_file)
    fig_measured, ax_measured = plt.subplots()
    fig_set, ax_set = plt.subplots()
    if sipm_type == SipmType.MASTER:
        df_measured = df.loc[from_measured_cal_row:to_measured_cal_row, ['keithley measured U[V]', 'master measured U[bit]']]
        # print(df_measured)

        results_measured = smf.ols(formula="Q('keithley measured U[V]') ~ Q('master measured U[bit]')", data=df_measured).fit()
        print(results_measured.summary())
        a_measured = results_measured.params["Q('master measured U[bit]')"]
        da_measured = results_measured.bse["Q('master measured U[bit]')"]
        b_measured = results_measured.params["Intercept"]
        db_measured = results_measured.bse["Intercept"]

        df_set = df.loc[from_set_cal_row:to_set_cal_row, ['master set U[bit]', 'keithley measured U[V]']]
        # print('df_set: /n', df_set)
        results_set = smf.ols(formula="Q('master set U[bit]') ~ Q('keithley measured U[V]')", data=df_set).fit()
        print(results_set.summary())

        x_full_measured = df['master measured U[bit]']
        y_full_measured = df['keithley measured U[V]']
        x_selected_measured = x_full_measured[from_measured_cal_row : to_measured_cal_row + 1]
        y_selected_measured = y_full_measured[from_measured_cal_row : to_measured_cal_row + 1]

        # print('x_selected_measured: \n', x_selected_measured)
        # print('y_selected_measured: \n', y_selected_measured)

        x_full_set = df['keithley measured U[V]']
        y_full_set = df['master set U[bit]']
        x_selected_set = x_full_set[from_set_cal_row : to_set_cal_row + 1]
        y_selected_set = y_full_set[from_set_cal_row : to_set_cal_row + 1]
        # print('x_selected_set: \n', x_selected_set)
        # print('y_selected_set: \n', y_selected_set)

    else:
        df_measured = df.loc[from_measured_cal_row:to_measured_cal_row, ['keithley measured U[V]', 'slave measured U[bit]']]
        # print(df_measured)
        results_measured = smf.ols(formula="Q('keithley measured U[V]') ~ Q('slave measured U[bit]')", data=df_measured).fit()
        print(results_measured.summary())
        a_measured = results_measured.params["Q('slave measured U[bit]')"]
        da_measured = results_measured.bse["Q('slave measured U[bit]')"]
        b_measured = results_measured.params["Intercept"]
        db_measured = results_measured.bse["Intercept"]

        df_set = df.loc[from_set_cal_row:to_set_cal_row, ['slave set U[bit]', 'keithley measured U[V]']]
        # print('df_set: /n', df_set)
        results_set = smf.ols(formula="Q('slave set U[bit]') ~ Q('keithley measured U[V]')", data=df_set).fit()
        print(results_set.summary())

        x_full_measured = df['slave measured U[bit]']
        y_full_measured = df['keithley measured U[V]']
        x_selected_measured = x_full_measured[from_measured_cal_row: to_measured_cal_row + 1]
        y_selected_measured = y_full_measured[from_measured_cal_row: to_measured_cal_row + 1]

        # print('x_selected_measured: \n', x_selected_measured)
        # print('y_selected_measured: \n', y_selected_measured)

        x_full_set = df['keithley measured U[V]']
        y_full_set = df['slave set U[bit]']
        x_selected_set = x_full_set[from_set_cal_row : to_set_cal_row + 1]
        y_selected_set = y_full_set[from_set_cal_row : to_set_cal_row + 1]
        # print('x_selected_set: \n', x_selected_set)
        # print('y_selected_set: \n', y_selected_set)

    root, extension = os.path.splitext(path_to_file)

    ax_measured.plot(x_full_measured, y_full_measured, 'mo', markerfacecolor='none')
    ax_measured.plot(x_selected_measured, y_selected_measured, 'mo')

    x0 = x_full_measured.iloc[0]
    y0 = a_measured * x0 + b_measured

    x1 = x_full_measured.iloc[-1]
    y1 = a_measured * x1 + b_measured

    ax_measured.plot([x0, x1], [y0, y1], '-', color='darkred')

    ax_measured.set_xlabel('ADC counts')
    ax_measured.set_ylabel('Voltage [V]')
    equation_measured_text = '$U =' + '{:.7f}'.format(a_measured) + '\pm' + '{:.7f}'.format(da_measured) + 'V \cdot U_{AFE,read} ' + '{:.4f}'.format(b_measured) + \
                    '\pm' + '{:.4f}V'.format(db_measured) + '$'
    ax_measured.text(2670, 63, equation_measured_text, horizontalalignment='left', verticalalignment='top', color='darkred', fontsize=10)
    ax_measured.grid(True)
    fig_measured.savefig(root + '_measured.png')

    a_set = results_set.params["Q('keithley measured U[V]')"]
    da_set = results_set.bse["Q('keithley measured U[V]')"]
    b_set = results_set.params["Intercept"]
    db_set = results_set.bse["Intercept"]

    dict = {'a set': [a_set],
            'std dev a set': [da_set],
            'b set': [b_set],
            'std dev b set': [db_set],
            'a measured': [a_measured],
            'std dev a measured': [da_measured],
            'b measured': [b_measured],
            'std dev b measured': [db_measured],
            }
    df_params = pd.DataFrame(dict)
    df_params.to_csv(root + '_params' + extension, index = False)

    ax_set.plot(x_full_set, y_full_set, 'co', markerfacecolor='none')
    ax_set.plot(x_selected_set, y_selected_set, 'co')

    x0 = x_full_set.iloc[0]
    y0 = a_set * x0 + b_set
    x1 = x_full_set.iloc[-1]
    y1 = a_set * x1 + b_set
    ax_set.plot([x0, x1], [y0, y1], '-', color='darkblue')
    ax_set.set_xlabel('Voltage [V]')
    ax_set.set_ylabel('DAC counts')
    equation_measured_text = '$U_{AFE,set} =' + '{:.3f}'.format(a_set) + '\pm' + '{da:.3f}'.format(da = da_set) + 'V^{-1} \cdot U_{req} + ' +' {b:.2f}'.format(b = b_set) + \
                    '\pm' + '{db:.2f}'.format(db = db_set) + '$'
    ax_set.text(50, 4000, equation_measured_text, horizontalalignment='left', verticalalignment='top', color='darkblue', fontsize=10)
    ax_set.grid(True)
    # plt.scatter(df['keithley measured U[V]'], df['slave set U[bit]'], s=60, c='purple')
    plt.show()
    fig_set.savefig(root + '_set.png')


def generate_current_calibration_parameters_and_plot(sipm_type: SipmType, path_to_file: str):
    df = pd.read_csv(path_to_file)
    R = 4.93e6
    fig, ax = plt.subplots()

    if sipm_type == SipmType.MASTER:
        df_filtered = df.query("`AFE master measured current [bit]` > 0 and `AFE master measured current [bit]` < 4095")
        I_AFE = df_filtered['AFE master expected set U[V]'].subtract(df_filtered['keithley measured Voltage[V]']) / R
        I_bit = df_filtered['AFE master measured current [bit]']
        I_bit_const = sm.add_constant(I_bit)
        results = sm.OLS(I_AFE, I_bit_const).fit()
        a = results.params['AFE master measured current [bit]']
        da = results.bse['AFE master measured current [bit]']
        b = results.params['const']
        db = results.bse['const']
        print(results.summary())

        I_AFE_full = df['AFE master expected set U[V]'].subtract(df['keithley measured Voltage[V]']) / R
        I_bit_full = df['AFE master measured current [bit]']
    else:
        df_filtered = df.query("`AFE slave measured current [bit]` > 0 and `AFE slave measured current [bit]` < 4095")
        I_AFE = df_filtered['AFE slave expected set U[V]'].subtract(df_filtered['keithley measured Voltage[V]']) / R
        I_bit = df_filtered['AFE slave measured current [bit]']
        I_bit_const = sm.add_constant(I_bit)
        results = sm.OLS(I_AFE, I_bit_const).fit()
        a = results.params['AFE slave measured current [bit]']
        da = results.bse['AFE slave measured current [bit]']
        b = results.params["const"]
        db = results.bse["const"]
        print(results.summary())

        I_AFE_full = df['AFE slave expected set U[V]'].subtract(df['keithley measured Voltage[V]']) / R
        I_bit_full = df['AFE slave measured current [bit]']

    root, extension = os.path.splitext(path_to_file)
    ax.grid(True)
    ax.set_xlabel('ADC counts')
    ax.set_ylabel('Current [A]')
    ax.plot(I_bit_full, I_AFE_full, 'o', markerfacecolor='none', color='violet')
    ax.plot(I_bit, I_AFE, 'mo')

    x0 = I_bit_full.iloc[0]
    y0 = a * x0 + b

    x1 = I_bit_full.iloc[-1]
    y1 = a * x1 + b

    ax.plot([x0, x1], [y0, y1], '-', color='darkred')

    equation_text = '$I =' + '{:.4e}'.format(a) + '\pm' + '{:.4e}'.format(da) + 'A \cdot I_{AFE} +' + '{:.2e}'.format(b) + \
                    '\pm' + '{:.2e}A'.format(db) + '$'
    ax.text(0, 0.9E-5, equation_text, horizontalalignment='left', verticalalignment='top', color='darkred', fontsize=8)

    fig.savefig(root + '.png')

    dict = {'a': [a],
            'std dev a': [da],
            'b': [b],
            'std dev b': [db],
            }
    df_params = pd.DataFrame(dict)
    df_params.to_csv(root + '_params' + extension, index = False)

    plt.show()

def test_range():
    keithley = keithley_util.Keithley6517()
    keithley.range()

def test_nplc():
    keithley = keithley_util.Keithley6517()
    keithley.nplc()

if __name__ == '__main__':
    # stability(1651239000, 2, 0.1, 59.5, 5, 'stability_keithley6.csv')
    # stability(1651239300, 2, 0.1, 59.5, 10, 'stability_keithley7.csv')
    # stability(1651284000, 1, 0.01, 59.5, 0, 'stability_keithley8.csv')
    # stability(1651557600, 20, 0.1, 55.5, 30, 'stability_keithley9.csv')
    # calibration(60, 0, 4095, 64, 1, 0.01, 'calibration_keithley.csv', SipmType.MASTER)
    # calibration(300, 0, 4095, 16, 5, 0.1, 'calibration_keithley3.csv', SipmType.MASTER)
    # calibration(600, 0, 4095, 16, 10, 0.1, 'calibration_keithley4.csv', SipmType.MASTER)
    # calibration(600, 0, 4095, 1, 10, 0.2, 'calibration_keithley5.csv', SipmType.MASTER)
    # calibration(30, 0, 4095, 64, 12, 0.01, 'calibration_keithley6.csv', SipmType.MASTER)
    # calibration(30, 0, 4095, 64, 12, 0.01, 'calibration_keithley7.csv', SipmType.MASTER)
    # calibration(300, 0, 4095, 1, 12, 0.01, 'calibration_keithley8_slave_no_resistor.csv', SipmType.SLAVE)
    # calibration(300, 0, 4095, 1, 12, 0.01, 'calibration_keithley9_slave_with_resistor.csv', SipmType.SLAVE)
    # stability(1653285600, 20, 0.1, 55.5, 30, 'stability_keithley_slave_with_load.csv')
    # stability_temp(1653484500, 20, 0.1, 55.5, 30, 'test_temp_stability.csv')
    # stability_temp(1653544800, 10, 0.1, 55.5, 0, 'stability_temp25052022.csv')
    # stability_temp(1653631200, 10, 0.1, 60.0, 0, 'stability_temp26052022.csv')
    # calibration(1500, 0, 4095, 64, 12, 0.01, 'calibration_keithley.csv', SipmType.SLAVE)
    # calibration(60, 0, 4095, 64, 12, 0.01, 'calibration_keithley27052022b.csv', SipmType.SLAVE)
    # calibration(60, 0, 4095, 64, 12, 0.01, 'calibration_keithley27052022b_with_resistor.csv', SipmType.SLAVE)
    # calibration(60, 0, 4095, 64, 12, 0.01, 'calibration_keithley27052022b_without_resistor.csv', SipmType.SLAVE)
    # calibration(60, 0, 4095, 64, 12, 0.01, 'calibration_keithley27052022c_master_without_resistor.csv', SipmType.MASTER)
    # calibration(60, 0, 4095, 64, 12, 0.01, 'calibration_keithley27052022c_master_with_resistor.csv', SipmType.MASTER)
    # calibration(600, 0, 4095, 64, 12, 0.01, 'calibration_keithley27052022d_slave_with_resistor.csv', SipmType.SLAVE)
    # stability_temp(1653890400, 20, 0.1, 60.0, 0, 'stability_temp27052022.csv')
    # calibration(1800, 0, 4095, 64, 12, 0.01, 'calibration_keithley31052022_slave_without_resistor.csv', SipmType.SLAVE)
    # stability_temp2(1654581600, 20, 0.1, 48.0, 0, 'stability_temp2_06062022.csv')
    # stability(1654758000, 0, 0.1, 59.5, 1800, 'stability_current08062022b.csv')
    # current_calibration_SiPM_master(a_master_set_AFE_12, b_master_set_AFE_12, a_master_measured_AFE_12, b_master_measured_AFE_12, 1800, 48.3, 62.8, 0.05, 100, 12, 'current_calibration_14062022.csv')
    # calibration(1800, 0, 4095, 64, 12, 0.01, 'calibration_keithley15062022a_master_without_resistor_AFE_11.csv',SipmType.MASTER) bez wlaczonego filtra uśredniajacego
    # calibration(120, 0, 4095, 64, 12, 0.01, 'calibration_keithley15062022a_slave_without_resistor_AFE_11.csv', SipmType.SLAVE)
    # calibration(120, 0, 4095, 64, 12, 0.01, 'calibration_keithley15062022a_master_without_resistor_AFE_11_filter3.csv',SipmType.MASTER)
    # calibration(60, 0, 4095, 128, 8, 0.01, 'calibration_keithley15062022a_master_without_resistor_AFE_11_reapet.csv', SipmType.MASTER)
    # calibration(60, 0, 4095, 128, 8, 0.01, 'calibration_keithley15062022a_slave_without_resistor_AFE_11_reapet.csv', SipmType.SLAVE)
    # stability_temp(1655622000, 20, 0.1, 60.0, 0, 'stability_temp15062022b_AFE15.csv')
    # calibration(1800, 0, 4095, 64, 12, 0.01, 'calibration_keithley21062022a_master_with_resistor_AFE_11_filter3.csv', SipmType.MASTER)
    # calibration(1800, 0, 4095, 64, 12, 0.01, 'calibration_keithley21062022b_slave_with_resistor_AFE_11_filter3.csv', SipmType.SLAVE)
    # calibration(1800, 0, 4095, 64, 12, 0.01, 'calibration_keithley21062022c_master_without_resistor_AFE_10_filter3.csv', SipmType.MASTER)
    # calibration(1800, 0, 4095, 64, 12, 0.01, 'calibration_keithley21062022d_slave_without_resistor_AFE_10_filter3.csv', SipmType.SLAVE)
    # calibration(1800, 0, 4095, 64, 12, 0.01, 'calibration_keithley21062022e_slave_with_resistor_AFE_10_filter3.csv', SipmType.SLAVE)
    # stability_temp(1655888400, 5, 0.1, 60.0, 0, 'stability_temp22062022a_AFE15_2h.csv')
    # calibration(1800, 0, 4095, 64, 12, 0.01, 'calibration_keithley22062022b_master_with_resistor_AFE_10_filter3.csv', SipmType.MASTER)
    # calibration(1800, 0, 4095, 64, 12, 0.01, 'calibration_keithley22062022c_master_without_resistor_AFE_14_filter3.csv', SipmType.MASTER)
    # calibration(1800, 0, 4095, 64, 12, 0.01, 'calibration_keithley22062022d_slave_without_resistor_AFE_14_filter3.csv', SipmType.SLAVE)
    # current_calibration_SiPM_slave(a_slave_set_AFE_12, b_slave_set_AFE_12, a_slave_measured_AFE_12,
    #                                 b_slave_measured_AFE_12, 1800, 48.3, 62.8, 0.05, 100, 12,
    #                                 'current_calibration_slave_AFE_12_22062022e.csv')
    # calibration(1800, 0, 4095, 64, 12, 0.01, 'calibration_keithley23062022a_master_with_resistor_AFE_14_filter3.csv', SipmType.MASTER)
    # calibration(1800, 0, 4095, 64, 12, 0.01, 'calibration_keithley23062022b_slave_with_resistor_AFE_14_without_filter3.csv', SipmType.SLAVE)
    # calibration(1800, 0, 4095, 64, 12, 0.01, 'calibration_keithley23062022b_slave_with_resistor_AFE_14_filter.csv', SipmType.SLAVE)
    # current_calibration_SiPM_slave(a_master_set_AFE_14, b_master_set_AFE_14, a_master_measured_AFE_14,
    #                                 b_master_measured_AFE_14, 1800, 48.3, 62.8, 0.05, 100, 12,
    #                                 'current_calibration_master_AFE_14_23062022c.csv')
    # calibration(1800, 0, 4095, 64, 12, 0.01, 'calibration_keithley24062022a_master_without_resistor_AFE_15_filter3.csv', SipmType.MASTER)
    # calibration(1800, 0, 4095, 64, 12, 0.01, 'calibration_keithley24062022b_master_with_resistor_AFE_15_filter3.csv', SipmType.MASTER)
    # calibration(1800, 0, 4095, 64, 12, 0.01, 'calibration_keithley24062022c_slave_without_resistor_AFE_15_filter3.csv', SipmType.SLAVE)
    # stability_temp(1656311400, 20, 0.1, 60.0, 0, 'stability_temp24062022d_AFE14.csv')
    # calibration(1800, 0, 4095, 64, 12, 0.01, 'calibration_keithley28062022a_slave_with_resistor_AFE_15_filter3.csv', SipmType.SLAVE)

    # current_calibration_SiPM_master(a_master_set_AFE_14, b_master_set_AFE_14, a_master_measured_AFE_14,
    #                                 b_master_measured_AFE_14, 1800, 48.3, 62.8, 0.05, 100, 12,
    #                                 'current_calibration_master_AFE_14_28062022b.csv')
    # Cos jest nie tak z AFE 14 - ustawiam napięcie i mierzę go na Keithleyu, a nie mierzę żadnego prądu na wewnętrznym amperomierzu

    # stability_temp(1656504000, 5, 0.1, 60.0, 0, 'stability_temp29062022a_AFE14_2h.csv')

    # current_calibration_SiPM_master(a_master_set_AFE_11, b_master_set_AFE_11, a_master_measured_AFE_11,
    #                                 b_master_measured_AFE_11, 1800, 48.3, 62.8, 0.5, 100, 12,
    #                                 'current_calibration_master_AFE_11_01072022a.csv')

    # Cos jest nie tak także z AFE 11 - ustawiam napięcie i mierzę go na Keithleyu, a nie mierzę żadnego prądu na wewnętrznym amperomierzu

    # stability_temp(1656921600, 20, 0.1, 60.0, 0, 'stability_temp01072022b_AFE11.csv')

    # stability_temp(1657013400, 20, 0.1, 60.0, 0, 'stability_temp05072022a_AFE11.csv')

    # stability_temp(1657022400, 10, 0.1, 60.0, 0, 'stability_temp05072022b_AFE14.csv')
    # stability_temp(1657024800, 10, 0.1, 60.0, 0, 'stability_temp05072022c_AFE14.csv')
    # stability_temp(1657035600, 10, 0.1, 60.0, 0, 'stability_temp05072022d_AFE15.csv')
    # stability_temp(1657107000, 10, 0.1, 60.0, 0, 'stability_temp06072022a_AFE10.csv')

    # current_calibration_SiPM_master(a_master_set_AFE_10, b_master_set_AFE_10, a_master_measured_AFE_10,
    #                                 b_master_measured_AFE_10, 1800, 48.3, 62.8, 0.2, 10, 12,
    #                                 'breakdown_voltage_master_AFE_10_06072022b.csv')

    # current_calibration_SiPM_master(a_master_set_AFE_12, b_master_set_AFE_12, a_master_measured_AFE_12,
    #                                 b_master_measured_AFE_12, 1800, 48.3, 62.8, 0.2, 10, 12,
    #                                 'breakdown_voltage_master_AFE_12_ext_SIMP_07072022a.csv')

    # current_calibration_SiPM_slave(a_slave_set_AFE_10, b_slave_set_AFE_10, a_slave_measured_AFE_10,
    #                                 b_slave_measured_AFE_10, 1800, 48.3, 62.8, 0.2, 10, 12,
    #                                 'breakdown_voltage_slave_AFE_10_07072022b.csv')

    # current_calibration_SiPM_slave(a_slave_set_AFE_10, b_slave_set_AFE_10, a_slave_measured_AFE_10,
    #                                 b_slave_measured_AFE_10, 180, 48.3, 62.8, 0.2, 10, 12,
    #                                 'breakdown_voltage_slave_AFE_10_repeat_08072022a.csv')

    # current_calibration_SiPM_slave(a_slave_set_AFE_10, b_slave_set_AFE_10, a_slave_measured_AFE_10,
    #                                 b_slave_measured_AFE_10, 180, 48.3, 62.8, 0.2, 10, 12,
    #                                 'breakdown_voltage_slave_AFE_10_repeat_08072022b.csv')

    # current_calibration_SiPM_slave(a_slave_set_AFE_10, b_slave_set_AFE_10, a_slave_measured_AFE_10,
    #                                 b_slave_measured_AFE_10, 180, 56, 62.8, 0.2, 10, 12,
    #                                 'breakdown_voltage_slave_AFE_10_repeat_08072022c.csv')

    # current_calibration_SiPM_master(a_master_set_AFE_10, b_master_set_AFE_10, a_master_measured_AFE_10,
    #                                 b_master_measured_AFE_10, 180, 56, 62.8, 0.2, 10, 12,
    #                                 'breakdown_voltage_master_AFE_10_repeat_08072022d.csv')

    # current_calibration_SiPM_slave(a_slave_set_AFE_10, b_slave_set_AFE_10, a_slave_measured_AFE_10,
    #                                 b_slave_measured_AFE_10, 180, 52, 62.8, 0.2, 10, 12,
    #                                 'breakdown_voltage_slave_AFE_10_repeat_08072022e.csv')

    # current_calibration_SiPM_slave(a_slave_set_AFE_10, b_slave_set_AFE_10, a_slave_measured_AFE_10,
    #                                 b_slave_measured_AFE_10, 180, 52, 62.8, 0.2, 10, 12,
    #                                 'breakdown_voltage_slave_AFE_10_repeat_08072022f.csv')

    # breakdown_voltage_determination_master(a_master_set_AFE_10, b_master_set_AFE_10, a_master_measured_AFE_10,
    #                                        b_master_measured_AFE_10, 120, 49, 62.8, 20, 0.01, 10, 12, "breakdown_voltage_determination_master_test_temp_AFE_10_12072022b.csv")

    # breakdown_voltage_determination_master(a_master_set_AFE_10, b_master_set_AFE_10, a_master_measured_AFE_10,
    #                                        b_master_measured_AFE_10, 120, 49, 62.8, 20, 0.01, 10, 12, "breakdown_voltage_determination_master_test_SiMP_AFE_10_13072022a.csv")

    # breakdown_voltage_determination_master(a_master_set_AFE_12, b_master_set_AFE_12, a_master_measured_AFE_12,
    #                                        b_master_measured_AFE_12, 120, 49, 62.8, 20, 0.01, 10, 12, "breakdown_voltage_determination_master_test_SiMP_AFE_12_13072022b.csv")

    # current_calibration_SiPM_master(a_master_set_AFE_10, b_master_set_AFE_10, a_master_measured_AFE_10,
    #                                 b_master_measured_AFE_10, 1800, 48.3, 62.8, 0.5, 10, 12,
    #                                 'current_calibration_master_AFE_10_14072022a.csv')

    # current_calibration_SiPM_master(a_master_set_AFE_10, b_master_set_AFE_10, a_master_measured_AFE_10,
    #                                 b_master_measured_AFE_10, 180, 48.3, 62.8, 0.5, 10, 12,
    #                                 'current_calibration_master_AFE_10_1MOhm_14072022b.csv')

    # current_calibration_SiPM_slave(a_slave_set_AFE_10, b_slave_set_AFE_10, a_slave_measured_AFE_10,
    #                                 b_slave_measured_AFE_10, 180, 48.3, 62.8, 0.5, 10, 12,
    #                                 'current_calibration_slave_AFE_10_1MOhm_14072022c.csv')

    # breakdown_voltage_determination_master_temp(a_master_set_AFE_15, b_master_set_AFE_15,
    #                                             a_master_measured_AFE_15, b_master_measured_AFE_15,
    #                                             180, 48.3, 62.8, 20, 0.01, 10, 10, 12, "breakdown_voltage_determination_master_temp_test_SiPM_AFE_15_15072022a.csv")

    # breakdown_voltage_determination_master_temp_keithley(a_master_set_AFE_15, b_master_set_AFE_15,
    #                                             a_master_measured_AFE_15, b_master_measured_AFE_15,
    #                                             180, 48.3, 62.8, 20, 0.01, 10, 10, 12, "breakdown_voltage_determination_master_temp_keithley_test_SiPM_AFE_15_15072022b.csv", keithley_util.Keithley6517())
    # breakdown_voltage_temp_master_time_dependence(1658217600, 120, a_master_set_AFE_15, b_master_set_AFE_15,
    #                                               a_master_measured_AFE_15, b_master_measured_AFE_15, 48.3, 62.8, 20, 0.01, 10, 10, 12, "breakdown_voltage_determination_master_time_dependence_test_SiPM_AFE_15_19072022b.csv")
    # breakdown_voltage_temp_master_time_dependence(1658307600, 300, a_master_set_AFE_15, b_master_set_AFE_15,
    #                                               a_master_measured_AFE_15, b_master_measured_AFE_15, 48.3, 62.8, 20, 0.01, 10, 10, 12, "breakdown_voltage_determination_master_time_dependence_24h_SiPM_AFE_15_19072022c.csv")
    # calibration(1800, 0, 4095, 64, 12, 0.01, 'calibration_keithley20072022a_master_without_resistor_AFE_32_filter3.csv',
    #             SipmType.MASTER)
    # current_calibration_SiPM_master(a_master_set_AFE_32, b_master_set_AFE_32, a_master_measured_AFE_32,
    #                                 b_master_measured_AFE_32, 180, 48.3, 62.8, 0.5, 20, 12,
    #                                 'current_calibration_master_AFE_32_21072022a.csv')
    # calibration(300, 0, 4095, 64, 12, 0.01, 'calibration_keithley21072022b_slave_without_resistor_AFE_32_filter3.csv', SipmType.SLAVE)

    # current_calibration_SiPM_slave(a_slave_set_AFE_32, b_slave_set_AFE_32, a_slave_measured_AFE_32,
    #                                 b_slave_measured_AFE_32, 1800, 48.3, 62.8, 0.2, 100, 12,
    #                                 'current_calibration_slave_AFE_32_21072022c.csv')
    # breakdown_voltage_temp_master_time_dependence(1658732400, 1800, a_master_set_AFE_12, b_master_set_AFE_12,
    #                                               a_master_measured_AFE_12, b_master_measured_AFE_12, 48.3, 62.8, 20, 0.01, 10, 10, 12, "breakdown_voltage_determination_master_time_dependence_3d_SiPM_AFE_12_22072022a.csv")
    # current_calibration_SiPM_slave(a_slave_set_AFE_32, b_slave_set_AFE_32, a_slave_measured_AFE_32,
    #                                 b_slave_measured_AFE_32, 1800, 48.3, 62.8, 0.2, 100, 12,
    #                                 'current_calibration_slave_AFE_32_478MOhm_26072022a.csv')
    # stability_temp(1658913300, 20, 0.1, 60.0, 0, 'test_ethernet.csv')

    # TODO
    # breakdown_voltage_temp_master_time_dependence(1658993400, 1800, a_master_set_AFE_12, b_master_set_AFE_12,
    #                                           a_master_measured_AFE_12, b_master_measured_AFE_12, 48.3, 62.8, 200, 0.01, 10, 10, 12, "breakdown_voltage_determination_master_time_dependence_20h_SiPM_AFE_12_27072022a.csv")
    # current_calibration_SiPM_slave2(a_slave_set_AFE_32, b_slave_set_AFE_32, a_slave_measured_AFE_32,
    #                                 b_slave_measured_AFE_32, 1800, 48.3, 62.8, 0.2, 100, 12,
    #                                 'current_calibration_slave_AFE_32_983MOhm_28072022a.csv')
    # current_calibration_SiPM_slave2(a_slave_set_AFE_32, b_slave_set_AFE_32, a_slave_measured_AFE_32,
    #                                 b_slave_measured_AFE_32, 300, 48.3, 62.8, 2, 100, 12,
    #                                 'current_calibration_slave_AFE_32_983MOhm_29072022a.csv')
    # current_calibration_SiPM_slave2(a_slave_set_AFE_32, b_slave_set_AFE_32, a_slave_measured_AFE_32,
    #                                 b_slave_measured_AFE_32, 1800, 48.3, 62.8, 2, 100, 12,
    #                                 'current_calibration_slave_AFE_32_983MOhm_29072022b.csv')
    # current_calibration_SiPM_slave2(a_slave_set_AFE_32, b_slave_set_AFE_32, a_slave_measured_AFE_32,
    #                                 b_slave_measured_AFE_32, 1800, 48.3, 62.8, 2, 100, 12,
    #                                 'current_calibration_slave_AFE_32_10.5MOhm_29072022b.csv')
    # calibration(1800, 0, 4095, 64, 12, 0.01, 'calibration_keithley01082022a_master_without_resistor_AFE_34_filter3.csv',
    #             SipmType.MASTER)
    # current_calibration_SiPM_master(a_master_set_AFE_34, b_master_set_AFE_34, a_master_measured_AFE_34,
    # b_master_measured_AFE_34, 1800, 48.3, 62.8, 0.5, 10, 12,
    # 'current_calibration_master_AFE_34_10.5MOhm_01082022b.csv')
    # current_calibration_SiPM_master(a_master_set_AFE_34, b_master_set_AFE_34, a_master_measured_AFE_34,
    #                                 b_master_measured_AFE_34, 1800, 48.3, 62.8, 0.5, 100, 12,
    #                                 'current_calibration_master_AFE_34_983MOhm_01082022c.csv')
    # calibration(1800, 0, 4095, 64, 12, 0.01, 'calibration_keithley02082022a_slave_without_resistor_AFE_34_filter3.csv',
    #             SipmType.SLAVE)
    # current_calibration_SiPM_slave2(a_slave_set_AFE_34, b_slave_set_AFE_34, a_slave_measured_AFE_34,
    #                                 b_slave_measured_AFE_34, 600, 48.3, 62.8, 0.5, 10, 12,
    #                                 'current_calibration_slave_AFE_34_10.5MOhm_02082022b.csv')
    # current_calibration_SiPM_slave2(a_slave_set_AFE_34, b_slave_set_AFE_34, a_slave_measured_AFE_34,
    #                                 b_slave_measured_AFE_34, 600, 48.3, 62.8, 0.5, 100, 12,
    #                                 'current_calibration_slave_AFE_34_983MOhm_02082022c.csv')
    # current_calibration_SiPM_master(a_master_set_AFE_32, b_master_set_AFE_32, a_master_measured_AFE_32,
    #                                 b_master_measured_AFE_32, 1800, 48.3, 62.8, 0.5, 100, 12,
    #                                 'current_calibration_master_AFE_32_983MOhm_21072022a.csv')
    # calibration(1800, 0, 4095, 64, 12, 0.01, 'calibration_keithley02082022e_master_without_resistor_AFE_35_filter3.csv',
    #             SipmType.MASTER)
    # current_calibration_SiPM_master2(a_master_set_AFE_35, b_master_set_AFE_35, a_master_measured_AFE_35,
    #                                 b_master_measured_AFE_35, 1800, 48.3, 62.8, 0.5, 100, 12,
    #                                 'current_calibration_master_AFE_35_983MOhm_03082022a.csv')
    # current_calibration_SiPM_master2(a_master_set_AFE_35, b_master_set_AFE_35, a_master_measured_AFE_35,
    #                                 b_master_measured_AFE_35, 600, 48.3, 62.8, 0.5, 10, 12,
    #                                 'current_calibration_master_AFE_35_10.5MOhm_03082022b.csv')
    # calibration(600, 0, 4095, 64, 12, 0.01, 'calibration_keithley03082022b_slave_without_resistor_AFE_35_filter3.csv',
    #             SipmType.SLAVE)
    # current_calibration_SiPM_slave2(a_slave_set_AFE_35, b_slave_set_AFE_35, a_slave_measured_AFE_35,
    #                                 b_slave_measured_AFE_35, 600, 48.3, 62.8, 0.5, 20, 12,
    #                                 'current_calibration_slave_AFE_35_10.5MOhm_03082022c.csv')
    # current_calibration_SiPM_slave2(a_slave_set_AFE_35, b_slave_set_AFE_35, a_slave_measured_AFE_35,
    #                                 b_slave_measured_AFE_35, 600, 48.3, 62.8, 0.5, 100, 12,
    #                                 'current_calibration_slave_AFE_35_983MOhm_03082022d.csv')
    # calibration(1800, 0, 4095, 64, 12, 0.01, 'calibration_keithley03082022e_master_without_resistor_AFE_36_filter3.csv',
    #             SipmType.MASTER)
    # current_calibration_SiPM_master2(a_master_set_AFE_36, b_master_set_AFE_36, a_master_measured_AFE_36,
    #                                 b_master_measured_AFE_36, 3600, 48.3, 62.8, 0.5, 500, 12,
    #                                 'current_calibration_master_AFE_36_983MOhm_03082022f.csv')
    # current_calibration_SiPM_master2(a_master_set_AFE_36, b_master_set_AFE_36, a_master_measured_AFE_36,
    #                                 b_master_measured_AFE_36, 900, 48.3, 62.8, 0.5, 20, 12,
    #                                 'current_calibration_master_AFE_10.5MOhm_04082022a.csv')
    # calibration(600, 0, 4095, 64, 12, 0.01, 'calibration_keithley04082022b_slave_without_resistor_AFE_36_filter3.csv',
    #             SipmType.SLAVE)
    # current_calibration_SiPM_master2(a_slave_set_AFE_36, b_slave_set_AFE_36, a_slave_measured_AFE_36, Pomylka powinna być procedura pomiaru dla slave
    #                                  b_slave_measured_AFE_36, 1800, 48.3, 62.8, 0.5, 20, 12,
    #                                  'current_calibration_master_AFE_36_10.5MOhm_04082022c.csv')
    # current_calibration_SiPM_slave2(a_slave_set_AFE_36, b_slave_set_AFE_36, a_slave_measured_AFE_36,
    #                                  b_slave_measured_AFE_36, 1800, 48.3, 62.8, 0.5, 20, 12,
    #                                  'current_calibration_slave_AFE_36_10.5MOhm_04082022d.csv')
    # current_calibration_SiPM_slave2(a_slave_set_AFE_36, b_slave_set_AFE_36, a_slave_measured_AFE_36,
    #                                 b_slave_measured_AFE_36, 3600, 48.3, 62.8, 0.5, 500, 12,
    #                                 'current_calibration_slave_AFE_36_983MOhm_04082022e.csv')
    # calibration(1800, 0, 4095, 64, 12, 0.01, 'calibration_keithley05082022a_master_without_resistor_AFE_37_filter3.csv',
    #             SipmType.MASTER)
    # current_calibration_SiPM_master2(a_master_set_AFE_37, b_master_set_AFE_37, a_master_measured_AFE_37,
    #                                  b_master_measured_AFE_37, 900, 48.3, 62.8, 0.5, 100, 12,
    #                                  'current_calibration_master_AFE_37_983MOhm_05082022b.csv')
    # current_calibration_SiPM_master2(a_master_set_AFE_37, b_master_set_AFE_37, a_master_measured_AFE_37,
    #                                  b_master_measured_AFE_37, 900, 48.3, 62.8, 0.5, 20, 12,
    #                                  'current_calibration_master_AFE_37_10.5MOhm_05082022c.csv')
    # calibration(900, 0, 4095, 64, 12, 0.01, 'calibration_keithley05082022d_slave_without_resistor_AFE_37_filter3.csv',
    #             SipmType.SLAVE)
    # current_calibration_SiPM_slave2(a_slave_set_AFE_37, b_slave_set_AFE_37, a_slave_measured_AFE_37,
    #                                  b_slave_measured_AFE_37, 3600, 48.3, 62.8, 0.5, 500, 12,
    #                                  'current_calibration_slave_AFE_37_983MOhm_05082022e.csv')
    # current_calibration_SiPM_slave2(a_slave_set_AFE_37, b_slave_set_AFE_37, a_slave_measured_AFE_37,
    #                                  b_slave_measured_AFE_37, 1800, 48.3, 62.8, 0.5, 20, 12,
    #                                  'current_calibration_slave_AFE_37_10.5MOhm_09082022a.csv')
    # calibration(600, 0, 4095, 64, 12, 0.01, 'calibration_keithley09082022b_master_without_resistor_AFE_38_filter3.csv',
    #             SipmType.MASTER)
    # current_calibration_SiPM_master2(a_master_set_AFE_38, b_master_set_AFE_38, a_master_measured_AFE_38,
    #                                  b_master_measured_AFE_38, 900, 48.3, 62.8, 0.5, 100, 12,
    #                                  'current_calibration_master_AFE_38_983MOhm_10082022a.csv')
    # current_calibration_SiPM_master2(a_master_set_AFE_38, b_master_set_AFE_38, a_master_measured_AFE_38,
    #                                 b_master_measured_AFE_38, 600, 48.3, 62.8, 0.5, 20, 12,
    #                                 'current_calibration_master_AFE_10.5MOhm_10082022b.csv') W nazwie pliku zabrakło nr AFE - powinno być AFE 38
    # calibration(1800, 0, 4095, 64, 12, 0.01, 'calibration_keithley11082022a_slave_without_resistor_AFE_38_filter3.csv',
    #             SipmType.SLAVE)
    # current_calibration_SiPM_slave2(a_slave_set_AFE_38, b_slave_set_AFE_38, a_slave_measured_AFE_38,
    #                                  b_slave_measured_AFE_38, 1800, 48.3, 62.8, 0.5, 20, 12,
    #                                  'current_calibration_slave_AFE_38_10.5MOhm_11082022b.csv')
    # current_calibration_SiPM_slave2(a_slave_set_AFE_38, b_slave_set_AFE_38, a_slave_measured_AFE_38,
    #                                  b_slave_measured_AFE_38, 3600, 48.3, 62.8, 0.5, 500, 12,
    #                                  'current_calibration_slave_AFE_38_983MOhm_11082022c.csv'). Wyniki pomiaru odbiegają od pozostałych AFE
    # calibration(1800, 0, 4095, 64, 12, 0.01, 'calibration_keithley12082022a_master_without_resistor_AFE_39_filter3.csv',
    #             SipmType.MASTER)
    # current_calibration_SiPM_master2(a_master_set_AFE_39, b_master_set_AFE_39, a_master_measured_AFE_39,
    # b_master_measured_AFE_39, 900, 48.3, 62.8, 0.5, 100, 12,
    # 'current_calibration_master_AFE_39_983MOhm_12082022b.csv') #Pomiar przy współczynniku b_master_measured_AFE_39 = -1604 zamiast prawidłowej wartości -1.604
    # current_calibration_SiPM_master2(a_master_set_AFE_39, b_master_set_AFE_39, a_master_measured_AFE_39,
    #                                 b_master_measured_AFE_39, 1800, 48.3, 62.8, 0.5, 100, 12,
    #                                 'current_calibration_master_AFE_39_10.5MOhm_12082022c.csv')
    # current_calibration_SiPM_master2(a_master_set_AFE_39, b_master_set_AFE_39, a_master_measured_AFE_39,
    #                                  b_master_measured_AFE_39, 1800, 48.3, 62.8, 0.5, 100, 12,
    #                                  'current_calibration_master_AFE_39_983MOhm_16082022a_repeat.csv')
    # calibration(1800, 0, 4095, 64, 12, 0.01, 'calibration_keithley16082022b_slave_without_resistor_AFE_39_filter3.csv',
    #             SipmType.SLAVE)
    # current_calibration_SiPM_slave2(a_slave_set_AFE_39, b_slave_set_AFE_39, a_slave_measured_AFE_39, #zgubiony minus w parametrze b_slave_measured_AFE_39
    #                                  b_slave_measured_AFE_39, 1800, 48.3, 62.8, 0.5, 20, 12,
    #                                  'current_calibration_slave_AFE_39_10.5MOhm_17082022a.csv')
    # calibration(1800, 0, 4095, 64, 12, 0.01, 'calibration_keithley17082022b_slave_without_resistor_AFE_39_filter3_repeat.csv',
    # SipmType.SLAVE)
    # calibration(1800, 0, 4095, 64, 12, 0.01, 'calibration_keithley17082022c_slave_with_resistor_10.5MOhm_AFE_39_filter3_repeat.csv',
    #             SipmType.SLAVE)
    # current_calibration_SiPM_slave2(a_slave_set_AFE_39, b_slave_set_AFE_39, a_slave_measured_AFE_39,
    #                                  b_slave_measured_AFE_39, 1800, 48.3, 62.8, 0.5, 20, 12,
    #                                  'current_calibration_slave_AFE_39_10.5MOhm_17082022d.csv')
    # current_calibration_SiPM_slave2(a_slave_set_AFE_39, b_slave_set_AFE_39, a_slave_measured_AFE_39,
    #                                  b_slave_measured_AFE_39, 1800, 48.3, 62.8, 0.5, 100, 12,
    #                                  'current_calibration_slave_AFE_39_983MOhm_18082022a.csv')
    # current_calibration_SiPM_slave2(a_slave_set_AFE_38, b_slave_set_AFE_38, a_slave_measured_AFE_38,
    #                                  b_slave_measured_AFE_38, 1800, 48.3, 62.8, 0.5, 100, 12,
    #                                  'current_calibration_slave_AFE_38_983MOhm_18082022b.csv')
    # current_calibration_SiPM_slave2(a_slave_set_AFE_38, b_slave_set_AFE_38, a_slave_measured_AFE_38,
    #                                  b_slave_measured_AFE_38, 1800, 48.3, 62.8, 0.5, 20, 12,
    #                                  'current_calibration_slave_AFE_38_10.5MOhm_18082022c.csv')
    # current_calibration_SiPM_slave2(a_slave_set_AFE_38, b_slave_set_AFE_38, a_slave_measured_AFE_38,
    # b_slave_measured_AFE_38, 7200, 48.3, 62.8, 0.5, 500, 12,
    # 'current_calibration_slave_AFE_38_983MOhm_18082022d.csv')
    # breakdown_voltage_temp_master_time_dependence(1661155200, 1800, a_master_set_AFE_12, b_master_set_AFE_12,
    #                                           a_master_measured_AFE_12, b_master_measured_AFE_12, 48.3, 62.8, 700, 0.01, 10, 10, 12, "optimum_voltage_700_bit_temperature_master_time_dependence_72h_SiPM_AFE_12_19082022a.csv")
    # calibration(1800, 0, 4095, 64, 12, 0.01, 'calibration_keithley24082022a_master_without_resistor_AFE_33_filter3.csv',
    #             SipmType.MASTER)
    # current_calibration_SiPM_slave2(a_slave_set_AFE_12, b_slave_set_AFE_12, a_slave_measured_AFE_12,
    #                                  b_slave_measured_AFE_12, 1800, 48.3, 62.8, 0.1, 20, 12,
    #                                  'breakdown_voltage_slave_AFE_12_25082022a.csv')
    # current_calibration_SiPM_master2(a_master_set_AFE_33, b_master_set_AFE_33, a_master_measured_AFE_33,
    #                                  b_master_measured_AFE_33, 7200, 48.3, 62.8, 0.5, 500, 12,
    #                                  'current_calibration_master_AFE_33_983MOhm_26082022a.csv')

    # current_calibration_SiPM_master2(a_master_set_AFE_33, b_master_set_AFE_33, a_master_measured_AFE_33, # pomiar z opornikiem 400MOhma - Sasza ustawił zły opornik
    # b_master_measured_AFE_33, 1800, 48.3, 62.8, 0.5, 20, 12,
    # 'current_calibration_master_AFE_33_10.5MOhm_29082022a.csv')

    # current_calibration_SiPM_master2(a_master_set_AFE_33, b_master_set_AFE_33, a_master_measured_AFE_33, # ponowny pomiar, już z poprawnym opornikiem
    #                                  b_master_measured_AFE_33, 1800, 48.3, 62.8, 0.5, 20, 12,
    #                                  'current_calibration_master_AFE_33_10.5MOhm_29082022b.csv')
    # calibration(1800, 0, 4095, 64, 12, 0.01, 'calibration_keithley29082022c_slave_without_resistor_AFE_33_filter3.csv',  #pomiary Keithleyem sa bez sensu, cos zostalo zle podlaczone
    #             SipmType.SLAVE)
    # calibration(1800, 0, 4095, 64, 12, 0.01, 'calibration_keithley29082022d_slave_without_resistor_AFE_33_filter3.csv',
    #             SipmType.SLAVE)
    # current_calibration_SiPM_slave2(a_slave_set_AFE_33, b_slave_set_AFE_33, a_slave_measured_AFE_33,
    #                                  b_slave_measured_AFE_33, 1800, 48.3, 62.8, 0.5, 20, 12,
    #                                  'current_calibration_slave_AFE_33_10.5MOhm_30082022a.csv')
    # current_calibration_SiPM_slave2(a_slave_set_AFE_33, b_slave_set_AFE_33, a_slave_measured_AFE_33,
    #                                  b_slave_measured_AFE_33, 7200, 48.3, 62.8, 0.5, 500, 12,
    #                                  'current_calibration_slave_AFE_33_983MOhm_30082022b.csv')
    # calibration(1800, 0, 4095, 64, 12, 0.01, 'calibration_keithley08092022a_master_without_resistor_AFE_11_nowe_filter3.csv',
    #             SipmType.MASTER)
    # current_calibration_SiPM_master2(a_master_set_AFE_11_nowe, b_master_set_AFE_11_nowe, a_master_measured_AFE_11_nowe,
    #                                  b_master_measured_AFE_11_nowe, 7200, 48.3, 62.8, 0.5, 500, 12,
    #                                  'current_calibration_master_AFE_11_nowe_983MOhm_09092022a.csv')
    # current_calibration_SiPM_master2(a_master_set_AFE_11_nowe, b_master_set_AFE_11_nowe, a_master_measured_AFE_11_nowe,
    #                                  b_master_measured_AFE_11_nowe, 1800, 48.3, 62.8, 0.5, 20, 12,
    #                                  'current_calibration_master_AFE_11_new_10MOhm_13092022a.csv')
    # stability_only_AFE_temp(1663069200, 900, "temperature_test_AFE_11_new_SiPM_slave_13092022b.csv")
    # stability_only_AFE_temp(1663072620, 300, "temperature_test_AFE_11_new_SiPM_slave_13092022c.csv")
    # stability_only_AFE_temp(1663073851, 120, "temperature_test_AFE_11_new_SiPM_slave_13092022d.csv")
    # stability_only_AFE_temp(1663075722, 120, "temperature_test_AFE_11_new_SiPM_slave_13092022e.csv")
    # stability_only_AFE_temp(1663076896, 120, "temperature_test_AFE_11_new_SiPM_slave_13092022f.csv")
    # stability_only_AFE_temp(1663139437, 900, "temperature_test_AFE_11_new_SiPM_slave_14092022a.csv")
    # calibration(1800, 0, 4095, 64, 12, 0.01, 'calibration_keithley14092022b_slave_without_resistor_AFE_11_new_filter3.csv',
    #             SipmType.SLAVE)
    # current_calibration_SiPM_slave2(a_slave_set_AFE_11_new, b_slave_set_AFE_11_new, a_slave_measured_AFE_11_new,
    #                                 b_slave_measured_AFE_11_new, 1800, 48.3, 62.8, 0.5, 20, 12,
    #                                 'current_calibration_slave_AFE_11_new_10.5MOhm_14092022a.csv') # Pomylka w nazwie - powinna koczyc sie literka c
    # current_calibration_SiPM_slave2(a_slave_set_AFE_11_new, b_slave_set_AFE_11_new, a_slave_measured_AFE_11_new,
    #                                  b_slave_measured_AFE_11_new, 7200, 48.3, 62.8, 0.5, 500, 12,
    #                                  'current_calibration_slave_AFE_11_new_983MOhm_14092022d.csv')
    # stability_only_AFE_temp(1663228664, 120, "temperature_test_AFE_14_new_SiPM_slave_15092022a.csv")
    # calibration(1800, 0, 4095, 64, 12, 0.01, 'calibration_keithley15092022b_master_without_resistor_AFE_14_new_filter3.csv',
    #             SipmType.MASTER)
    # stability_only_AFE_temp(1663234070, 120, "temperature_test_AFE_14_new_SiPM_slave_15092022b.csv")

    # stability_only_AFE_temp_on(1663260409, 120, "temperature_test_AFE_14_new_SiPM_slave_15092022c.csv")

    # calibration(1800, 0, 4095, 64, 12, 0.01, 'calibration_keithley15092022c_slave_without_resistor_AFE_14_new_filter3.csv',
    #             SipmType.SLAVE)  #Nieudany pomiar - Keithley nie mierzył - prawdopodobnie był ustawiony na zero-check

    # calibration(1800, 0, 4095, 64, 12, 0.01, 'calibration_keithley15092022d_slave_without_resistor_AFE_14_new_filter3_repeat.csv',
    #             SipmType.SLAVE)

    # current_calibration_SiPM_slave2(a_slave_set_AFE_14_new, b_slave_set_AFE_14_new, a_slave_measured_AFE_14_new,
    #                                  b_slave_measured_AFE_14_new, 1800, 48.3, 62.8, 0.5, 20, 12,
    #                                  'current_calibration_slave_AFE_14_new_10.5MOhm_16092022a.csv')

    # current_calibration_SiPM_slave2(a_slave_set_AFE_14_new, b_slave_set_AFE_14_new, a_slave_measured_AFE_14_new,
    #                                  b_slave_measured_AFE_14_new, 1800, 48.3, 62.8, 0.5, 100, 12,
    #                                  'current_calibration_slave_AFE_14_new_983MOhm_16092022b.csv')

    # current_calibration_SiPM_master2(a_master_set_AFE_14_new, b_master_set_AFE_14_new, a_master_measured_AFE_14_new,
    #                                  b_master_measured_AFE_14_new, 1800, 48.3, 62.8, 0.5, 20, 12,
    #                                  'current_calibration_master_AFE_14_new_10.5MOhm_15092022c.csv')

    # current_calibration_SiPM_master2(a_master_set_AFE_14_new, b_master_set_AFE_14_new, a_master_measured_AFE_14_new,
    #                                  b_master_measured_AFE_14_new, 1800, 48.3, 62.8, 0.5, 100, 12,
    #                                  'current_calibration_master_AFE_14_new_983MOhm_15092022d.csv')
    # calibration(1800, 0, 4095, 64, 12, 0.01, 'calibration_keithley20092022a_master_without_resistor_AFE_16_new_filter3.csv',
    #             SipmType.MASTER)
    # current_calibration_SiPM_master2(a_master_set_AFE_16_new, b_master_set_AFE_16_new, a_master_measured_AFE_16_new,
    #                                  b_master_measured_AFE_16_new, 1800, 48.3, 62.8, 0.5, 20, 12,
    #                                  'current_calibration_master_AFE_16_new_10.5MOhm_20092022b.csv')
    # current_calibration_SiPM_master2(a_master_set_AFE_16_new, b_master_set_AFE_16_new, a_master_measured_AFE_16_new,
    #                                  b_master_measured_AFE_16_new, 1800, 48.3, 62.8, 0.5, 100, 12,
    #                                  'current_calibration_master_AFE_16_new_983MOhm_20092022c.csv')

    # calibration(1800, 0, 4095, 64, 12, 0.01, 'calibration_keithley20092022d_slave_without_resistor_AFE_16_new_filter3.csv',
    #             SipmType.SLAVE)

    # current_calibration_SiPM_slave2(a_slave_set_AFE_16_new, b_slave_set_AFE_16_new, a_slave_measured_AFE_16_new,
    #                                  b_slave_measured_AFE_16_new, 1800, 48.3, 62.8, 0.5, 20, 12,
    #                                  'current_calibration_slave_AFE_16_new_10.5MOhm_21092022a.csv')

    # current_calibration_SiPM_slave2(a_slave_set_AFE_16_new, b_slave_set_AFE_16_new, a_slave_measured_AFE_16_new,
    #                                  b_slave_measured_AFE_16_new, 1800, 48.3, 62.8, 0.5, 100, 12,
    #                                  'current_calibration_slave_AFE_16_new_983MOhm_21092022a.csv')
    # calibration(1800, 0, 4095, 64, 12, 0.01, 'calibration_keithley21092022c_master_without_resistor_AFE_15_new_filter3.csv',
    #             SipmType.MASTER)
    # current_calibration_SiPM_master2(a_master_set_AFE_15_new, b_master_set_AFE_15_new, a_master_measured_AFE_15_new,
    #                                  b_master_measured_AFE_15_new, 7200, 48.3, 62.8, 0.5, 1000, 12,
    #                                  'current_calibration_master_AFE_15_new_983MOhm_21092022d.csv')
    # current_calibration_SiPM_master2(a_master_set_AFE_15_new, b_master_set_AFE_15_new, a_master_measured_AFE_15_new,
    #                                  b_master_measured_AFE_15_new, 1800, 48.3, 62.8, 0.5, 20, 12,
    #                                  'current_calibration_master_AFE_15_new_10.5MOhm_22092022a.csv')
    # calibration(1800, 0, 4095, 64, 12, 0.01, 'calibration_keithley22092022a_slave_without_resistor_AFE_15_new_filter3.csv',
    #             SipmType.SLAVE)

    # current_calibration_SiPM_slave2(a_slave_set_AFE_15_new, b_slave_set_AFE_15_new, a_slave_measured_AFE_15_new,
    #                                  b_slave_measured_AFE_15_new, 1800, 48.3, 62.8, 0.5, 20, 12,
    #                                  'current_calibration_slave_AFE_15_new_10.5MOhm_22092022b.csv')

    # current_calibration_SiPM_slave2(a_slave_set_AFE_15_new, b_slave_set_AFE_15_new, a_slave_measured_AFE_15_new,
    #                                  b_slave_measured_AFE_15_new, 7200, 48.3, 62.8, 0.5, 1000, 12,
    #                                  'current_calibration_slave_AFE_15_new_983MOhm_22092022c.csv')
    # calibration(1800, 0, 4095, 64, 12, 0.01, 'calibration_keithley23092022a_master_without_resistor_AFE_12_new_filter3.csv',
    #             SipmType.MASTER)
    # current_calibration_SiPM_master2(a_master_set_AFE_12_new, b_master_set_AFE_12_new, a_master_measured_AFE_12_new,
    #                                  b_master_measured_AFE_12_new, 1800, 48.3, 62.8, 0.5, 20, 12,
    #                                  'current_calibration_master_AFE_12_new_10.5MOhm_23092022b.csv')

    # current_calibration_SiPM_master2(a_master_set_AFE_12_new, b_master_set_AFE_12_new, a_master_measured_AFE_12_new,
    #                                  b_master_measured_AFE_12_new, 7200, 48.3, 62.8, 0.5, 1000, 12,
    #                                  'current_calibration_master_AFE_12_new_983MOhm_23092022c.csv')
    # calibration(1800, 0, 4095, 64, 12, 0.01, 'calibration_keithley27092022a_slave_without_resistor_AFE_12_new_filter3.csv',
    #             SipmType.SLAVE)

    # current_calibration_SiPM_slave2(a_slave_set_AFE_12_new, b_slave_set_AFE_12_new, a_slave_measured_AFE_12_new,
    #                                  b_slave_measured_AFE_12_new, 1800, 48.3, 62.8, 0.5, 20, 12,
    #                                  'current_calibration_slave_AFE_12_new_10.5MOhm_27092022b.csv')

    # current_calibration_SiPM_slave2(a_slave_set_AFE_12_new, b_slave_set_AFE_12_new, a_slave_measured_AFE_12_new,
    # b_slave_measured_AFE_12_new, 7200, 48.3, 62.8, 0.5, 1000, 12,
    # 'current_calibration_slave_AFE_15_new_983MOhm_27092022c.csv') # pomylka w nazwie - powinno być *AFE_12*, zmieniono nazwę pliku na poprawną

    # calibration(1800, 0, 4095, 64, 12, 0.01, 'calibration_keithley28092022a_master_without_resistor_AFE_17_new_filter3.csv',
    #             SipmType.MASTER)

    # current_calibration_SiPM_master2(a_master_set_AFE_17_new, b_master_set_AFE_17_new, a_master_measured_AFE_17_new,
    #                                  b_master_measured_AFE_17_new, 1800, 48.3, 62.8, 0.5, 20, 12,
    #                                  'current_calibration_master_AFE_17_new_10.5MOhm_28092022b.csv')

    # current_calibration_SiPM_master2(a_master_set_AFE_17_new, b_master_set_AFE_17_new, a_master_measured_AFE_17_new,
    #                                  b_master_measured_AFE_17_new, 7200, 48.3, 62.8, 0.5, 1000, 12,
    #                                  'current_calibration_master_AFE_17_new_983MOhm_28092022c.csv')

    # calibration(1800, 0, 4095, 64, 12, 0.01, 'calibration_keithley29092022a_slave_without_resistor_AFE_17_new_filter3.csv',
    #             SipmType.SLAVE)

    # current_calibration_SiPM_slave2(a_slave_set_AFE_17_new, b_slave_set_AFE_17_new, a_slave_measured_AFE_17_new,
    #                                 b_slave_measured_AFE_17_new, 1800, 48.3, 62.8, 0.5, 20, 12,
    #                                 'current_calibration_slave_AFE_17_new_10.5MOhm_29092022a.csv')

    # stability_temp_keithley(1664517600, 60, 0.01, 'keithley_stability_temp_29092022')

    # current_calibration_SiPM_slave2(a_slave_set_AFE_17_new, b_slave_set_AFE_17_new, a_slave_measured_AFE_17_new,
    #                                  b_slave_measured_AFE_17_new, 7200, 48.3, 62.8, 0.5, 1000, 12,
    #                                  'current_calibration_slave_AFE_17_new_983MOhm_29092022c.csv')

    # calibration(1800, 0, 4095, 64, 12, 0.01, 'calibration_keithley30092022a_master_without_resistor_AFE_13_new_filter3.csv',
    #             SipmType.MASTER)

    # current_calibration_SiPM_master2(a_master_set_AFE_13_new, b_master_set_AFE_13_new, a_master_measured_AFE_13_new,
    #                                  b_master_measured_AFE_13_new, 7200, 48.3, 62.8, 0.5, 1000, 12,
    #                                  'current_calibration_master_AFE_13_new_983MOhm_30092022b.csv')

    # current_calibration_SiPM_master2(a_master_set_AFE_13_new, b_master_set_AFE_13_new, a_master_measured_AFE_13_new,
    #                                  b_master_measured_AFE_13_new, 1800, 48.3, 62.8, 0.5, 20, 12,
    #                                  'current_calibration_master_AFE_13_new_10.5MOhm_04102022a.csv')

    # calibration(1800, 0, 4095, 64, 12, 0.01, 'calibration_keithley04102022b_slave_without_resistor_AFE_13_new_filter3.csv',
    #             SipmType.SLAVE)

    # current_calibration_SiPM_slave2(a_slave_set_AFE_13_new, b_slave_set_AFE_13_new, a_slave_measured_AFE_13_new,
    #                                 b_slave_measured_AFE_13_new, 1800, 48.3, 62.8, 0.5, 20, 12,
    #                                 'current_calibration_slave_AFE_13_new_10.5MOhm_04102022c.csv')

    # current_calibration_SiPM_slave2(a_slave_set_AFE_13_new, b_slave_set_AFE_13_new, a_slave_measured_AFE_13_new,
    #                                 b_slave_measured_AFE_13_new, 7200, 48.3, 62.8, 0.5, 1000, 12,
    #                                 'current_calibration_slave_AFE_13_new_983MOhm_04102022d.csv')

    # calibration(1800, 0, 4095, 64, 12, 0.01, 'calibration_keithley05102022a_master_without_resistor_AFE_18_new_filter3.csv',
    #             SipmType.MASTER)

    # current_calibration_SiPM_master2(a_master_set_AFE_18_new, b_master_set_AFE_18_new, a_master_measured_AFE_18_new,
    # b_master_measured_AFE_18_new, 1800, 48.3, 62.8, 0.5, 20, 12,
    # 'current_calibration_master_AFE_13_new_10.5MOhm_05102022b.csv') # przez pomylke wlozylem opornik 983 MOhmy zamiast 10.5 MOhm i blednie oznaczylem plik
    # po zmianie nazwa pliku to: "current_calibration_master_AFE_18_new_983MOhm_05102022b_poprawiana_nazwa.csv"

    # current_calibration_SiPM_master2(a_master_set_AFE_18_new, b_master_set_AFE_18_new, a_master_measured_AFE_18_new,
    #                                  b_master_measured_AFE_18_new, 7200, 48.3, 62.8, 0.5, 1000, 12,
    #                                  'current_calibration_master_AFE_18_new_983MOhm_05102022c.csv')

    # current_calibration_SiPM_master2(a_master_set_AFE_18_new, b_master_set_AFE_18_new, a_master_measured_AFE_18_new,
    #                                  b_master_measured_AFE_18_new, 1800, 48.3, 62.8, 0.5, 20, 12,
    #                                  'current_calibration_master_AFE_18_new_10.5MOhm_06102022a.csv')

    # calibration(1800, 0, 4095, 64, 12, 0.01, 'calibration_keithley06102022b_slave_without_resistor_AFE_18_new_filter3.csv',
    #             SipmType.SLAVE)

    # current_calibration_SiPM_slave2(a_slave_set_AFE_18_new, b_slave_set_AFE_18_new, a_slave_measured_AFE_18_new,
    #                                 b_slave_measured_AFE_18_new, 1800, 48.3, 62.8, 0.5, 20, 12,
    #                                 'current_calibration_slave_AFE_18_new_10.5MOhm_07102022a.csv')

    # current_calibration_SiPM_slave2(a_slave_set_AFE_18_new, b_slave_set_AFE_18_new, a_slave_measured_AFE_18_new,
    #                                 b_slave_measured_AFE_18_new, 7200, 48.3, 62.8, 0.5, 1000, 12,
    #                                 'current_calibration_slave_AFE_18_new_983MOhm_07102022b.csv')
    # stability_temp_keithley(1668593700, 60, 0.01, 'keithley_stability_temp_16112022')
    # current_voltage_dependence_master(a_master_set_AFE_12, b_master_set_AFE_12, a_master_measured_AFE_12, b_master_measured_AFE_12,
    #                                   1800, 48.3, 62.8, 0.1, 20, 12, 'current_voltage_dependence_SiPM_0150_16112022a')
    # breakdown_voltage_determination_master_temp_keithley2_alone(a_master_set_AFE_12, b_master_set_AFE_12, a_master_measured_AFE_12,
    #                                        b_master_measured_AFE_12, 1800, 48.3, 62.8, 20, 0.01, 20, 12,
    #                                       "breakdown_voltage_determination_master_temp_AFE_12_SiPM_0150_16112022b.csv")
    # current_voltage_dependence_master(a_master_set_AFE_12, b_master_set_AFE_12, a_master_measured_AFE_12, b_master_measured_AFE_12,
    #                                   7200, 48.3, 62.8, 0.1, 20, 12, 'current_voltage_dependence_SiPM_0150_16112022c')
    # current_voltage_dependence_master(a_master_set_AFE_12, b_master_set_AFE_12, a_master_measured_AFE_12, b_master_measured_AFE_12,
    # 1800, 48.3, 62.8, 0.1, 20, 12, 'current_voltage_dependence_SiPM_0150_17112022a')

    # calibration(1800, 0, 4095, 64, 12, 0.01, 'calibration_keithley17112022a_master_without_resistor_AFE_12_old_filter3.csv',
    #             SipmType.MASTER)

    # current_calibration_SiPM_master2(a_master_set_AFE_12_again, b_master_set_AFE_12_again, a_master_measured_AFE_12_again,
    #                                  b_master_measured_AFE_12_again, 1800, 48.3, 62.8, 0.5, 20, 12,
    #                                  'current_calibration_master_AFE_12_again_10.5MOhm_17112022c.csv')

    # current_calibration_SiPM_master2(a_master_set_AFE_12_again, b_master_set_AFE_12_again, a_master_measured_AFE_12_again,
    #                                  b_master_measured_AFE_12_again, 7200, 48.3, 62.8, 0.5, 1000, 12,
    #                                  'current_calibration_master_AFE_12_again_478MOhm_17112022d.csv')

    # current_calibration_SiPM_master2(a_master_set_AFE_12_again, b_master_set_AFE_12_again, a_master_measured_AFE_12_again,
    #                                  b_master_measured_AFE_12_again, 1800, 48.3, 62.8, 0.5, 20, 12,
    #                                  'current_calibration_master_AFE_12_again_6.44MOhm_22112022a.csv')

    # current_calibration_SiPM_master2(a_master_set_AFE_12_again, b_master_set_AFE_12_again, a_master_measured_AFE_12_again,
    #                                  b_master_measured_AFE_12_again, 1800, 48.3, 62.8, 0.5, 20, 12,
    #                                  'current_calibration_master_AFE_12_again_15.37MOhm_22112022b.csv')

    # current_voltage_dependence_master(a_master_set_AFE_12_again, b_master_set_AFE_12_again, a_master_measured_AFE_12_again, b_master_measured_AFE_12_again,
    #                                   180, 48.3, 62.8, 0.1, 20, 12, 'current_voltage_dependence_SiPM_0150_24112022b')
    # stability_temp3(1669645843, 10, 0.1, 60.0, 0, 'test_stability28112022a.csv')
    # stability_temp3(1669647643, 10, 0.1, 60.0, 0, 'test_stability28112022b.csv')
    # current_voltage_dependence_master(a_master_set_AFE_12_again, b_master_set_AFE_12_again, a_master_measured_AFE_12_again, b_master_measured_AFE_12_again,
    #                                   300, 52.0, 60.0, 0.1, 20, 12, 'current_voltage_dependence_SiPM_0150_28112022c')
    # current_voltage_dependence_master(a_master_set_AFE_12_again, b_master_set_AFE_12_again, a_master_measured_AFE_12_again, b_master_measured_AFE_12_again,
    # 300, 52.0, 60.0, 0.1, 20, 12, 'current_voltage_dependence_SiPM_0150_28112022d')
    # current_voltage_dependence_master(a_master_set_AFE_12_again, b_master_set_AFE_12_again, a_master_measured_AFE_12_again, b_master_measured_AFE_12_again,
    # 300, 52.0, 60.0, 0.1, 20, 12, 'current_voltage_dependence_SiPM_0150_28112022e')
    # current_voltage_dependence_master(a_master_set_AFE_12_again, b_master_set_AFE_12_again, a_master_measured_AFE_12_again, b_master_measured_AFE_12_again,
    #                                   300, 52.0, 60.0, 0.1, 20, 12, 'current_voltage_dependence_SiPM_0150_29112022a')
    # current_calibration_SiPM_master2(a_master_set_AFE_12_again, b_master_set_AFE_12_again, a_master_measured_AFE_12_again,
    #                                  b_master_measured_AFE_12_again, 180, 48.3, 62.8, 0.5, 1000, 12,
    #                                  'current_calibration_master_AFE_12_again_478MOhm_29112022a_test.csv')
    # current_calibration_SiPM_master2all(a_master_set_AFE_12_again, b_master_set_AFE_12_again, a_master_measured_AFE_12_again,
    #                                  b_master_measured_AFE_12_again, 180, 48.5, 50.0, 0.5, 10, 12,
    #                                  'current_calibration_master_AFE_12_again_478MOhm_30112022a_test0.csv')
    # current_calibration_SiPM_master2all(a_master_set_AFE_12_again, b_master_set_AFE_12_again, a_master_measured_AFE_12_again,
    #                                  b_master_measured_AFE_12_again, 180, 49, 61, 6, 1000, 60,
    #                                  'current_calibration_master_AFE_12_again_478MOhm_30112022a_test1.csv')
    # current_calibration_SiPM_slave2all(a_slave_set_AFE_12, b_slave_set_AFE_12, a_slave_measured_AFE_12,
    #                                  b_slave_measured_AFE_12, 180, 48.5, 50.0, 0.5, 10, 12,
    #                                  'current_calibration_slave_AFE_12_again_478MOhm_30112022a_test2.csv')
    # current_calibration_SiPM_slave2all(a_slave_set_AFE_12, b_slave_set_AFE_12, a_slave_measured_AFE_12,
    #                                  b_slave_measured_AFE_12,  7200, 48.3, 62.8, 0.5, 1000, 12,
    #                                  'current_calibration_slave_AFE_12_478MOhm_30112022a_test3')
    # current_calibration_SiPM_master2all(a_slave_set_AFE_12, b_slave_set_AFE_12, a_slave_measured_AFE_12,
    #                                     b_slave_measured_AFE_12, 180, 49, 61, 6, 1000, 60,
    #                                     'current_calibration_master_AFE_12_again_145MOhm_01122022a_test1.csv')
    # current_calibration_SiPM_slave2all(a_slave_set_AFE_12, b_slave_set_AFE_12, a_slave_measured_AFE_12,
                                       # b_slave_measured_AFE_12, 7200, 48.3, 62.8, 0.5, 1000, 12,
                                       # 'current_calibration_slave_AFE_12_again_145MOhm_01122022b_test2.csv')
    # current_voltage_dependence_slave(a_slave_set_AFE_12, b_slave_set_AFE_12, a_slave_measured_AFE_12,
    #                                  b_slave_measured_AFE_12, 1800, 52.0, 60.0, 0.1, 20, 12,
    #                                  'current_voltage_dependence_SiPM_0150_04012023a')
    # current_voltage_dependence_slave(a_slave_set_AFE_12, b_slave_set_AFE_12, a_slave_measured_AFE_12,
    #                                  b_slave_measured_AFE_12, 3600, 52.0, 60.0, 0.1, 20, 12,
    #                                  'current_voltage_dependence_SiPM_0150_20C_04012023b') nieudany pomiar - polaczenie sie zresetowalo
    # current_voltage_dependence_slave(a_slave_set_AFE_12, b_slave_set_AFE_12, a_slave_measured_AFE_12,
    #                                  b_slave_measured_AFE_12, 1800, 52.0, 60.0, 0.1, 20, 12,
    #                                  'current_voltage_dependence_SiPM_0150_20C_05012023a')
    # current_voltage_dependence_slave(a_slave_set_AFE_12, b_slave_set_AFE_12, a_slave_measured_AFE_12,
    #                                  b_slave_measured_AFE_12, 600, 52.0, 60.0, 0.1, 20, 12,
    #                                  'current_voltage_dependence_SiPM_0150_30C_05012023a')
    # current_voltage_dependence_slave(a_slave_set_AFE_12, b_slave_set_AFE_12, a_slave_measured_AFE_12,
    #                                  b_slave_measured_AFE_12, 1800, 52.0, 60.0, 0.1, 20, 12,
    #                                  'current_voltage_dependence_SiPM_0110_30C_05012023c')
    # current_voltage_dependence_slave(a_slave_set_AFE_12, b_slave_set_AFE_12, a_slave_measured_AFE_12,
    #                                  b_slave_measured_AFE_12, 14400, 52.0, 60.0, 0.1, 20, 12,
    #                                  'current_voltage_dependence_SiPM_0110_25C_09012023a') Nieudany pomiar - poczekało 4 h i połączenie się zresetowało
    #current_voltage_dependence_slave(a_slave_set_AFE_12, b_slave_set_AFE_12, a_slave_measured_AFE_12,
    #                                b_slave_measured_AFE_12, 600, 52.0, 60.0, 0.1, 20, 12,
    #                                 'current_voltage_dependence_SiPM_0110_25C_09012023b')
    #current_voltage_dependence_slave(a_slave_set_AFE_12, b_slave_set_AFE_12, a_slave_measured_AFE_12,
    #                                b_slave_measured_AFE_12, 300, 52.0, 60.0, 0.1, 20, 12,
    #                                 'current_voltage_dependence_SiPM_0110_20C_10012023a')
    #current_voltage_dependence_slave(a_slave_set_AFE_12, b_slave_set_AFE_12, a_slave_measured_AFE_12,
    #                                 b_slave_measured_AFE_12, 300, 52.0, 60.0, 0.1, 20, 12,
    #                                 'current_voltage_dependence_SiPM_0134_20C_10012023a')
    # current_voltage_dependence_slave(a_slave_set_AFE_12, b_slave_set_AFE_12, a_slave_measured_AFE_12,
    #                                  b_slave_measured_AFE_12, 600, 52.0, 60.0, 0.1, 20, 12,
    #                                  'current_voltage_dependence_SiPM_0134_25C_10012023a')
    #current_voltage_dependence_slave(a_slave_set_AFE_12, b_slave_set_AFE_12, a_slave_measured_AFE_12,
    #                                 b_slave_measured_AFE_12, 7200, 52.0, 60.0, 0.1, 20, 12,
    #                                 'current_voltage_dependence_SiPM_0134_30C_10012023b')
    # current_voltage_dependence_slave(a_slave_set_AFE_12, b_slave_set_AFE_12, a_slave_measured_AFE_12,
    #                                  b_slave_measured_AFE_12, 600, 52.0, 60.0, 0.1, 20, 12,
    #                                  'current_voltage_dependence_SiPM_0181_30C_11012023a')
    # current_voltage_dependence_slave(a_slave_set_AFE_12, b_slave_set_AFE_12, a_slave_measured_AFE_12,
    #                                  b_slave_measured_AFE_12, 600, 52.0, 60.0, 0.1, 20, 12,
    #                                  'current_voltage_dependence_SiPM_0181_25C_11012023b')
    #current_voltage_dependence_slave(a_slave_set_AFE_12, b_slave_set_AFE_12, a_slave_measured_AFE_12,
    #                                 b_slave_measured_AFE_12, 600, 52.0, 60.0, 0.1, 20, 12,
    #                                 'current_voltage_dependence_SiPM_0181_20C_11012023c')
    #current_voltage_dependence_slave(a_slave_set_AFE_12, b_slave_set_AFE_12, a_slave_measured_AFE_12,
    #                                 b_slave_measured_AFE_12, 600, 52.0, 60.0, 0.1, 20, 12,
    #                                 'current_voltage_dependence_SiPM_0137_20C_12012023a')
    # current_voltage_dependence_slave(a_slave_set_AFE_12, b_slave_set_AFE_12, a_slave_measured_AFE_12,
    #                                  b_slave_measured_AFE_12, 600, 52.0, 60.0, 0.1, 20, 12,
    #                                  'current_voltage_dependence_SiPM_0137_25C_12012023b')
    #current_voltage_dependence_slave(a_slave_set_AFE_12, b_slave_set_AFE_12, a_slave_measured_AFE_12,
    #                                 b_slave_measured_AFE_12, 600, 52.0, 60.0, 0.1, 20, 12,
    #                                 'current_voltage_dependence_SiPM_0137_30C_12012023c')
    #repeat for 0134 30C
    #current_voltage_dependence_slave(a_slave_set_AFE_12, b_slave_set_AFE_12, a_slave_measured_AFE_12,
    #                                 b_slave_measured_AFE_12, 1200, 52.0, 60.0, 0.1, 20, 12,
    #                                 'current_voltage_dependence_SiPM_0134_30C_13012023a')
    # current_voltage_dependence_slave(a_slave_set_AFE_12, b_slave_set_AFE_12, a_slave_measured_AFE_12,
    #                                  b_slave_measured_AFE_12, 600, 52.0, 60.0, 0.1, 20, 12,
    #                                  'current_voltage_dependence_SiPM_0145_30C_13012023b')
    # current_voltage_dependence_slave(a_slave_set_AFE_12, b_slave_set_AFE_12, a_slave_measured_AFE_12,
    #                                  b_slave_measured_AFE_12, 600, 52.0, 60.0, 0.1, 20, 12,
    #                                  'current_voltage_dependence_SiPM_0145_25C_14012023a')
    #current_voltage_dependence_slave(a_slave_set_AFE_12, b_slave_set_AFE_12, a_slave_measured_AFE_12,
    #                                 b_slave_measured_AFE_12, 600, 49.0, 62.0, 0.1, 20, 12,
    #                                 'current_voltage_dependence_SiPM_0145_20C_14012023b')
    # current_voltage_dependence_slave(a_slave_set_AFE_12, b_slave_set_AFE_12, a_slave_measured_AFE_12,
    #                                  b_slave_measured_AFE_12, 600, 49.0, 62.0, 0.1, 20, 12,
    #                                  'current_voltage_dependence_SiPM_0107_20C_16012023a')
    # current_voltage_dependence_slave(a_slave_set_AFE_12, b_slave_set_AFE_12, a_slave_measured_AFE_12,
    #                                  b_slave_measured_AFE_12, 600, 49.0, 62.0, 0.1, 20, 12,
    #                                  'current_voltage_dependence_SiPM_0107_25C_16012023b')
    # current_voltage_dependence_slave(a_slave_set_AFE_12, b_slave_set_AFE_12, a_slave_measured_AFE_12,
    #                                  b_slave_measured_AFE_12, 600, 49.0, 62.0, 0.1, 20, 12,
    #                                  'current_voltage_dependence_SiPM_0107_30C_17012023a')
    # current_voltage_dependence_slave2(a_slave_set_AFE_12, b_slave_set_AFE_12, a_slave_measured_AFE_12,
    #                                  b_slave_measured_AFE_12, 300, 49.0, 49.5, 0.1, 20, 12,
    #                                  'test_current_voltage_dependence_slave2_v2')
    # current_voltage_dependence_slave2(a_slave_set_AFE_12, b_slave_set_AFE_12, a_slave_measured_AFE_12,
                                     # b_slave_measured_AFE_12, 600, 49.0, 62.0, 0.1, 20, 12,
                                     # 'current_voltage_dependence_SiPM_0101_30C_17012023b')
    # current_voltage_dependence_slave2(a_slave_set_AFE_12, b_slave_set_AFE_12, a_slave_measured_AFE_12,
    #                                  b_slave_measured_AFE_12, 600, 49.0, 62.0, 0.1, 20, 12,
    #                                  'current_voltage_dependence_SiPM_0101_25C_18012023a')
    # current_voltage_dependence_slave2(a_slave_set_AFE_12, b_slave_set_AFE_12, a_slave_measured_AFE_12,
    #                                  b_slave_measured_AFE_12, 600, 49.0, 62.0, 0.1, 20, 12,
    #                                  'current_voltage_dependence_SiPM_0101_20C_18012023b')
    #current_voltage_dependence_slave2(a_slave_set_AFE_12, b_slave_set_AFE_12, a_slave_measured_AFE_12,
    #                                  b_slave_measured_AFE_12, 600, 49.0, 62.0, 0.1, 20, 12,
    #                                  'current_voltage_dependence_SiPM_0205_20C_18012023c')
    # current_voltage_dependence_slave2(a_slave_set_AFE_12, b_slave_set_AFE_12, a_slave_measured_AFE_12,
    #                                   b_slave_measured_AFE_12, 600, 49.0, 62.0, 0.1, 20, 12,
    #                                   'current_voltage_dependence_SiPM_0205_25C_18012023d')
    #current_voltage_dependence_slave2(a_slave_set_AFE_12, b_slave_set_AFE_12, a_slave_measured_AFE_12,
    #                                  b_slave_measured_AFE_12, 600, 49.0, 62.0, 0.1, 20, 12,
    #                                  'current_voltage_dependence_SiPM_0205_30C_19012023a')
    #current_voltage_dependence_slave2(a_slave_set_AFE_12, b_slave_set_AFE_12, a_slave_measured_AFE_12,
    #                                  b_slave_measured_AFE_12, 600, 49.0, 62.0, 0.1, 20, 12,
    #                                  'current_voltage_dependence_SiPM_0139_30C_19012023a')
    # current_voltage_dependence_slave2(a_slave_set_AFE_12, b_slave_set_AFE_12, a_slave_measured_AFE_12,
    #                                   b_slave_measured_AFE_12, 600, 49.0, 62.0, 0.1, 20, 12,
    #                                   'current_voltage_dependence_SiPM_0139_25C_19012023a')
    # current_voltage_dependence_slave2(a_slave_set_AFE_12, b_slave_set_AFE_12, a_slave_measured_AFE_12,
    #                                   b_slave_measured_AFE_12, 600, 49.0, 62.0, 0.1, 20, 12,
    #                                   'current_voltage_dependence_SiPM_0139_20C_20012023a')

    # parameters = {
    #     12: {
    #         "set_master_a": a_master_set_AFE_12_new,
    #         "set_master_b": b_master_set_AFE_12_new,
    #         "set_slave_a": a_slave_set_AFE_12_new,
    #         "set_slave_b": b_slave_set_AFE_12_new,
    #         "measured_master_a": a_master_measured_AFE_12_new,
    #         "measured_master_b": b_master_measured_AFE_12_new,
    #         "measured_slave_a": a_slave_measured_AFE_12_new,
    #         "measured_slave_b": b_slave_measured_AFE_12_new
    #     },
    #     13: {
    #         "set_master_a": a_master_set_AFE_13_new,
    #         "set_master_b": b_master_set_AFE_13_new,
    #         "set_slave_a": a_slave_set_AFE_13_new,
    #         "set_slave_b": b_slave_set_AFE_13_new,
    #         "measured_master_a": a_master_measured_AFE_13_new,
    #         "measured_master_b": b_master_measured_AFE_13_new,
    #         "measured_slave_a": a_slave_measured_AFE_13_new,
    #         "measured_slave_b": b_slave_measured_AFE_13_new
    #     },
    #     14: {
    #         "set_master_a": a_master_set_AFE_14_new,
    #         "set_master_b": b_master_set_AFE_14_new,
    #         "set_slave_a": a_slave_set_AFE_14_new,
    #         "set_slave_b": b_slave_set_AFE_14_new,
    #         "measured_master_a": a_master_measured_AFE_14_new,
    #         "measured_master_b": b_master_measured_AFE_14_new,
    #         "measured_slave_a": a_slave_measured_AFE_14_new,
    #         "measured_slave_b": b_slave_measured_AFE_14_new
    #     },
    #     15: {
    #         "set_master_a": a_master_set_AFE_15_new,
    #         "set_master_b": b_master_set_AFE_15_new,
    #         "set_slave_a": a_slave_set_AFE_15_new,
    #         "set_slave_b": b_slave_set_AFE_15_new,
    #         "measured_master_a": a_master_measured_AFE_15_new,
    #         "measured_master_b": b_master_measured_AFE_15_new,
    #         "measured_slave_a": a_slave_measured_AFE_15_new,
    #         "measured_slave_b": b_slave_measured_AFE_15_new
    #     },
    #     16: {
    #         "set_master_a": a_master_set_AFE_16_new,
    #         "set_master_b": b_master_set_AFE_16_new,
    #         "set_slave_a": a_slave_set_AFE_16_new,
    #         "set_slave_b": b_slave_set_AFE_16_new,
    #         "measured_master_a": a_master_measured_AFE_16_new,
    #         "measured_master_b": b_master_measured_AFE_16_new,
    #         "measured_slave_a": a_slave_measured_AFE_16_new,
    #         "measured_slave_b": b_slave_measured_AFE_16_new
    #     },
    #     17: {
    #         "set_master_a": a_master_set_AFE_17_new,
    #         "set_master_b": b_master_set_AFE_17_new,
    #         "set_slave_a": a_slave_set_AFE_17_new,
    #         "set_slave_b": b_slave_set_AFE_17_new,
    #         "measured_master_a": a_master_measured_AFE_17_new,
    #         "measured_master_b": b_master_measured_AFE_17_new,
    #         "measured_slave_a": a_slave_measured_AFE_17_new,
    #         "measured_slave_b": b_slave_measured_AFE_17_new
    #     },
    #     18: {
    #         "set_master_a": a_master_set_AFE_18_new,
    #         "set_master_b": b_master_set_AFE_18_new,
    #         "set_slave_a": a_slave_set_AFE_18_new,
    #         "set_slave_b": b_slave_set_AFE_18_new,
    #         "measured_master_a": a_master_measured_AFE_18_new,
    #         "measured_master_b": b_master_measured_AFE_18_new,
    #         "measured_slave_a": a_slave_measured_AFE_18_new,
    #         "measured_slave_b": b_slave_measured_AFE_18_new
    #     },
    #     39: {
    #         "set_master_a": a_master_set_AFE_39,
    #         "set_master_b": b_master_set_AFE_39,
    #         "set_slave_a": a_slave_set_AFE_39,
    #         "set_slave_b": b_slave_set_AFE_39,
    #         "measured_master_a": a_master_measured_AFE_39,
    #         "measured_master_b": b_master_measured_AFE_39,
    #         "measured_slave_a": a_slave_measured_AFE_39,
    #         "measured_slave_b": b_slave_measured_AFE_39
    #     }
    # }
    #
    # current_voltage_dependence_multi_slabs(parameters, 1800, 48.6, 51.0, 0.2, 20, 12,
    #                                        'current_low_voltage_dependencies') #Dało niepoprawne wyniki - metoda jest do poprawy.

    # current_voltage_dependence_slave2_without_Keithley(a_slave_set_AFE_12_new, b_slave_set_AFE_12_new, a_slave_measured_AFE_12_new,
    #                                   b_slave_measured_AFE_12_new, 600, 48.6, 51.0, 0.2, 20, 12,
    #                                   'current_low_voltage_dependence_AFE_12_new_slave')

    # current_voltage_dependence_master2_without_Keithley(a_master_set_AFE_12_new, b_master_set_AFE_12_new, a_master_measured_AFE_12_new,
    #                                   b_master_measured_AFE_12_new, 600, 48.6, 51.0, 0.2, 20, 12,
    #                                   'current_low_voltage_dependence_AFE_12_new_master')

    # current_voltage_dependence_slave2_without_Keithley(a_slave_set_AFE_13_new, b_slave_set_AFE_13_new, a_slave_measured_AFE_13_new,
    #                                   b_slave_measured_AFE_13_new, 600, 48.6, 51.0, 0.2, 20, 12,
    #                                   'current_low_voltage_dependence_AFE_13_new_slave')

    # current_voltage_dependence_master2_without_Keithley(a_master_set_AFE_13_new, b_master_set_AFE_13_new, a_master_measured_AFE_13_new,
    #                                   b_master_measured_AFE_13_new, 600, 48.6, 51.0, 0.2, 20, 12,
    #                                   'current_low_voltage_dependence_AFE_13_new_master')

    # current_voltage_dependence_slave2_without_Keithley(a_slave_set_AFE_14_new, b_slave_set_AFE_14_new, a_slave_measured_AFE_14_new,
    #                                   b_slave_measured_AFE_14_new, 600, 48.6, 51.0, 0.2, 20, 12,
    #                                   'current_low_voltage_dependence_AFE_14_new_slave')
    #
    # current_voltage_dependence_master2_without_Keithley(a_master_set_AFE_14_new, b_master_set_AFE_14_new, a_master_measured_AFE_14_new,
    #                                   b_master_measured_AFE_14_new, 600, 48.6, 51.0, 0.2, 20, 12,
    #                                   'current_low_voltage_dependence_AFE_14_new_master')

    # current_voltage_dependence_slave2_without_Keithley(a_slave_set_AFE_39, b_slave_set_AFE_39, a_slave_measured_AFE_39,
    #                                   b_slave_measured_AFE_39, 600, 48.6, 51.0, 0.2, 20, 12,
    #                                   'current_low_voltage_dependence_AFE_39_slave')
    #
    # current_voltage_dependence_master2_without_Keithley(a_master_set_AFE_39, b_master_set_AFE_39, a_master_measured_AFE_39,
    #                                   b_master_measured_AFE_39, 600, 48.6, 51.0, 0.2, 20, 12,
    #                                   'current_low_voltage_dependence_AFE_39_master')


    # current_voltage_dependence_slave2_without_Keithley(a_slave_set_AFE_15_new, b_slave_set_AFE_15_new, a_slave_measured_AFE_15_new,
    #                                   b_slave_measured_AFE_15_new, 600, 48.6, 51.0, 0.2, 20, 12,
    #                                   'current_low_voltage_dependence_AFE_15_new_slave')
    #
    # current_voltage_dependence_master2_without_Keithley(a_master_set_AFE_15_new, b_master_set_AFE_15_new, a_master_measured_AFE_15_new,
    #                                   b_master_measured_AFE_15_new, 600, 48.6, 51.0, 0.2, 20, 12,
    #                                   'current_low_voltage_dependence_AFE_15_new_master')

    # current_voltage_dependence_master2_without_Keithley(a_master_set_AFE_15_new, b_master_set_AFE_15_new, a_master_measured_AFE_15_new,
    #                                   b_master_measured_AFE_15_new, 600, 52.0, 63.0, 0.5, 20, 12,
    #                                   'current_high_voltage_test_dependence_AFE_15_new_master')

    # current_voltage_dependence_slave2_without_Keithley(a_slave_set_AFE_16_new, b_slave_set_AFE_16_new, a_slave_measured_AFE_16_new,
    #                                   b_slave_measured_AFE_16_new, 600, 48.6, 51.0, 0.2, 20, 12,
    #                                   'current_low_voltage_dependence_AFE_16_new_slave')
    #
    # current_voltage_dependence_master2_without_Keithley(a_master_set_AFE_15_new, b_master_set_AFE_16_new, a_master_measured_AFE_16_new,
    #                                   b_master_measured_AFE_16_new, 600, 48.6, 51.0, 0.2, 20, 12,
    #                                   'current_low_voltage_dependence_AFE_16_new_master')                                                #Parametr kalibracyjny został nie dla tej deski, ale dla pomiaru szumu nie ma to praktycznie znaczenia

    # current_voltage_dependence_slave2_without_Keithley(a_slave_set_AFE_17_new, b_slave_set_AFE_17_new, a_slave_measured_AFE_17_new,
    #                                   b_slave_measured_AFE_17_new, 600, 48.6, 51.0, 0.2, 20, 12,
    #                                   'current_low_voltage_dependence_AFE_17_new_slave')
    #
    # current_voltage_dependence_master2_without_Keithley(a_master_set_AFE_17_new, b_master_set_AFE_17_new, a_master_measured_AFE_17_new,
    #                                   b_master_measured_AFE_17_new, 600, 48.6, 51.0, 0.2, 20, 12,
    #                                   'current_low_voltage_dependence_AFE_17_new_master')

    # current_voltage_dependence_slave2_without_Keithley(a_slave_set_AFE_18_new, b_slave_set_AFE_18_new, a_slave_measured_AFE_18_new,
    #                                   b_slave_measured_AFE_18_new, 600, 48.6, 51.0, 0.2, 20, 12,
    #                                   'current_low_voltage_dependence_AFE_18_new_slave')
    #
    # current_voltage_dependence_master2_without_Keithley(a_master_set_AFE_18_new, b_master_set_AFE_18_new, a_master_measured_AFE_18_new,
    #                                   b_master_measured_AFE_18_new, 600, 48.6, 51.0, 0.2, 20, 12,
    #                                   'current_low_voltage_dependence_AFE_18_new_master')

    # current_voltage_dependence_slave2_without_Keithley(a_slave_set_AFE_32, b_slave_set_AFE_32, a_slave_measured_AFE_32,
    #                                   b_slave_measured_AFE_32, 3600, 51.0, 62.0, 0.1, 20, 12,
    #                                   'current_voltage_dependence_AFE_32_1s_slave')
    #
    # current_voltage_dependence_master2_without_Keithley(a_master_set_AFE_32, b_master_set_AFE_32, a_master_measured_AFE_32,
    #                                   b_master_measured_AFE_32, 3600, 51.0, 62.0, 0.1, 20, 12,
    #                                   'current_voltage_dependence_AFE_32_1s_master')

    # current_voltage_dependence_slave2_without_Keithley(a_slave_set_AFE_32, b_slave_set_AFE_32, a_slave_measured_AFE_32,
    #                                   b_slave_measured_AFE_32, 600, 48.6, 51.0, 0.2, 20, 12,
    #                                   'current_low_voltage_dependence_AFE_32_1s_slave20230322')

    # current_voltage_dependence_slave2_without_Keithley(a_slave_set_AFE_32, b_slave_set_AFE_32, a_slave_measured_AFE_32,
    #                                   b_slave_measured_AFE_32, 600, 48.6, 51.0, 0.2, 20, 12,
    #                                   'current_low_voltage_dependence_AFE_32_1s_slave_other_hub_20230322b')

    # current_voltage_dependence_slave2_without_Keithley(a_slave_set_AFE_18_new, b_slave_set_AFE_18_new, a_slave_measured_AFE_18_new,
    #                                   b_slave_measured_AFE_18_new, 600, 48.6, 51.0, 0.2, 20, 12,
    #                                   'current_low_voltage_dependence_AFE_18_new_slave_other_hub_20230322c')
    #
    # current_voltage_dependence_master2_without_Keithley(a_master_set_AFE_18_new, b_master_set_AFE_18_new, a_master_measured_AFE_18_new,
    #                                   b_master_measured_AFE_18_new, 600, 48.6, 51.0, 0.2, 20, 12,
    #                                   'current_low_voltage_dependence_AFE_18_new_master_other_hub_20230322c')

    # current_voltage_dependence_slave2_without_Keithley(a_slave_set_AFE_32, b_slave_set_AFE_32, a_slave_measured_AFE_32,
    #                                   b_slave_measured_AFE_32, 3600, 51.0, 62.0, 0.1, 20, 12,
    #                                   'current_voltage_dependence_AFE_32_0s_slave20230322d')
    #
    # current_voltage_dependence_master2_without_Keithley(a_master_set_AFE_32, b_master_set_AFE_32, a_master_measured_AFE_32,
    #                                   b_master_measured_AFE_32, 3600, 51.0, 62.0, 0.1, 20, 12,
    #                                   'current_voltage_dependence_AFE_32_0s_master20230322d')

    # calibration(1800, 0, 4095, 64, 12, 0.01, 'calibration_keithley_master_without_resistor_AFE_0_filter3_20230328a.csv',
                # SipmType.MASTER)

    # current_calibration_SiPM_master2all(a_master_set_AFE_0, b_master_set_AFE_0, a_master_measured_AFE_0,
    #                                     b_master_measured_AFE_0, 1800, 48.5, 62.5, 0.1, 20, 12,
    #                                    'current_calibration_master_AFE_0_10.5MOhm_20230328b')

    # current_calibration_SiPM_master2all(a_master_set_AFE_0, b_master_set_AFE_0, a_master_measured_AFE_0,
    #                                     b_master_measured_AFE_0, 1800, 48.5, 62.5, 0.1, 20, 12,
    #                                    'current_calibration_master_AFE_0_145MOhm_20230329a')

    # current_calibration_SiPM_master2all(a_master_set_AFE_0, b_master_set_AFE_0, a_master_measured_AFE_0,
    #                                     b_master_measured_AFE_0, 1800, 48.5, 62.5, 0.1, 20, 12,
    #                                    'current_calibration_master_AFE_0_478MOhm_20230329b')

    # current_calibration_SiPM_master2all(a_master_set_AFE_0, b_master_set_AFE_0, a_master_measured_AFE_0,
    #                                     b_master_measured_AFE_0, 600, 48.5, 62.5, 0.1, 20, 12,
    #                                    'current_calibration_master_extra_capacitor_AFE_0_478MOhm_20230329c')

    # current_calibration_SiPM_master2all(a_master_set_AFE_0, b_master_set_AFE_0, a_master_measured_AFE_0,
    #                                     b_master_measured_AFE_0, 3600, 48.5, 62.5, 0.1, 20, 12,
    #                                    'current_calibration_master_2extra_capacitors_AFE_0_478MOhm_20230329d')

    # current_calibration_SiPM_master2all(a_master_set_AFE_0, b_master_set_AFE_0, a_master_measured_AFE_0,
    #                                     b_master_measured_AFE_0, 1800, 48.5, 62.5, 0.1, 20, 12,
    #                                    'current_calibration_master_2extra_capacitors_changed_gain_AFE_0_145MOhm_20230330a')

    # current_calibration_SiPM_master2all(a_master_set_AFE_0, b_master_set_AFE_0, a_master_measured_AFE_0,
    #                                     b_master_measured_AFE_0, 1800, 48.5, 62.5, 0.1, 20, 12,
    #                                    'current_calibration_master_2extra_capacitors__changed_gain_AFE_0_478MOhm_20230330b')

    # current_calibration_SiPM_master2all(a_master_set_AFE_0, b_master_set_AFE_0, a_master_measured_AFE_0,
    #                                     b_master_measured_AFE_0, 1800, 48.5, 62.5, 0.1, 20, 12,
    #                                    'current_calibration_master_2extra_capacitors_changed_gain_AFE_0_10.5MOhm_20230330c')

    # calibration(1800, 0, 4095, 64, 12, 0.01, 'calibration_keithley_slave_without_resistor_2extra_capacitors_changed_gain_AFE_0_filter3_20230330d.csv',
    #             SipmType.SLAVE)

    # current_calibration_SiPM_slave2all(a_slave_set_AFE_0, b_slave_set_AFE_0, a_slave_measured_AFE_0,
                                        # b_slave_measured_AFE_0, 1800, 48.5, 62.5, 0.1, 20, 12,
                                       # 'current_calibration_slave_2extra_capacitors_changed_gain_AFE_0_10.5MOhm_20230331a')

    # current_calibration_SiPM_slave2all(a_slave_set_AFE_0, b_slave_set_AFE_0, a_slave_measured_AFE_0,
    #                                     b_slave_measured_AFE_0, 1800, 48.5, 62.5, 0.1, 20, 12,
    #                                    'current_calibration_slave_2extra_capacitors_changed_gain_AFE_0_478MOhm_20230331a')

    # current_calibration_SiPM_slave2all(a_slave_set_AFE_0, b_slave_set_AFE_0, a_slave_measured_AFE_0,
    #                                     b_slave_measured_AFE_0, 1800, 48.5, 62.5, 0.1, 20, 12,
    #                                    'current_calibration_slave_2extra_capacitors_changed_gain_AFE_0_145MOhm_20230403a')

    # current_calibration_SiPM_master2all(a_master_set_AFE_0, b_master_set_AFE_0, a_master_measured_AFE_0,
    #                                     b_master_measured_AFE_0, 1800, 48.5, 62.5, 0.1, 20, 12,
    #                                    'current_calibration_master_2extra_capacitors_changed_gain_AFE_0_10.5MOhm_20230403b')

    # current_calibration_SiPM_master2all(a_master_set_AFE_0, b_master_set_AFE_0, a_master_measured_AFE_0,
    #                                     b_master_measured_AFE_0, 1800, 48.5, 62.5, 0.1, 20, 12,
    #                                    'current_calibration_master_2extra_capacitors_changed_gain_AFE_0_478MOhm_20230404a')

    # current_calibration_SiPM_master2all(a_master_set_AFE_0, b_master_set_AFE_0, a_master_measured_AFE_0,
    #                                     b_master_measured_AFE_0, 1800, 48.5, 62.5, 0.1, 20, 12,
    #                                    'current_calibration_master_2extra_capacitors_changed_gain_AFE_0_145MOhm_20230404b')

    # current_calibration_SiPM_master2all(a_master_set_AFE_0, b_master_set_AFE_0, a_master_measured_AFE_0,
    #                                     b_master_measured_AFE_0, 1800, 48.5, 62.5, 0.1, 20, 12,
    #                                    'current_calibration_master_2extra_capacitors_changed_gain_AFE_0_990MOhm_20230404c')

    # calibration(1800, 0, 4095, 64, 12, 0.01, 'calibration_keithley15052022a_master_without_resistor_AFE_1_filter3.csv',
    #             SipmType.MASTER)

    # calibration(1800, 0, 4095, 64, 12, 0.01, 'calibration_keithley15052023b_slave_without_resistor_AFE_1_filter3.csv',
    #             SipmType.SLAVE)

    # current_calibration_SiPM_slave2all(a_slave_set_AFE_1, b_slave_set_AFE_1, a_slave_measured_AFE_1,
    #                                     b_slave_measured_AFE_1, 1800, 48.5, 62.5, 0.1, 20, 12,
    #                                    'current_calibration_slave_2extra_capacitors_changed_gain5x_AFE_1_478MOhm_20230515c')

    # current_calibration_SiPM_slave2all(a_slave_set_AFE_1, b_slave_set_AFE_1, a_slave_measured_AFE_1,
    #                                     b_slave_measured_AFE_1, 1800, 48.5, 62.5, 0.1, 20, 12,
    #                                    'current_calibration_slave_2extra_capacitors_changed_gain5x_AFE_1_478MOhm_again_20230516a')

    # current_calibration_SiPM_slave2all(a_slave_set_AFE_1, b_slave_set_AFE_1, a_slave_measured_AFE_1,
    #                                     b_slave_measured_AFE_1, 1800, 48.5, 62.5, 0.1, 10, 12,
    #                                    'current_calibration_slave_2extra_capacitors_changed_gain5x_AFE_1_10.48MOhm_20230516b')


    # current_calibration_SiPM_master2all(a_master_set_AFE_1, b_master_set_AFE_1, a_master_measured_AFE_1,
    #                                     b_master_measured_AFE_1, 1800, 48.5, 62.5, 0.1, 10, 12,
    #                                    'current_calibration_master_2extra_capacitors_changed_gain5x_AFE_1_10.48MOhm_20230516c')

    # current_calibration_SiPM_master2all(a_master_set_AFE_1, b_master_set_AFE_1, a_master_measured_AFE_1,
    #                                     b_master_measured_AFE_1, 1800, 48.5, 62.5, 0.1, 20, 12,
    #                                    'current_calibration_master_2extra_capacitors_changed_gain5x_AFE_1_990MOhm_20230516d')

    # current_calibration_SiPM_slave2all(a_slave_set_AFE_1, b_slave_set_AFE_1, a_slave_measured_AFE_1,
    #                                     b_slave_measured_AFE_1, 1800, 48.5, 62.5, 0.1, 20, 12,
    #                                    'current_calibration_slave_2extra_capacitors_changed_gain5x_AFE_1_990MOhm_20230516e')


    # current_calibration_SiPM_slave2all(a_slave_set_AFE_1, b_slave_set_AFE_1, a_slave_measured_AFE_1,
    #                                     b_slave_measured_AFE_1, 1800, 48.5, 62.5, 0.1, 20, 12,
    #                                    'current_calibration_slave_2extra_capacitors_changed_gain5x_AFE_1_990MOhm_20230517a')

    # current_calibration_SiPM_slave2all(a_slave_set_AFE_1, b_slave_set_AFE_1, a_slave_measured_AFE_1,
    #                                     b_slave_measured_AFE_1, 1800, 48.5, 62.5, 0.1, 20, 12,
    #                                    'current_calibration_slave_2extra_capacitors_changed_gain5x_AFE_1_145MOhm_20230517b')

    # current_calibration_SiPM_master2all(a_master_set_AFE_1, b_master_set_AFE_1, a_master_measured_AFE_1,
    #                                     b_master_measured_AFE_1, 1800, 48.5, 62.5, 0.1, 20, 12,
    #                                    'current_calibration_master_2extra_capacitors_changed_gain5x_AFE_1_145MOhm_20230517c')

    # current_calibration_SiPM_master2all(a_master_set_AFE_1, b_master_set_AFE_1, a_master_measured_AFE_1,
    #                                     b_master_measured_AFE_1, 1800, 48.5, 62.5, 0.1, 20, 12,
    #                                    'current_calibration_master_2extra_capacitors_changed_gain5x_AFE_1_478MOhm_20230517d')

    # current_voltage_dependence_master2_without_Keithley(a_master_set_AFE_1, b_master_set_AFE_1, a_master_measured_AFE_1,
    #                                   b_master_measured_AFE_1, 7200, 48.6, 62.0, 0.1, 20, 12,
    #                                   'current_voltage_dependence_AFE_1_2extra_capacitors_changed_gain5x_master.csv')

    # current_voltage_dependence_slave2_without_Keithley(a_slave_set_AFE_1, b_slave_set_AFE_1, a_slave_measured_AFE_1,
    #                                   b_slave_measured_AFE_1, 900, 48.6, 62.0, 0.1, 20, 12,
    #                                   'current_voltage_dependence_AFE_1_2extra_capacitors_changed_gain5x_slave.csv')

    # current_voltage_dependence_slave2_without_Keithley_time(a_slave_set_AFE_18_new, b_slave_set_AFE_18_new, a_slave_measured_AFE_18_new,
    #                                   b_slave_measured_AFE_18_new, 60, 48.6, 62.0, 0.1, 1000, 12,
    #                                   'current_timing_test4.csv')
    # keithley = keithley_util.Keithley6517()
    # print(keithley.measure(keithley_util.MeasurementType.CURRENT)["current"])
    # connection = lanconnection.LanConnection(ip, port)
    # connection.do_cmd(['init', bar_id])
    # connection.do_cmd(['hvon', bar_id])
    # voltage_bit = int(a_master_set_AFE_12 * 49 + b_master_set_AFE_12)
    # set_bit_voltage(voltage_bit, connection)
    # keithley.setVoltage(30.12345)
    # time.sleep(2)
    # print(connection.do_cmd(['adc', bar_id, 5])[1])
    # connection.close_connection()
    # print(keithley.measure(keithley_util.MeasurementType.CURRENT)["current"])
    # new_current_callibration(120, 45, 49.7, 0.1, 10, 19, "test_new_current_callibration2.csv")
    #  new_current_callibration_reverse(120, 49.7, 45, 0.1, 10, 10, "test_new_current_callibration4.csv")
    # new_current_callibration_reverse(120, 49.7, 45, 0.1, 10, 10, "test_new_current_callibration5.csv")
    # new_current_callibration_reverse(10, 49.7, 45, 0.1, 10, 10, "test_new_current_callibration9.csv")
    # test_range()
    # new_current_callibration_reverse(10, 50.5, 47, 0.05, 10, 10, "test_new_current_callibration15.csv")
    # test_nplc()
    # new_current_callibration_reverse(10, 50.5, 47, 0.05, 10, 10, "test_new_current_callibration16.csv")
    # new_current_callibration_reverse(10, 50.5, 47, 0.05, 10, 10, "test_new_current_callibration17_range_e-5.csv")
    # new_current_callibration_reverse(10, 48, 35, 0.1, 10, 10, "test_new_current_callibration18_range_e-5.csv")
    # new_current_callibration_reverse(10, 50, 40, 0.1, 10, 10, "test_new_current_callibration19_range_e-5.csv")
    # new_current_callibration_reverse(10, 50.6, 0, 0.2, 10, 10, "test_new_current_callibration21_range_e-5.csv")
    # connection = lanconnection.LanConnection(ip, port)
    # connection.do_cmd(['init', bar_id])
    # connection.do_cmd(['hvon', bar_id])
    # print(measure_avg_current2(avg_current_number, SipmType.MASTER,
    #                      connection))
    # new_current_callibration2(a_master_set_AFE_12, b_master_set_AFE_12, a_master_measured_AFE_12, b_master_measured_AFE_12,
    #                           60, 48.5, 62.5, 0.1, 6, 10, "test_new_current_callibration1_voltage_method_10V")
    # new_current_callibration2(a_master_set_AFE_12, b_master_set_AFE_12, a_master_measured_AFE_12, b_master_measured_AFE_12,
    #                           60, 48.5, 62.5, 0.1, 6, 10, "test_new_current_callibration1_voltage_method_40V")
    # new_current_callibration_reverse(60, 50.5, 47, 0.1, 10, 10, "test_new_current_callibration22_range_e-6.csv")
    # new_current_callibration_reverse(60, 50.5, 47, 0.1, 10, 10, "test_new_current_callibration23_range_e-5.csv")
    # new_current_callibration_reverse(60, 50.5, 0, 0.2, 10, 10, "test_new_current_callibration24_range_e-5.csv")
    # new_current_callibration_reverse(60, 50.3, 49.95, 0.05, 10, 10, "test_new_current_callibration25_range_e-7.csv")
    # new_current_callibration_reverse(60, 50.3, 49.2, 0.05, 10, 10, "test_new_current_callibration26_range_e-7.csv")
    # new_current_callibration_reverse(60, 50.5, 47.5, 0.1, 10, 10, "test_new_current_callibration27_range_e-6.csv")
    # new_current_callibration2(a_master_set_AFE_12, b_master_set_AFE_12, a_master_measured_AFE_12, b_master_measured_AFE_12,
    #                           60, 48.5, 62.5, 0.5, 6, 10, "test_new_current_callibration2_voltage_method_40V")
    # new_current_callibration3(a_master_set_AFE_12, b_master_set_AFE_12, a_master_measured_AFE_12, b_master_measured_AFE_12,
    #                           60, 48.5, 62.5, 0.5, 6, 10, "test_new_current_callibration3_voltage_method_40V")
    # calibration(300, 0, 4095, 64, 12, 0.01, 'calibration_keithley05012024a_master_without_resistor_AFE_12_old.csv',
    #             SipmType.MASTER)
    # new_current_callibration2(a_master_set_AFE_12_new_measurement, b_master_set_AFE_12_new_measurement, a_master_measured_AFE_12_new_measurement, b_master_measured_AFE_12_new_measurement,
    #                           60, 48.5, 62.5, 0.5, 6, 10, "test_new_current_callibration4_voltage_method_40V")
    # new_current_callibration2(a_master_set_AFE_12_new_measurement, b_master_set_AFE_12_new_measurement, a_master_measured_AFE_12_new_measurement, b_master_measured_AFE_12_new_measurement,
    #                           60, 48.5, 62.5, 0.5, 6, 10, "test_new_current_callibration5_voltage_method_40V")
    # new_current_callibration2(a_master_set_AFE_12_new_measurement, b_master_set_AFE_12_new_measurement, a_master_measured_AFE_12_new_measurement, b_master_measured_AFE_12_new_measurement,
    #                           60, 48.5, 62.5, 0.05, 30, 10, "test_new_current_callibration6_voltage_method_49V_filtr10")

    # calibration(300, 0, 4095, 64, 12, 0.01, 'calibration_keithley08012024a_master_without_resistor_AFE_12_old.csv',
    #             SipmType.SLAVE)


    # new_current_callibration4(SipmType.SLAVE, a_master_set_AFE_12_new_measurement, b_master_set_AFE_12_new_measurement, a_master_measured_AFE_12_new_measurement, b_master_measured_AFE_12_new_measurement,
    #                           600, 48.5, 62.5, 0.1, 12, 10, "test_new_current_callibration_slave1_voltage_method_49V")

    # new_current_callibration4(SipmType.SLAVE, a_slave_set_AFE_12_new_measurement, b_slave_set_AFE_12_new_measurement, a_slave_measured_AFE_12_new_measurement, b_slave_measured_AFE_12_new_measurement,
    #                           300, 48.5, 62.5, 0.1, 12, 10, "test_new_current_callibration_slave2_voltage_method_49V")

    # new_current_callibration5(SipmType.SLAVE, a_slave_set_AFE_12_new_measurement, b_slave_set_AFE_12_new_measurement, a_slave_measured_AFE_12_new_measurement, b_slave_measured_AFE_12_new_measurement,
    #                           600, 48.5, 62.5, 0.5, 12, 10, "test_new_current_callibration_slave3_voltage_method_13.2V")

    # calibration2(30, 0, 4095, 512, 12, 0.01, 6, 'calibration2_test',
    #             SipmType.SLAVE)
    # calibration2(7200, 0, 4095, 64, 12, 0.01, 30, 'calibration_keithley09012024a_slave_without_resistor_AFE_12_old_filter10_2h.csv',
    #             SipmType.SLAVE)
    # calibration2(60, 0, 4095, 64, 12, 0.01, 30, 'calibration3_test',
                # SipmType.SLAVE)
    # calibration2(7200, 0, 4095, 64, 12, 0.01, 30, 'calibration_keithley09012024a_slave_without_resistor_AFE_12_old_filter10_2h_again.csv',
    #             SipmType.SLAVE)
    # calibration2(60, 0, 4095, 256, 12, 0.01, 6, 'calibration4_test',
    #             SipmType.SLAVE)
    # calibration2(60, 0, 4095, 256, 12, 0.01, 6, 'calibration5_test',
    #             SipmType.SLAVE)
    # calibration2(7200, 0, 4095, 64, 12, 0.01, 30, 'calibration_keithley10012024a_slave_without_resistor_AFE_12_old_filter10_2h_again2.csv',
    #             SipmType.SLAVE)
    # calibration2(7200, 0, 4095, 64, 12, 0.01, 30, 'calibration_keithley11012024a_slave_without_resistor_AFE_12_old_filter10_2h_again3.csv',
    #             SipmType.SLAVE)
    # calibration2(300, 0, 4095, 128, 12, 0.01, 10, 'calibration_keithley15012024a_slave_without_resistor_AFE_12_old_filter10_5m.csv',
    #             SipmType.SLAVE)
    # calibration2(1800, 0, 4095, 64, 12, 0.01, 15, 'calibration_keithley15012024b_slave_without_resistor_AFE_12_old_filter10_30m.csv',
    #             SipmType.SLAVE)
    # new_current_callibration5(SipmType.SLAVE, a_slave_set_AFE_12_new_measurement2, b_slave_set_AFE_12_new_measurement2, a_slave_measured_AFE_12_new_measurement2, b_slave_measured_AFE_12_new_measurement2,
    #                           120, 48.5, 62.5, 0.5, 6, 12, "test_new_current_callibration_slave5_voltage_method_49V_again2")
    # new_current_callibration5(SipmType.SLAVE, a_slave_set_AFE_12_new_measurement2, b_slave_set_AFE_12_new_measurement2, a_slave_measured_AFE_12_new_measurement2, b_slave_measured_AFE_12_new_measurement2,
    #                           120, 48.5, 62.5, 0.5, 6, 12, "test_new_current_callibration_slave5_voltage_method_49V_again4")
    # stability2_slave(a_slave_measured_AFE_12_new_measurement2, b_slave_measured_AFE_12_new_measurement2, 49, 5, 0.01, "test_stability2_slave_2023_01_17_v9")
    # stability2_slave(a_slave_measured_AFE_12_new_measurement2, b_slave_measured_AFE_12_new_measurement2, 50, 5, 0.01,
    #                  "test_stability2_slave_2023_01_17_v10")
    # stability2_slave_many_voltage(a_slave_measured_AFE_12_new_measurement2, b_slave_measured_AFE_12_new_measurement2, 49, 1800, 50, 1800, 60, 1800, 5, 0.01, "test_stability2_slave_many_voltage_2023_01_18_v1")
    # stability2_slave_many_voltage(a_slave_measured_AFE_12_new_measurement2, b_slave_measured_AFE_12_new_measurement2, 49, 1800, 50, 1800, 60, 1800, 5, 0.01, "test_stability2_slave_many_voltage_2023_01_18_v2")
    # stability2_slave_many_voltage(a_slave_measured_AFE_12_new_measurement2, b_slave_measured_AFE_12_new_measurement2, 49, 7200, 50, 7200, 60, 7200, 5, 0.01, "test_stability2_slave_many_voltage_2023_01_19_v3") #zimne afe
    # calibration3(1800, 0, 4095, 64, 12, 0.01, 10, 5, 'calibration3_keithley23012024a_slave_without_resistor_AFE_12_old_without_filter_30m.csv', SipmType.SLAVE)
    # calibration3(3600, 0, 4095, 64, 12, 0.01, 10, 5, 'calibration3_keithley24012024a_slave_without_resistor_AFE_12_old_without_filter_60m.csv', SipmType.SLAVE)
    # new_current_callibration6(SipmType.SLAVE, a_slave_set_AFE_12_new_measurement3, b_slave_set_AFE_12_new_measurement3, a_slave_measured_AFE_12_new_measurement3, b_slave_measured_AFE_12_new_measurement3, 7200,
    #                           50, 60, 49, 62.5, 0.05,
    #                           40, 60, 49, 62.5, 0.1,
    #                           30, 60, 49, 62.5, 0.1,
    #                           20, 60, 49, 62.5, 0.5,
    #                           10, 60, 49, 62.5, 0.5,
    #                           10, 5, 12, 0.01, "test_new_current_callibration6_v2")
    # new_current_callibration6(SipmType.SLAVE, a_slave_set_AFE_12_new_measurement3, b_slave_set_AFE_12_new_measurement3, a_slave_measured_AFE_12_new_measurement3, b_slave_measured_AFE_12_new_measurement3, 1800,
    #                           50, 60, 49, 62.5, 0.05,
    #                           40, 60, 49, 62.5, 0.1,
    #                           30, 60, 49, 62.5, 0.1,
    #                           20, 60, 49, 62.5, 0.5,
    #                           10, 60, 49, 62.5, 0.5,
    #                           10, 5, 12, 0.01, "test_new_current_callibration6_v3")

    # new_current_callibration7(SipmType.SLAVE, a_slave_set_AFE_12_new_measurement3, b_slave_set_AFE_12_new_measurement3, a_slave_measured_AFE_12_new_measurement3, b_slave_measured_AFE_12_new_measurement3, 1800,
    #                           10, 60, 62.5, 49, 0.5,
    #                           20, 60, 62.5, 49, 0.5,
    #                           30, 60, 62.5, 49, 0.5,
    #                           40, 60, 62.5, 49, 0.5,
    #                           50, 60, 62.5, 55, 0.1,
    #                           50, 30, 55, 49, 0.05,
    #                           10, 5, 12, 0.01, "test_new_current_callibration7_v1")

    # new_current_callibration7(SipmType.SLAVE, a_slave_set_AFE_12_new_measurement3, b_slave_set_AFE_12_new_measurement3, a_slave_measured_AFE_12_new_measurement3, b_slave_measured_AFE_12_new_measurement3, 1800,
    #                          10, 60, 59, 49, 1,
    #                          20, 60, 60, 49, 1,
    #                          30, 60, 60, 49, 1,
    #                          40, 60, 60, 49, 1,
    #                          50, 60, 60, 53, 0.5,
    #                          50, 30, 53, 49, 0.05,
    #                          10, 5, 12, 0.01, "test_new_current_callibration7_v2")

    # new_current_callibration7(SipmType.SLAVE, a_slave_set_AFE_12_new_measurement3, b_slave_set_AFE_12_new_measurement3, a_slave_measured_AFE_12_new_measurement3, b_slave_measured_AFE_12_new_measurement3, 1800,
    #                           10, 60, 59, 49, 1,
    #                           20, 60, 59, 49, 1,
    #                           30, 60, 59, 49, 1,
    #                           40, 60, 59, 49, 1,
    #                           50, 60, 59, 52, 0.5,
    #                           50, 30, 52, 49, 0.05,
    #                           10, 5, 12, 0.01, "test_new_current_callibration7_v3")

    # new_current_callibration7(SipmType.SLAVE, a_slave_set_AFE_12_new_measurement3, b_slave_set_AFE_12_new_measurement3, a_slave_measured_AFE_12_new_measurement3, b_slave_measured_AFE_12_new_measurement3, 180,
    #                           10, 60, 59, 49, 1,
    #                           20, 60, 59, 49, 1,
    #                           30, 60, 59, 49, 1,
    #                           40, 60, 59, 49, 1,
    #                           50, 60, 59, 52, 0.5,
    #                           50, 30, 52, 49, 0.05,
    #                           10, 5, 12, 0.01, "test_new_current_callibration7_v4")

    # calibration3(3600, 0, 4095, 64, 12, 0.01, 10, 5, 'calibration3_keithley31012024a_master_without_resistor_AFE_12_old_without_filter_60m.csv', SipmType.MASTER)

    # new_current_callibration7(SipmType.MASTER, a_master_set_AFE_12_new_measurement2, b_master_set_AFE_12_new_measurement2, a_master_measured_AFE_12_new_measurement2, b_master_measured_AFE_12_new_measurement2, 3600,
    #                           10, 60, 59, 49, 1,
    #                           20, 60, 59, 49, 1,
    #                           30, 60, 59, 49, 1,
    #                           40, 60, 59, 49, 1,
    #                           50, 60, 59, 52, 0.5,
    #                           50, 30, 52, 49, 0.05,
    #                           10, 5, 12, 0.01, "test_new_current_callibration7_v5")

    # calibration3(4200, 0, 4095, 64, 12, 0.01, 10, 5,
    #              'calibration3_keithley02022024a_master_without_resistor_AFE_22_without_filter_90m.csv',
    #              SipmType.MASTER)


    # new_current_callibration7(SipmType.MASTER, a_master_set_AFE_22_without_capacitors, b_master_set_AFE_22_without_capacitors, a_master_measured_AFE_22_without_capacitors, b_master_measured_AFE_22_without_capacitors, 3600,
    #                           10, 60, 59, 49, 1,
    #                           20, 60, 59, 49, 1,
    #                           30, 60, 59, 49, 1,
    #                           40, 60, 59, 49, 1,
    #                           50, 60, 59, 52, 0.5,
    #                           50, 30, 52, 49, 0.05,
    #                           10, 5, 12, 0.01, "new_current_callibration_afe_wihout_capacitors_v1_20240202")
    #
    # new_current_callibration7(SipmType.MASTER, a_master_set_AFE_22_without_capacitors, b_master_set_AFE_22_without_capacitors, a_master_measured_AFE_22_without_capacitors, b_master_measured_AFE_22_without_capacitors, 1800,
    #                           10, 60, 62.5, 49, 0.5,
    #                           20, 60, 62.5, 49, 0.5,
    #                           30, 60, 62.5, 49, 0.5,
    #                           40, 60, 62.5, 49, 0.5,
    #                           50, 60, 62.5, 55, 0.1,
    #                           50, 30, 55, 49, 0.05,
    #                           100, 5, 12, 0.01, "new_current_callibration_afe_wihout_capacitors_v2_20240202")

    # current_measurement_to_histogram(SipmType.MASTER, a_master_set_AFE_22_without_capacitors, b_master_set_AFE_22_without_capacitors, a_master_measured_AFE_22_without_capacitors, b_master_measured_AFE_22_without_capacitors, 300,
    #                                  50, 50.35, 100, 5, 0.01, "test_current_measurement_to_histogram_v1")
    #
    # current_measurement_to_histogram(SipmType.MASTER, a_master_set_AFE_22_without_capacitors, b_master_set_AFE_22_without_capacitors, a_master_measured_AFE_22_without_capacitors, b_master_measured_AFE_22_without_capacitors, 300,
    #                                  50, 50.35, 100, 5, 0.01, "test_current_measurement_to_histogram_v2")

    # current_measurement_to_histogram(SipmType.MASTER, a_master_set_AFE_22_without_capacitors, b_master_set_AFE_22_without_capacitors, a_master_measured_AFE_22_without_capacitors, b_master_measured_AFE_22_without_capacitors, 7200,
    #                                  50, 49.9, 10000, 5, 0.01, "current_measurement_to_histogram_2024_02_06a.csv")
    # current_measurement_to_histogram(SipmType.MASTER, a_master_set_AFE_22_without_capacitors, b_master_set_AFE_22_without_capacitors, a_master_measured_AFE_22_without_capacitors, b_master_measured_AFE_22_without_capacitors, 1800,
    #                                  50, 50.1, 10000, 5, 0.01, "current_measurement_to_histogram_2024_02_06b.csv")
    # current_measurement_to_histogram(SipmType.MASTER, a_master_set_AFE_22_without_capacitors, b_master_set_AFE_22_without_capacitors, a_master_measured_AFE_22_without_capacitors, b_master_measured_AFE_22_without_capacitors, 1800,
    #                                  50, 50.35, 10000, 5, 0.01, "current_measurement_to_histogram_2024_02_06c.csv")
    # current_measurement_to_histogram(SipmType.MASTER, a_master_set_AFE_22_without_capacitors, b_master_set_AFE_22_without_capacitors, a_master_measured_AFE_22_without_capacitors, b_master_measured_AFE_22_without_capacitors, 1800,
    #                                  50, 51.45, 10000, 5, 0.01, "current_measurement_to_histogram_2024_02_06d.csv")

    # calibration3(4200, 0, 4095, 64, 12, 0.01, 10, 5,
    #              'calibration3_keithley07022024a_master_without_resistor_AFE_22_without_filter_90m.csv',
    #              SipmType.SLAVE) #niepoprawna nazwa - zmieniono tak, żeby w nazwie było slave, zamiast master

    # new_current_callibration7(SipmType.SLAVE, a_slave_set_AFE_22_without_capacitors, b_slave_set_AFE_22_without_capacitors, a_slave_measured_AFE_22_without_capacitors, b_slave_measured_AFE_22_without_capacitors, 3600,
    #                           10, 60, 59, 49, 1,
    #                           20, 60, 59, 49, 1,
    #                           30, 60, 59, 49, 1,
    #                           40, 60, 59, 49, 1,
    #                           50, 60, 59, 52, 0.5,
    #                           50, 30, 52, 49, 0.05,
    #                           10, 5, 12, 0.01, "new_current_callibration_slave_afe22_wihout_capacitors_v1_20240207")
    #
    # new_current_callibration7(SipmType.SLAVE, a_slave_set_AFE_22_without_capacitors, b_slave_set_AFE_22_without_capacitors, a_slave_measured_AFE_22_without_capacitors, b_slave_measured_AFE_22_without_capacitors, 1800,
    #                           10, 60, 62.5, 49, 0.5,
    #                           20, 60, 62.5, 49, 0.5,
    #                           30, 60, 62.5, 49, 0.5,
    #                           40, 60, 62.5, 49, 0.5,
    #                           50, 60, 62.5, 55, 0.1,
    #                           50, 30, 55, 49, 0.05,
    #                           100, 5, 12, 0.01, "new_current_callibration_slave_afe22_wihout_capacitors_v2_20240207")

    # current_measurement_to_histogram(SipmType.SLAVE, a_slave_set_AFE_12_new_measurement3, b_slave_set_AFE_12_new_measurement3, a_slave_measured_AFE_12_new_measurement3, b_slave_measured_AFE_12_new_measurement3, 7200,
    #                                  50, 50.5, 10000, 5, 0.01, "current_measurement_slave_AFE12_to_histogram_2024_02_09a.csv")
    # current_measurement_to_histogram(SipmType.SLAVE, a_slave_set_AFE_12_new_measurement3, b_slave_set_AFE_12_new_measurement3, a_slave_measured_AFE_12_new_measurement3, b_slave_measured_AFE_12_new_measurement3, 1800,
    #                                  50, 50.85, 10000, 5, 0.01, "current_measurement_slave_AFE12_to_histogram_2024_02_09b.csv")
    # current_measurement_to_histogram(SipmType.SLAVE, a_slave_set_AFE_12_new_measurement3, b_slave_set_AFE_12_new_measurement3, a_slave_measured_AFE_12_new_measurement3, b_slave_measured_AFE_12_new_measurement3, 1800,
    #                                  50, 51.45, 10000, 5, 0.01, "current_measurement_slave_AFE12_to_histogram_2024_02_09c.csv")
    # current_measurement_to_histogram(SipmType.SLAVE, a_slave_set_AFE_12_new_measurement3, b_slave_set_AFE_12_new_measurement3, a_slave_measured_AFE_12_new_measurement3, b_slave_measured_AFE_12_new_measurement3, 1800,
    #                                  40, 52.0, 10000, 5, 0.01, "current_measurement_slave_AFE12_to_histogram_2024_02_09d.csv")

    # current_measurement_to_histogram(SipmType.SLAVE, a_slave_set_AFE_12_new_measurement3,
    #                                  b_slave_set_AFE_12_new_measurement3, a_slave_measured_AFE_12_new_measurement3,
    #                                  b_slave_measured_AFE_12_new_measurement3, 30,
    #                                  40, 52.0, 5, 5, 0.01,
    #                                  "current_measurement_slave_AFE12_to_histogram_test_off3")
    # generate_voltage_calibration_parameters_and_plot(SipmType.SLAVE, 'calibration3_keithley07022024a_master_without_resistor_AFE_22_without_filter_90m.csv', 3, 62, 0, 63)
    # generate_voltage_calibration_parameters_and_plot(SipmType.SLAVE,
    #                                                  'calibration3_keithley24012024a_slave_without_resistor_AFE_12_old_without_filter_60m.csv',
    #                                                  3, 62, 0, 63)
    # generate_voltage_calibration_parameters_and_plot(SipmType.SLAVE,
    #                                                  'calibration3_keithley07022024a_slave_without_resistor_AFE_22_without_filter_90m.csv',
    #                                                  3, 62, 0, 63)
    # generate_current_calibration_parameters_and_plot(SipmType.MASTER, 'test_new_current_callibration7_v5.csv')
    # generate_current_calibration_parameters_and_plot(SipmType.SLAVE, 'test_new_current_callibration7_v4.csv')
    new_current_callibration8(SipmType.SLAVE, 'calibration3_keithley07022024a_slave_without_resistor_AFE_22_without_filter_90m_params.csv', 1800,
                              10, 60, 62.5, 49, 0.5,
                              20, 60, 62.5, 49, 0.5,
                              30, 60, 62.5, 49, 0.5,
                              40, 60, 62.5, 49, 0.5,
                              50, 60, 62.5, 55, 0.1,
                              50, 30, 55, 49, 0.05,
                              100, 5, 12, 0.01, "test_params_file")















