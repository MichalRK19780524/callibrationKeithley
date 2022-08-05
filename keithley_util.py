import pyvisa
import time


class Keithley6517:
    def __init__(self):
        rm = pyvisa.ResourceManager()
        resources = rm.list_resources()
        # self.keithley = rm.open_resource(resources[0])

        self.keithley = rm.open_resource("TCPIP0::10.2.0.71::23::SOCKET")
        self.keithley.read_termination = "\r\n"

        print(self.keithley.query('*IDN?'))

        self.keithley.write('FORM:ELEM READ, RNUM, TST, ETEM')
        self.keithley.write('SYST:TST:TYPE RTCL')
        print(self.keithley.query('SYST:ERR?'))

    def measure(self):
        result = self.keithley.query('FETCH?')
        result = result.split(",")
        measure_dict = {}
        voltage = float(result[0])
        time = result[1]
        date = result[2]
        r_num = int(result[3])
        temp = float(result[4])
        measure_dict['voltage'] = voltage
        measure_dict['time'] = time
        measure_dict['date'] = date
        measure_dict['rNum'] = r_num
        measure_dict['temp'] = temp
        return measure_dict
