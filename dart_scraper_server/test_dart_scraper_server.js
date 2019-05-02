var net = require('net');

var client = new net.Socket();

client.connect(8989, '127.0.0.1', function() {
  console.log('Connected');
  data = JSON.stringify({'opcode': 'dart_download_file', 'data': {'crp_cd_list':['005930', '003284'], 'path':'C:\\Users\\swjo\\Desktop\\socekt_test', 'start_dt':'20180101'}})
  client.write(data);
});

client.on('data', function(data) {
  console.log(JSON.parse(data));
  data = JSON.stringify({'opcode': 'dart_shut_down', 'data': null});
  client.write(data);
});

client.on('close', function() {
	console.log('Connection closed');
});