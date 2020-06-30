# serial.engine

## Installation

Python:
```
pip install serial.engine
```

This library requires Python3. It was tested extensively on Python 3.7.5 with Ubuntu 19.04.

## How to use

```python
# Device 1
from serialengine import Hub

h = Hub()

h.connect('port1', '/dev/ttyACM0', 9600)

h.writeAll('channel', 'Hello there!')

h.close()
```

```python
# Device 2
from serialengine import Hub

h = Hub()

h.connect('port1', '/dev/ttyACM0', 9600)

print(h.getAll('channel')) # Hello there!

h.close()
```

## Documentation

#### Hub

Hub Constructor:
```
Hub(timeout=2, size=128)
	timeout = Sets the standard timeout of a serial connection (in seconds)
	size = Default read size
```
Hub Methods:
```
Hub.connect(name, port, baud, timeout=2, size=128):
	Connects to another port. The Transport is named 'name', and the target is the port specified.
Hub.close():
	Closes the Hub and all Transports. Also stops all threads.
Hub.getConnections():
	Returns all the Transports to the Hub as 'Transport' objects.
Hub.getAll(channel):
	Reads all data from a specified channel. Returns a list of all responses (or [] if no responses)
Hub.getByName(name, channel):
	Reads all data from a named socket by channel. Returns a list of all responses (or [] if no responses)
Hub.writeAll(channel, data):
	Writes to all connected Transports via the 'channel' with data.
Hub.writToName(name, channel, data):
	Writes to all connected ports with the specified name.
```

#### Transport

Transport Constructor:
```
Transport(port, baud=9600, timeout=2, size=128, name=None)
	port = the serial port to use for the Transport
	baud = the baud rate of the port (must match the remote Transport)
	name = the name of the connection
	timeout = Sets the standard timeout of a port (in seconds)
	size = Default read size
```
Transport Methods:
```
Transport.start():
	Initiates a Transport to a remote Transport or Hub. Starts the thread.
Transport.get(channel):
	Gets data from a channel if it exists. Returns None if no data exists on channel.
Transport.write(channel, data):
	Writes data over a specified channel with the given data.
Transport.close():
	Closes the socket Transport.
```
