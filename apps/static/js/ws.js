function WSSHClient() {
};

WSSHClient.prototype.connect = function (options) {

    if (window.WebSocket) {
        this._connection = new WebSocket("ws://192.168.10.45:7777/ws");
    }
    else if (window.MozWebSocket) {
        this._connection = MozWebSocket("ws://192.168.10.45:7777/ws");
    }
    else {
        options.onError('WebSocket Not Supported');
        return;
    }

    this._connection.onopen = function () {
        options.onConnect();
    };

    this._connection.onmessage = function (evt) {
        var data = evt.data.toString();
        options.onData(data);
    };


    this._connection.onclose = function (evt) {
        options.onClose();
    };
};

WSSHClient.prototype.send = function (data) {
    this._connection.send(JSON.stringify(data));
};

WSSHClient.prototype.sendInitData = function (options) {
    var data = {
        host: options.host,
        remote_user: options.remote_user
    }
    this._connection.send(JSON.stringify({"tp": "init", "data": data}))
}

WSSHClient.prototype.sendClientData = function (data) {
    this._connection.send(JSON.stringify({"tp": "client", "data": data}))
}

WSSHClient.prototype.close = function(data){
   this._connection.close()
}

var client = new WSSHClient();
