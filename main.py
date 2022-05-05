# This is a sample Python script.
import keithley_util
import time
import os
# from typing import Dict, List
import csv
import lanconnection
from enum import Enum, auto


# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

class SipmType(Enum):
    MASTER = auto()
    SLAVE = auto()

epsilon = 0.000001
ip = '10.2.0.126'
port = 5555
bar_id = 12


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


def set_bit_voltage(voltage_bit: int, connection: lanconnection.LanConnection) \
        -> (float, int, int, float, int, int):
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


def measure_AFE_all(connection: lanconnection.LanConnection) -> (int, int, int, int):
    measured_master_voltage = connection.do_cmd(['adc', bar_id, 3])[1]
    measured_slave_voltage = connection.do_cmd(['adc', bar_id, 4])[1]
    measured_master_current = connection.do_cmd(['adc', bar_id, 5])[1]
    measured_slave_current = connection.do_cmd(['adc', bar_id, 6])[1]
    return measured_master_voltage, measured_slave_voltage, measured_master_current, measured_slave_current


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
            time.sleep(waiting_time)
            current_time = time.time()
            print(current_time)
            voltage_result = connection.do_cmd(['setdac', bar_id, set_voltage, set_voltage])
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


def calibration(waiting_time: float, start: int, stop: int, step_voltage: int, step_time: float,
                step_keithley_time: float, file_name: str, sipm_type: SipmType):
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

                measure_dict = {}
                time.sleep(step_time)

                result_keithley = keithley.measure()
                r_num = result_keithley['rNum']
                while result_keithley['rNum'] == r_num:
                    r_num = result_keithley['rNum']
                    time.sleep(step_keithley_time)
                    result_keithley = keithley.measure()

                measure_dict[_headers_master[0]] = voltage_bit
                if sipm_type == SipmType.MASTER:
                    measure_dict[_headers_master[1]] = measure_AFE_voltage_master(connection)
                else:
                    measure_dict[_headers_slave[1]] = measure_AFE_voltage_slave(connection)
                measure_dict[_headers_master[2]] = result_keithley['voltage']

                voltage_bit += step_voltage

                writer.writerow(measure_dict)
                print(voltage_bit)

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


if __name__ == '__main__':
    # stability(1651239000, 2, 0.1, 59.5, 5, 'stability_keithley6.csv')
    # stability(1651239300, 2, 0.1, 59.5, 10, 'stability_keithley7.csv')
    # stability(1651284000, 1, 0.01, 59.5, 0, 'stability_keithley8.csv')
    # stability(1651557600, 20, 0.1, 55.5, 30, 'stability_keithley9.csv')
    # calibration(60, 0, 4095, 64, 1, 0.01, 'calibration_keithley.csv', SipmType.MASTER)
    # calibration(300, 0, 4095, 16, 5, 0.1, 'calibration_keithley3.csv', SipmType.MASTER)
    calibration(600, 0, 4095, 16, 10, 0.1, 'calibration_keithley4.csv', SipmType.MASTER)
