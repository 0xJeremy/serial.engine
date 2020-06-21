'use strict'

const EventEmitter = require('events').EventEmitter;
const inherits = require('util').inherits;
const SerialPort = require('serialport');

/////////////////
/// CONSTANTS ///
/////////////////

const { ACK, NEWLINE } = require('./constants');
const { TYPE, DATA } = require('./constants');
const { TIMEOUT, SIZE } = require('./constants');
const { STATUS, CLOSING } = require('./constants');
const { READY } = require('./constants');

///////////////////////////////////////////////////////////////

////////////////////////
/// CONNECTION CLASS ///
////////////////////////

function connection(port, baud, timeout=TIMEOUT, size=SIZE) {
	EventEmitter.call(this);
	this.port = port;
	this.baud = baud;
	this.canWrite = true;
	this.channels = {};
	this.timeout = timeout;
	this.opened = false;
	this.size = size;
	this.msgBuffer = '';
	this.serial = null;
	this.parser = null;

	this.start = function() {
		return new Promise((resolve, reject) => {
			this.serial =  new SerialPort(this.port, { baudRate: this.baud });
			this.parser = this.serial.pipe(new SerialPort.parsers.Ready({ delimiter: READY }));
			this.parser.on('ready', () => {
				this.__run();
				this.opened = true;
				resolve();
			});
		});
	}

	this.__run = function() {
		this.opened = true;
		this.parser.on('data', (bytes) => {
			this.msgBuffer += bytes.toString();
			if(this.msgBuffer != '' && this.msgBuffer != '\n') {
				var data = this.msgBuffer.split('\n');

				for(var i = 0; i < data.length; i++) {
					try {
						if(data[i] == '') {
							continue;
						}
						var msg = JSON.parse(data[i]);
						this.__cascade(msg[TYPE], msg[DATA]);
						this.channels[msg[TYPE]] = msg[DATA];

						this.emit(msg[TYPE], msg[DATA]);
						this.emit('data', msg);
					} catch(err) {console.log(err)};
				}

			}
		});
		this.serial.on('end', () => {
			this.emit('end');
		});

		this.serial.on('error', (err) => {
			this.emit('warning', err);
		});
	}
	

	this.__cascade = function(mtype, mdata) {
		if(mtype == ACK) {
			this.canWrite = true;
		}
		if(mtype == STATUS) {
			if(mdata == CLOSING) {
				this.__close();
			}
		}
	}

	this.__close = function() {
		this.opened = false;
		this.serial.close();
	}

	/////////////////
	/// INTERFACE ///
	/////////////////

	this.get = function(channel) {
		return this.channels[channel];
	}

	this.write = function(dataType, data) {
		if(!this.opened) {
			new Error('Port not opened');
		}
		var msg = {
			'type': dataType.replace('\n', ''),
			'data': data.replace('\n', '')
		};
		this.serial.write(JSON.stringify(msg) + NEWLINE);
	}

	this.close = function() {
		try {
			this.write(STATUS, CLOSING)
		} catch { }
		this.__close()
	}

}

inherits(connection, EventEmitter);

module.exports = exports = connection;
