'use strict'

var data = {
	/////////////////////////
	/// MESSAGE CONSTANTS ///
	/////////////////////////

	NEWLINE : '\n',
	TYPE    : 'type',
	DATA    : 'data',

	////////////////////////
	/// SERIAL CONSTANTS ///
	////////////////////////

	SIZE        : 128,
	TIMEOUT     : 2,
	BAUD_RATE   : 9600,

	////////////////////
	/// STATUS TYPES ///
	////////////////////
	
	STATUS    : '__status',
	CLOSING   : '__closing',
	ACK       : '__ack',
	READY     : Buffer.from('READY')
}

module.exports = exports = data;
