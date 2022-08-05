# This is a sample Python s
import time
import os
# from typing import Dict, List
import csv
import lanconnection
import statistics
import keithley_util
from enum import Enum, auto


# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

class SipmType(Enum):
    MASTER = auto()
    SLAVE = auto()


epsilon = 0.000001
ip = '10.2.0.126'
port = 5555
bar_id = 37

a_master_set_AFE_12 = -260.002
b_master_set_AFE_12 = 16535.2

a_master_measured_AFE_12 = 0.0184174
b_master_measured_AFE_12 = -1.6745

a_slave_set_AFE_12 = -260.2817
b_slave_set_AFE_12 = 16626.31

# a_slave_measured_AFE_12 = -1.591    #Tu chyba zamieniono współczynniki a z b
# b_slave_measured_AFE_12 = 0.0184290 #Tu chyba zamieniono współczynniki a z b

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

a_slave_set_AFE_36 = -260.14
b_slave_set_AFE_36 = 16475.48

a_slave_measured_AFE_36 = 0.0184000
b_slave_measured_AFE_36 = -1.672

resistance = 10.48 * 10**6


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


def set_bit_voltage(voltage_bit: float, connection: lanconnection.LanConnection) \
        -> str:
    result = connection.do_cmd(['setrawdac', bar_id, voltage_bit, voltage_bit])
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
    return sum/number


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


def current_calibration_SiPM_master(a_master_set: float, b_master_set: float, a_master_measured: float, b_master_measured: float, waiting_time: float, start_voltage: float,
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
            voltage_bit = int(a_master_set * start_voltage + b_master_set)
            _headers_master = ('master set U[V]', 'master measured U[V]', 'calculated master set amperage', 'calculated master measured amperage', 'master current measured I[bit]')
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


def current_calibration_SiPM_master2(a_master_set: float, b_master_set: float, a_master_measured: float, b_master_measured: float, waiting_time: float, start_voltage: float,
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
            voltage_bit = int(a_master_set * start_voltage + b_master_set)
            _headers_master = ('master set U[V]', 'master measured U[V]', 'calculated master set amperage', 'calculated master measured amperage', 'master current measured I[bit]', 'master stddev measured current [bit]')
            # _headers_slave = ('slave set U[V]', 'master measured U[V]', 'calculated master set amperage', 'calculated master measured amperage', 'master current measured I[bit]')
            writer = csv.DictWriter(csv_file, fieldnames=_headers_master)
            writer.writeheader()
            time.sleep(waiting_time)

            while voltage < stop_voltage:
                print(voltage)
                set_bit_voltage(voltage_bit, connection)
                time.sleep(step_time)
                measured_voltage = a_master_measured * measure_AFE_voltage_master(connection) + b_master_measured
                current, stddev_current = measure_avg_current2(avg_number, SipmType.MASTER, connection)

                measure_dict = {_headers_master[0]: voltage,
                                _headers_master[1]: measured_voltage,
                                _headers_master[2]: voltage / resistance,
                                _headers_master[3]: measured_voltage / resistance,
                                _headers_master[4]: current,
                                _headers_master[5]: stddev_current}

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


def current_calibration_SiPM_slave(a_slave_set: float, b_slave_set: float, a_slave_measured: float, b_slave_measured: float, waiting_time: float, start_voltage: float,
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

            _headers_slave = ('slave set U[V]', 'slave measured U[V]', 'calculated slave set amperage', 'calculated slave measured amperage', 'slave current measured I[bit]')
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


def current_calibration_SiPM_slave2(a_slave_set: float, b_slave_set: float, a_slave_measured: float, b_slave_measured: float, waiting_time: float, start_voltage: float,
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

            _headers_slave = ('slave set U[V]', 'slave measured U[V]', 'calculated slave set amperage', 'calculated slave measured amperage', 'slave current measured I[bit]', 'stddev slave current measured I[bit]')
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
                                _headers_slave[5]: stddev_current}

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


def breakdown_voltage_determination_master(a_master_set: float, b_master_set: float, a_master_measured: float, b_master_measured: float, waiting_time: float, start_voltage: float,
                                    stop_voltage: float, current_limit: float, voltage_difference: float, avg_number: int, step_time: float, file_name: str):
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

            _headers_master = ('master set U[V]', 'master measured U[V]', 'master measured current I[bit]', 'master stdev measured current  I[bit]', 'Internal temperature [bit]')

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
                measured_current, stddev_measured_current = measure_avg_current2(avg_number, SipmType.MASTER, connection)
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


def breakdown_voltage_determination_master_temp(a_master_set: float, b_master_set: float, a_master_measured: float, b_master_measured: float, waiting_time: float, start_voltage: float,
                                                stop_voltage: float, current_limit: float, voltage_difference: float, avg_current_number: int, avg_temp_number: int, step_time: float, file_name: str):
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

            _headers_master = ('master set U[V]', 'master measured U[V]', 'master measured current I[bit]', 'master stdev measured current  I[bit]', ',master internal temperature [bit]', 'master stdev measured temperature [bit]')

            writer = csv.DictWriter(csv_file, fieldnames=_headers_master)
            writer.writeheader()
            time.sleep(waiting_time)

            voltage_bit = int(a_master_set * start_voltage + b_master_set)
            set_bit_voltage(voltage_bit, connection)
            time.sleep(step_time)

            measured_voltage = a_master_measured * measure_AFE_voltage_master(connection) + b_master_measured
            measured_current, stddev_measured_current = measure_avg_current2(avg_current_number, SipmType.MASTER, connection)
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
            measured_current, stddev_measured_current = measure_avg_current2(avg_current_number, SipmType.MASTER, connection)
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
                measured_current, stddev_measured_current = measure_avg_current2(avg_current_number, SipmType.MASTER, connection)
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


def breakdown_voltage_determination_master_temp_keithley(a_master_set: float, b_master_set: float, a_master_measured: float, b_master_measured: float, waiting_time: float, start_voltage: float,
                                                         stop_voltage: float, current_limit: float, voltage_difference: float, avg_current_number: int, avg_temp_number: int, step_time: float, file_name: str, keithley: keithley_util.Keithley6517):
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

            _headers_master = ('master set U[V]', 'master measured U[V]', 'master measured current I[bit]', 'master stdev measured current  I[bit]', ',master internal temperature [bit]', 'master stdev measured temperature [bit]', 'temp Keithley [C]')

            writer = csv.DictWriter(csv_file, fieldnames=_headers_master)
            writer.writeheader()
            time.sleep(waiting_time)

            voltage_bit = int(a_master_set * start_voltage + b_master_set)
            set_bit_voltage(voltage_bit, connection)
            time.sleep(step_time)

            measured_voltage = a_master_measured * measure_AFE_voltage_master(connection) + b_master_measured
            measured_current, stddev_measured_current = measure_avg_current2(avg_current_number, SipmType.MASTER, connection)
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
            measured_current, stddev_measured_current = measure_avg_current2(avg_current_number, SipmType.MASTER, connection)
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
                measured_current, stddev_measured_current = measure_avg_current2(avg_current_number, SipmType.MASTER, connection)
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


def breakdown_voltage_determination_master_temp_keithley2(a_master_set: float, b_master_set: float, a_master_measured: float, b_master_measured: float, start_voltage: float,
                                                          stop_voltage: float, current_limit: float, voltage_difference: float, avg_current_number: int, avg_temp_number: int, step_time: float,
                                                          keithley: keithley_util.Keithley6517, connection: lanconnection.LanConnection, writer, headers: [str], start_time: float, iter_number: int):
        try:
            voltage_bit = int(a_master_set * start_voltage + b_master_set)
            set_bit_voltage(voltage_bit, connection)
            time.sleep(step_time)

            measured_voltage = a_master_measured * measure_AFE_voltage_master(connection) + b_master_measured
            measured_current, stddev_measured_current = measure_avg_current2(avg_current_number, SipmType.MASTER, connection)
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
            measured_current, stddev_measured_current = measure_avg_current2(avg_current_number, SipmType.MASTER, connection)
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
                measured_current, stddev_measured_current = measure_avg_current2(avg_current_number, SipmType.MASTER, connection)
                temp, stddev_temp  = measure_AFE_temp_avg_master(avg_temp_number, connection)
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


def breakdown_voltage_temp_master_time_dependence(end_date: float, waiting_time: float, a_master_set, b_master_set, a_master_measured, b_master_measured, start_voltage,
                                                          stop_voltage, current_limit, voltage_difference, avg_current_number, avg_temp_number, step_time, file_name: str):
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
                breakdown_voltage_determination_master_temp_keithley2(a_master_set, b_master_set, a_master_measured, b_master_measured, start_voltage,
                                                          stop_voltage, current_limit, voltage_difference, avg_current_number, avg_temp_number, step_time,
                                                          keithley, connection, writer, _headers_master, current_time, iter_number)
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
    calibration(1800, 0, 4095, 64, 12, 0.01, 'calibration_keithley05082022a_master_without_resistor_AFE_37_filter3.csv',
                SipmType.MASTER)