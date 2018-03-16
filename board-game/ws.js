var WebSocketServer = require('ws').Server,
  wss = new WebSocketServer({port: 40510})

let players = [];
wss.on('connection', function (ws) {
    let numberOfPlayers = 0;
    let alivePlayers = 0;
    let field = [];
    let playerOnMove = 0;

    // ws.send("Waiting cin game lobby");
    while (true) {
        /* if button push - new game is started */
        if (true) {
            // calculate the number of player / the number of jacks connected at the beginning
            numberOfPlayers = getNumberOfPlayers();
            alivePlayers = numberOfPlayers;
            generatePlayersObj(numberOfPlayers);
            // generate field
            field = generateField();
            invokeLEDs(field);

            // game cycle
            while(true) {
                let diceFlag = false;
                let playerPosition = -1;
                let playerDiceValue = 0;
                
                playerOnMove = getPlayerOnMove(playerOnMove);
                ws.send(JSON.stringify({
                    type: "player-information",
                    playerToMove: playerOnMove
                }));
                /*one person turn*/
                while (true && diceFlag !== true)
                /*if dice button pushed*/
                if (true) {
                    playerDiceValue = Math.round(Math.random() * 5) + 1;
                    ws.send(JSON.stringify({
                        type: "dice",
                        value: `${playerDiceValue}`
                    }));
                    diceFlag = true;
                    playerPosition = getPlayerPosition();
                }


                // playerPosition = getPlayerPosition();
                if (diceFlag === true && playerPosition !== -1) {
                    // if (playerPosition + playerDiceValue === getPlayerPosition()) {
                    if (true) {
                        /*when the dice button is clicked and the player has moved to the right place*/
                        handleCorretFieldOptions(playerPosition + playerDiceValue, field, playerOnMove);
                    } else {
                        /*not on right position*/
                        penalizePlayer(playerOnMove);
                    }
                    break;
                } else if (playerPosition === -1){
                    /*player in air*/

                }



                if (alivePlayers === 1) {
                    // someone won


                    players = [];
                    break;
                }
            }
        }
    }
});

function handleCorretFieldOptions(playerPostion, field, player) {
    let color = field[playerPostion].color;
    if(color === "red") {
        //red ask a question if answered wrong deal damage
        askQuestion(player);
    }
    if(color === "green") {
        //green asks a question if answered correctly restore 1
        askQuestion(player);
    }
}

function invokeLEDs(field) {
    /*Sets diod's GPIO's*/
}

function generatePlayersObj() {
    players = [];
    let boardInfo = getBoardInfo();
    // for (let i = 0; i < boardInfo.size; i++) {
    for (let i = 0; i < 4; i++) {
        players.push(
            {
                id: i,
                sensorId: 0,
                hp: 10,
                turns: 0,
                position: 0,
            }
        );
    }
}

function getBoardInfo() {
    /*Returns the S_id's and current position for them*/
    return [];
}

function penalizePlayer(playerId) {
    players[playerId].hp -= 2;
}

function getPlayerPosition() {
    return 0;
}
/*ws.on('message', function (message) {
            console.log('received: %s', message)
            });
        */

function getPlayerOnMove(playerOnMove) {
    if (playerOnMove + 1 > players.length - 1) {
        return 0;
    } else {
        return playerOnMove + 1
    }
}

function getNumberOfPlayers() {
    //TODO
    return 0;
}

function generateField() {
    let result = [];
    let color = 'green';
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
        [a[i], a[j]] = [a[j], a[i]];
    }
    return a;
}