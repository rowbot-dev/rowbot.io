
const WebSocket = require('ws');
const http = require('http');

// Should be by id for filtering
var sockets = {};

// set up message http server
const message_server = http.createServer(function (request, response) {
  if (request.method == 'POST') {
    let body = '';
    request.on('data', function (data) {
      body += data;
    });
    request.on('end', function () {
      var payload = JSON.parse(body);

      // only send if socket key matches keys
      Object.keys(sockets).forEach(function (key) {
        let socket = sockets[key];
        if (payload.keys.indexOf(key) !== -1) {
          socket.send(JSON.stringify(payload.data));
        }
      });
      response.end();
    });
  } else if (request.method == 'GET') {
    var [previous, current] = request.url.slice(1).split('.');
    delete sockets[previous];
    sockets[current] = undefined; // prepare for connection
    response.end();
  }
});
message_server.keepAliveTimeout = 20000;
message_server.listen(3000, 'localhost', function (error) {
  if (error) {
    return console.log('Error', error);
  }

  console.log('Message server is listening on localhost:3000');
});

// websocket server
const websocket_server = new WebSocket.Server({port: 4000, host: 'localhost'});
websocket_server.on('connection', function (socket) {
  socket.on('message', function (message) {
    if (message in sockets) {
      sockets[message] = socket;
      console.log(`Connection established to ${message}`);
    }
  });
});
