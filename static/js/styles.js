function getTime(adj) {
    var d = new Date();
    var n = d.getHours() - adj;
    var m = d.getMinutes() - adj;
    var time = (String(n) + ':' + String(m));
    document.getElementById('updatetime').innerHTML = time;
    console.log(time);
}

setInterval(function() {
    getTime(5);
}, 5000);