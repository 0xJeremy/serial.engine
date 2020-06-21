<div align="center">
  <img src="https://raw.githubusercontent.com/0xJeremy/serial.engine/master/graphics/Logo.png">
</div>

## Installation

[Python](https://pypi.org/project/serial.engine/):
```
pip install serial.engine
```

[Node.js](https://www.npmjs.com/package/serial.engine):
```
npm install serial.engine
```

This library requires Python3 or Node.js (>= v10). It was tested extensively on Python 3.7.5 and Node.js v10.15.2 with Ubuntu 19.04.

## Features
Serial.engine enables real-time bidirectional communication between serial devices. It is implemented in Python and Node.js, with support for C++ based embedded processors (i.e., Arduino). The interface between each language is extremely similar, allowing plug and play communication, and easy swapping between languages. It is optimized for high-speed, reliable information transfer.

Its main features are:

#### Speed
Very litte overhead is used to serialize and send the messages, with the priority being speed and reliability. Serial.engine operates using JSON serialization, and verifies all incoming and outgoing messages meet the proper specification before being sent.

#### Easy to use
This library was designed to lower the barrier to entry as much as possible. As such, it was built as a wrapper for serial device interfaces to send large amount of information quickly and reliably.

## Documentation

[Python Documentation](https://github.com/0xJeremy/serial.engine/blob/master/python/README.md)

[Node.js Documentation](https://github.com/0xJeremy/serial.engine/blob/master/nodejs/README.md)