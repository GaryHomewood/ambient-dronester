var DronesterApp = DronesterApp || {};

DronesterApp.Main = function() {
    var play = function(el) {
        // toggle the play button icon
        const playerIcon = el.getElementsByTagName('img')[0];
        if (playerIcon.src.indexOf('play') != -1) {
            playerIcon.src = "/static/img/pause.svg";
            document.getElementById('btn-text').textContent = "PAUSE";
        } else {
            playerIcon.src = "/static/img/play.svg"
            document.getElementById('btn-text').textContent = "PLAY";
        }

        const center = document.getElementById('center').value
        const wave = document.getElementById('wave').value
        const volume = document.getElementById('volume').value;

        fetch('/play', {
            method: 'POST',
            credentials: 'same-origin',
            headers: {
                'content-type': 'application/json'
            },
            body: JSON.stringify({
                center: center,
                wave: wave,
                volume: volume
            })
        });
    };

    var changeVolume = function(volume) {
        fetch('/volume', {
            method: 'POST',
            headers: {
                'content-type': 'application/json'
            },
            body: JSON.stringify({
                volume: volume
            })
        });
    }

    return {
        play: play,
        changeVolume: changeVolume
    };
}();
