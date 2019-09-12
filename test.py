from pymodbus.constants import Endian
from pymodbus.payload import BinaryPayloadDecoder
from pymodbus.client.sync import ModbusTcpClient as ModbusClient
import requests
from time import sleep
import time
asset_names = ['Asset 156', 'Asset 155', 'Asset 160', 'Asset 150', 'Asset 152', 'Asset 153']
with ModbusClient('10.60.10.2', port=502) as client:
    while 1:
        registers = client.read_holding_registers(49152, 16).registers
        decoder = BinaryPayloadDecoder.fromRegisters(registers, Endian.Big)
        counters = []
        for i in range(6):
            lsw = decoder.decode_16bit_uint()
            msw = decoder.decode_16bit_uint() << 16
            print(msw)
            print(lsw)

            counters.append(lsw + msw)
            #counters.append(decoder.decode_32bit_uint())
        print(counters)

        timestamp = int(time.time()*1000)

        ci = 0
        counter_data = ""
        counter_data += '# TYPE parts counter\n'
        for counter in counters:
            counter_data += 'parts{{instance="{2}"}} {0} {1}\n'.format(counter, timestamp, asset_names[ci])
            ci += 1
        print(counter_data)
        #r = requests.post('http://localhost:9091/metrics/job/gluers', data=counter_data)
        #print(r.url)
        #print(r.text)
        sleep(1)

    client.close()
