import serial
# import time
import multiprocessing

## Change this to match your local settings
# SERIAL_PORT = '/dev/ttyACM0'
SERIAL_PORT = '/dev/ttyUSB0'
SERIAL_BAUDRATE = 115200


class SerialProcess(multiprocessing.Process):

    def __init__(self, input_queue, output_queue):
        multiprocessing.Process.__init__(self)
        self.input_queue = input_queue
        self.output_queue = output_queue
        self.sp = serial.Serial(SERIAL_PORT, SERIAL_BAUDRATE, timeout=1)

    def close(self):
        self.sp.close()

    def writeSerial(self, data):
        self.sp.write(bytearray(data, encoding="utf-8"))
        # time.sleep(1)

    def readSerial(self):
        return self.sp.readline().replace(b"\n", b"")

    def run(self):

        self.sp.flushInput()

        while True:
            # look for incoming tornado request
            if not self.input_queue.empty():
                data = self.input_queue.get()

                # send it to the serial device
                self.writeSerial(data)
                print("writing to serial: " + data)

            # look for incoming serial data
            if self.sp.inWaiting() > 0:
                data = self.readSerial()
                print("reading from serial: " + str(data.decode("utf-8", errors='ignore')))
                # print("reading from serial: " + str(data))
                # send it back to tornado
                self.output_queue.put(data)
