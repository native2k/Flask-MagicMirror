// http://stackoverflow.com/a/2998874/5441252
function zeroPad(num, places) {
  var zero = places - num.toString().length + 1;
  return Array(+(zero > 0 && zero)).join("0") + num;
}

function getTime(adjHour, adjMin) {
    var d = new Date();
    var n = d.getHours() - adjHour;
    var m = zeroPad(d.getMinutes(), 2);
    var time = (String(n) + ':' + String(m));
    document.getElementById('updatetime').innerHTML = time;
    console.log(time);
}

setInterval(function() {
    getTime(5, 0);
}, 1000);

setTimeout(function() {
    window.location.reload(true);
}, 60000);