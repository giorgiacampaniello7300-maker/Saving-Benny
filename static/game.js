"use strict";

const howToPlay = document.querySelector("#how-to-play");
const start = document.querySelector("#start");
const instructions = document.querySelector("#instructions");
const backButton = document.querySelector("#back-button");
const game = document.querySelector("#game");
const gameOver = document.querySelector("#game-over");
const victory = document.querySelector("#victory");
const newGame = document.querySelector("#new-game");
const defeatMenu = document.querySelector("#defeat-menu");
const victoryMenu = document.querySelector("#victory-menu");
const tryAgain = document.querySelector("#try-again");
const playAgain = document.querySelector("#play-again");
const saveExit = document.querySelector("#save-exit");

instructions.style.display = "none";
game.style.display = "none";
gameOver.style.display = "none";
victory.style.display = "none";

howToPlay.addEventListener("click", function() {
    start.style.display = "none";
    instructions.style.display = "block";
});

backButton.addEventListener("click", function() {
    instructions.style.display = "none";
    start.style.display = "block";
});

newGame.addEventListener("click", function() {
    start.style.display = "none";
    game.style.display = "block";
});

defeatMenu.addEventListener("click", function() {
    gameOver.style.display = "none";
    start.style.display = "block";
});

victoryMenu.addEventListener("click", function() {
    victory.style.display = "none";
    start.style.display = "block";
});

tryAgain.addEventListener("click", function() {
    gameOver.style.display = "none";
    game.style.display = "block";
});

playAgain.addEventListener("click", function() {
    victory.style.display = "none";
    game.style.display = "block";
});

saveExit.addEventListener("click", function() {
    game.style.display = "none";
    start.style.display = "block";
});