var WebSocketServer = require('ws').Server,
  wss = new WebSocketServer({port: 40510})

let players = [];
wss.on('connection', function (ws) {
    let numberOfPlayers = 0;
    let alivePlayers = 0;
    let field = [];

    ws.send("Waiting cin game lobby");
    while (true) {
        /* if button push - new game is started */
        if (true) {
            // calculate the number of player / the number of jacks connected at the beginning
            numberOfPlayers = getNumberOfPlayers();
            alivePlayers = numberOfPlayers;
            // generate field
            field = generateField();
            
            // game cycle
            while(true) {
                let diceFlag = false;
                let playerPosition = -1;
                let playerDiceValue = 0;
                
                let playerOnMove = getPlayerOnMove();
                /*one person turn*/
                while (true)
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


                let playerPosition = getPlayerPosition();
                if (diceFlag === true && playerPosition !== -1) {
                    if (playerPosition + playerDiceValue === playerPosition) {
                        /*when the dice button is clicked and the player has moved to the right place*/
                    } else {
                        /*not on right position*/
                        penalizePlayer(playerOnMove);
                    }
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

function penalizePlayer(playerId) {

}

function getPlayerPosition() {
    return 0;
}
/*ws.on('message', function (message) {
            console.log('received: %s', message)
            });
        */

function getPlayerOnMove() {
    return 0;
}

function getNumberOfPlayers() {
    //TODO
    return 0;
}

function generateField() {
    let result = [];


}