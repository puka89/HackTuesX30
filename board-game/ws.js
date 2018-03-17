"use strict";
var WebSocketServer = require('ws').Server,
    wss = new WebSocketServer({port: 40510});
var sensor = require('ds18b20-raspi');

var colors = ["purple", "blue", "white", "black"];
var connectionPool = [];
var gameState = {
    started: false,
    players: [],
    playerOnMove: -1,
    connectedPlayers: 0,
    lastDiceValue: 0
};
wss.on('connection', function (ws) {
    connectionPool.push(ws);
    console.log("new connection - number: " + connectionPool.length + 1);

    var list = sensor.list();
    console.log(list);

// async version
    sensor.list(function (err, deviceIds) {
        if(err) {
            console.log(err);
        } else {
            console.log(deviceIds);
        }
    });


    // sendAllClients();
});



function sendNewClientInitalInfo(ws) {
    ws.send(JSON.stringify({
        type: "game",
        game: gameState
    }));
}

/*when event is handled and something has changed*/
function sendAllClients(data) {
    var dataToSend = data;

    if (!data) {
        /*in case the data is undefined a.k.a is not passed as argument or is false, null, undefined, 0*/
        dataToSend = gameState;
    }

    connectionPool.map(function (value, index, array) {
        console.log("client_id_connected: " + index);
    });
}

function getDiceValue() {

}

/*when new game is started*/
function initializeNewGame() {
    gameState.started = true;
    gameState.players = initPlayers();
}

/*close game when is finished*/
function closeGame() {
    gameState = {};
}

/*initializing player*/
function initPlayers() {
    var players = [];
    for (var i = 0; i < 4; i++) {
        players.push(
            {
                id: i,
                sensorId: "12312",
                alive: true,
                color: colors[i],

            }
        );
    }
}

/*Returns the number of alive players*/
function getAlivePlayers() {
    var counter = 0;
    gameState.players.map(function (value) {
        if (value.alive) {
            counter++;
        }
    })

    return counter;
}