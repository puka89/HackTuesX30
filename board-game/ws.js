"use strict";
var WebSocketServer = require('ws').Server,
    wss = new WebSocketServer({port: 40510});
// var sensor = require('ds18b20-raspi');

var gpio = require('rpi-gpio');
var colors = ["purple", "blue", "white", "black"];
var connectionPool = [];

var gameState = {
    started: false,
    players: [],
    playerOnMove: -1,
    connectedPlayers: 0,
    lastDiceValue: 0
};

gpio.setup(9, gpio.DIR_IN, gpio.EDGE_BOTH); // dice, start
gpio.setup(7, gpio.DIR_IN, gpio.EDGE_BOTH); // true button
gpio.setup(8, gpio.DIR_IN, gpio.EDGE_BOTH); // false button
gpio.setup(2, gpio.DIR_IN, gpio.EDGE_BOTH); // field_1
gpio.setup(3, gpio.DIR_IN, gpio.EDGE_BOTH); // field_2
gpio.setup(17, gpio.DIR_IN, gpio.EDGE_BOTH); // field_3
gpio.setup(27, gpio.DIR_IN, gpio.EDGE_BOTH); // field_4
gpio.setup(22, gpio.DIR_IN, gpio.EDGE_BOTH); // field_5
gpio.setup(5, gpio.DIR_IN, gpio.EDGE_BOTH); // field_6
gpio.setup(6, gpio.DIR_IN, gpio.EDGE_BOTH); // field_7
gpio.setup(13, gpio.DIR_IN, gpio.EDGE_BOTH); // field_8
gpio.setup(19, gpio.DIR_IN, gpio.EDGE_BOTH); //field_9
gpio.setup(26, gpio.DIR_IN, gpio.EDGE_BOTH); //field_10
gpio.setup(18, gpio.DIR_IN, gpio.EDGE_BOTH); //field_11
gpio.setup(23, gpio.DIR_IN, gpio.EDGE_BOTH); //field_12
gpio.setup(24, gpio.DIR_IN, gpio.EDGE_BOTH); //field_13
gpio.setup(25, gpio.DIR_IN, gpio.EDGE_BOTH); //field_14
gpio.setup(12, gpio.DIR_IN, gpio.EDGE_BOTH); //field_15
gpio.setup(16, gpio.DIR_IN, gpio.EDGE_BOTH); //field_16

var sensors = require('ds1820-temp');
var gpio = require('rpi-gpio');

gpio.on('change', function(channel, value) {
    // if (channel == 9) {
    //     /*start button dice*/
    //     console.log("start/dice");
    // }
    console.log('Channel ' + channel + ' value is now ' + value);
});
// listDevices([cb(error, result)]);

wss.on('connection', function (ws) {
    connectionPool.push(ws);
    console.log("new connection - number: " + connectionPool.length + 1);

    // var list = sensor.list();
    // listDevices([cb(error, result)]);
    sensors.listDevices(function (err, devices) {
        if (err) {
            console.log('An error occurred', err);
            // return;
        }

        console.log('Read all devices', devices);
    });

    // sendAllClients();
});

var ws281x = require('rpi-ws281x-native');

var NUM_LEDS = parseInt(16),
    pixelData = new Uint32Array(NUM_LEDS);

ws281x.init(NUM_LEDS);

// ---- trap the SIGINT and reset before exit
process.on('SIGINT', function () {
    ws281x.reset();
    process.nextTick(function () { process.exit(0); });
});


/*
for (var i = 0; i < NUM_LEDS; i++) {
    pixelData[i] = colorwheel((1 + i) % 256);

}

ws281x.render(pixelData);
*/

// ---- animation-loop
var offset = 0;
setInterval(function () {
    for (var i = 0; i < NUM_LEDS; i++) {
        pixelData[i] = colorwheel((offset + i) % 256);
    }

    offset = (offset + 1) % 256;
    ws281x.render(pixelData);
}, 1000 / 30);

console.log('Press <ctrl>+C to exit.');


// rainbow-colors, taken from http://goo.gl/Cs3H0v
function colorwheel(pos) {
    pos = 255 - pos;
    if (pos < 85) { return rgb2Int(255 - pos * 3, 0, pos * 3); }
    else if (pos < 170) { pos -= 85; return rgb2Int(0, pos * 3, 255 - pos * 3); }
    else { pos -= 170; return rgb2Int(pos * 3, 255 - pos * 3, 0); }
}

function rgb2Int(r, g, b) {
    return ((r & 0xff) << 16) + ((g & 0xff) << 8) + (b & 0xff);
}
/*Generating random field with 10 green and 6 red fields*/
function generateField() {
    let result = [];
    let color = "green";

    for (let i = 0; i < 16; i++) {
        if (i >= 10 && color !== "red") {
            color = "red";
        }
        result.push(
            {
                color: color,
                owner: "game"
            }
        )
    }

    return shuffle(result);
}

/*
* The fallowing part of code is taken from: https://stackoverflow.com/questions/6274339/how-can-i-shuffle-an-array*/
function shuffle(a) {
    for (let i = a.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        let temp = a[i];
        a[i] = a[j];
        a[j] = temp;
        // [a[i], a[j]] = [a[j], a[i]];
    }
    return a;
}

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
    return Math.round(Math.random() * 5) + 1;
}

/*when new game is started*/
function initializeNewGame() {
    gameState.started = true;
    gameState.players = initPlayers();
}

function lightLEDs() {
    gpio.setup(18, gpio.DIR_OUT, write);
}

function write() {
    gpio.write(7, true, function(err) {
        if (err) throw err;
        console.log('Written to pin');
    });
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
