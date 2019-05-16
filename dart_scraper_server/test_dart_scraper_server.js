var net = require('net');

if (process.argv.length < 3) {
  console.log('Port is not defined')
  process.exit(-1);
}
const port = process.argv[2]

var client = new net.Socket();

var client_state = null;

const STATE_READING = 0;
const STATE_SAVING = 1;
const STATE_DOWNLOADING = 2;
const STATE_SHUTDOWN = 3;

function reading_config() {
  console.log('Reading config file');
  client_state = STATE_READING;
  let data = JSON.stringify({'opcode': 'dart_get_api_key', 'data': null});
  client.write(data);
}

function saving_config(api_key) {
  console.log('Saving config file')
  client_state = STATE_SAVING;
  let data = JSON.stringify({'opcode': 'dart_set_api_key', 'data': api_key})
  client.write(data);
}

function downloading() {
  console.log('Downloading')
  client_state = STATE_DOWNLOADING;
  let data = JSON.stringify({'opcode': 'dart_download_file', 'data': {'crp_cd_list':['005930', '003284'], 'path':'socekt_test', 'start_dt':'20180101'}})
  client.write(data);
}

function shutdown() {
  console.log('Shutdown')
  client_state = STATE_SHUTDOWN;
  let data = JSON.stringify({'opcode': 'dart_shut_down', 'data': null});
  client.write(data);
}

client.connect(port, '127.0.0.1', function() {
  console.log('Connected');
  reading_config();
});

client.on('data', function(data) {
  let recv = JSON.parse(data)
  console.log('=====Data Recv=====')
  console.log(recv)
  console.log('===================')
  if (client_state === STATE_READING) {
    saving_config(recv['data']);
  } else if (client_state ===  STATE_SAVING) {
    downloading();
  } else {
    shutdown();
  }
});

client.on('close', function() {
	console.log('Connection closed');
});