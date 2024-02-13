import pyvisa
from enum import Enum, auto
import time


class MeasurementType(Enum):
    VOLTAGE = auto()
    CURRENT_VOLTAGE = auto()
    CURRENT_CURRENT = auto()

class Keithley6517:

    # def __init__(self, time_util=time):
    #     rm = pyvisa.ResourceManager()
    #     # resources = rm.list_resources()
    #     # self.keithley = rm.open_resource(resources[0])
    #
    #     self.keithley = rm.open_resource("TCPIP0::10.2.0.134::23::SOCKET")
    #     # self.keithley = rm.open_resource("TCPIP0::10.7.1.11::23::SOCKET")
    #     self.keithley.read_termination = "\r\n"
    #
    #     # self.keithley.write('ABORT')
    #     # self.keithley.write('*CLS')
    #     # self.keithley.write('INIT')
    #     print(self.keithley.query('*IDN?'))
    #
    #     self.keithley.write('FORM:ELEM READ, RNUM, TST, ETEM')
    #     self.keithley.write('SYST:TST:TYPE RTCL')
    #     time.sleep(1)
    #     self.keithley.write("SYST:ZCH OFF")
    #     print(self.keithley.query('SYST:ERR?'))
    #     # self.keithley.write(':OUTP ON')
    #     # self.keithley.write(':SOURCE:VOLT ' + str(49.7))
    #     # self.keithley.write("SYST:ZCH OFF")
    #     # time_util.sleep(3)
    #     # self.keithley.write(":CURR:RUNG:AUTO OFF")
    #     # self.keithley.write("SENS:CURR:RANG 2e-5")
    #     # time_util.sleep(5)

    def __init__(self, measurementType=MeasurementType.VOLTAGE, time_util=time):
        rm = pyvisa.ResourceManager()
        # resources = rm.list_resources()
        # self.keithley = rm.open_resource(resources[0])

        self.keithley = rm.open_resource("TCPIP0::10.2.0.134::23::SOCKET")
        # self.keithley = rm.open_resource("TCPIP0::10.7.1.11::23::SOCKET")
        self.keithley.read_termination = "\r\n"

        self.keithley.write('ABORT')
        self.keithley.write('*CLS')
        self.keithley.write('INIT')
        print(self.keithley.query('*IDN?'))
        self.keithley.write('FORM:ELEM READ, RNUM, TST, ETEM')
        self.keithley.write('SYST:TST:TYPE RTCL')
        time_util.sleep(1)
        self.keithley.write("SYST:ZCH OFF")
        time_util.sleep(2)
        print(self.keithley.query('SYST:ERR?'))

        if measurementType == MeasurementType.VOLTAGE or MeasurementType.CURRENT_VOLTAGE:
            self.keithley.write("CONF:VOLT")
            self.keithley.write("SENS:VOLT:NPLC 10")
            time_util.sleep(1)
            self.keithley.write("SENS:VOLT:RANG 100")
            if measurementType == MeasurementType.CURRENT_VOLTAGE:
                self.keithley.write(':OUTP ON')
        else:
            self.keithley.write(":CURR:RUNG:AUTO OFF")
            self.keithley.write("SENS:CURR:RANG 2e-5")
            time_util.sleep(5)


    def __del__(self):
        self.keithley.write("SYST:ZCH ON")
        self.keithley.write(':OUTP OFF')
        self.keithley.write('SYST:TST:TYPE RTCL')

    def measure(self, measurementType: MeasurementType = MeasurementType.VOLTAGE, time_util=time):
        if measurementType == MeasurementType.VOLTAGE or measurementType == MeasurementType.CURRENT_VOLTAGE:
            self.keithley.write("CONF:VOLT")
            self.keithley.write("SENS:VOLT:NPLC 10")
            time_util.sleep(1)
            self.keithley.write("SENS:VOLT:RANG 100")
            time_util.sleep(1)
            result = self.keithley.query('READ?')
        else:
            self.keithley.write("CONF:CURR")
            time_util.sleep(1)
            self.keithley.write("SENS:CURR:NPLC 10")
            time_util.sleep(1)
            self.keithley.write("SENS:CURR:RANG 2e-5")
            time_util.sleep(1)
            result = self.keithley.query('READ?')
        # self.keithley.write("SYST:ZCOR ON")
        # self.keithley.write("SYST:ZCH OFF")
        # time_util.sleep(2)
        # result = self.keithley.query('READ?')

        result = result.split(",")
        measure_dict = {}

        if measurementType == MeasurementType.VOLTAGE or measurementType == MeasurementType.CURRENT_VOLTAGE:
            voltage = float(result[0])
            measure_dict['voltage'] = voltage
        else:
            current = float(result[0])
            measure_dict['current'] = current

        time = result[1]
        date = result[2]
        r_num = int(result[3])
        temp = float(result[4])

        measure_dict['time'] = time
        measure_dict['date'] = date
        measure_dict['rNum'] = r_num
        measure_dict['temp'] = temp
        return measure_dict

    def setVoltage(self, voltage):
        self.keithley.write(':SOURCE:VOLT ' + str(voltage))

    def range(self):
        self.keithley.write("SENS:CURR:RANG 2e-6")

    def nplc(self):
        self.keithley.write("SENS:CURR:NPLC 10")
