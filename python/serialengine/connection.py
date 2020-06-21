from threading import Thread, Lock
from json import dumps as dictToJson
from json import loads as jsonToDict
from json.decoder import JSONDecodeError
import serial

#################
### CONSTANTS ###
#################

from .constants import ACK, NEWLINE, READY
from .constants import TYPE, DATA
from .constants import TIMEOUT, SIZE
from .constants import STATUS, CLOSING
from .constants import BAUD_RATE

###############################################################

########################
### CONNECTION CLASS ###
########################


class connection:
    def __init__(self, port, baud=BAUD_RATE, timeout=TIMEOUT, size=SIZE):
        self.canWrite = True
        self.channels = {}
        self.size = size
        self.timeout = timeout
        self.stopped = False
        self.opened = False
        self.port = port
        self.baud = baud
        self.serial = serial.Serial(port, baudrate=baud, timeout=self.timeout)
        self.lock = Lock()

    def __run(self):
        tmp = ""
        while True:
            if self.stopped:
                self.serial.close()
                return

            tmp += self.serial.read(self.size).decode()

            if tmp == READY:
                self.opened = True
                tmp = ""

            if tmp != "":
                data = tmp.split("\n")
                for i in range(len(data)):
                    try:
                        msg = jsonToDict(data[i])
                    except JSONDecodeError:
                        continue

                    self.__cascade(msg[TYPE], msg[DATA])
                    self.channels[msg[TYPE]] = msg[DATA]
                    data[i] = ""

                tmp = "".join(data)

    def __cascade(self, mtype, mdata):
        if mtype == ACK:
            self.canWrite = True
        if mtype == STATUS:
            if mdata == CLOSING:
                self.__close()
        return

    def __close(self):
        self.opened = False
        self.stopped = True

    #################
    ### INTERFACE ###
    #################

    def start(self):
        Thread(target=self.__run, args=()).start()
        while not self.opened:
            pass
        return self

    def get(self, channel):
        with self.lock:
            if channel in self.channels.keys():
                return self.channels[channel]
            return None

    def write(self, channel, data):
        if self.opened:
            with self.lock:
                msg = {TYPE: channel.replace("\n", ""), DATA: data.replace("\n", "")}
                self.serial.write(dictToJson(msg).encode() + NEWLINE)

    def close(self):
        self.write(STATUS, CLOSING)
        self.__close()
