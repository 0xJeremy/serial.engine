from threading import Thread, Lock
from .transport import Transport
import serial

#################
### CONSTANTS ###
#################

from .constants import TIMEOUT, SIZE

###############################################################

#################
### HUB CLASS ###
#################


class Hub:
    def __init__(self, timeout=TIMEOUT, size=SIZE):
        self.timeout = timeout
        self.size = size
        self.transports = []

    def connect(self, name, port, baud, timeout=self.timeout, size=self.size):
        t = Transport(port, baud, timeout=timeout, size=size, name=name).start()
        self.transports.append(t)
        return self

    def close(self):
        for t in self.transports:
            t.close()

    def getConnections(self):
        return self.transports

    ##########################
    ### INTERFACE, GETTERS ###
    ##########################

    def getAll(self, channel):
        data = []
        for t in self.transports:
            tmp = t.get(channel)
            if tmp is not None:
                data.append(tmp)
        return data

    def getByName(self, name, channel):
        data = []
        for t in self.transports:
            if t.name == name:
                tmp = t.get(channel)
                if tmp is not None:
                    data.append(tmp)
        return data

    ##########################
    ### INTERFACE, WRITERS ###
    ##########################

    def writeAll(self, channel, data):
        for t in self.transports:
            t.write(channel, data)
        return self

    def writeToName(self, name, channel, data):
        for t in self.transports:
            if t.name == name:
                t.write(channel, data)
        return self
