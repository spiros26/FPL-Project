document.addEventListener("DOMContentLoaded", function () {
    const btnAdd = document.getElementById("btnAdd");
    const btnRemove = document.getElementById("btnRemove");
    const addPlayer = document.getElementById("addPlayer");
    const squad = document.querySelector(".squad");

    btnAdd.addEventListener("click", function () {
        const selectedPlayer = addPlayer.value;
        const newPlayer = document.createElement("div");
        newPlayer.className = "player";
        newPlayer.textContent = selectedPlayer;
        squad.appendChild(newPlayer);
    });

    btnRemove.addEventListener("click", function () {
        const players = squad.getElementsByClassName("player");
        if (players.length > 0) {
            squad.removeChild(players[players.length - 1]);
        }
    });
});
