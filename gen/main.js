var canvas = document.getElementById("canvas");
var ctx = canvas.getContext("2d");
var ta = document.getElementById("ta");
var data = [];

function isValid(x) {
    return 0 <= x && x < 800;
}

CanvasRenderingContext2D.prototype.circle = function(x, y) {
    this.save();
    this.beginPath();
    this.arc(x, y, 5, 0, Math.PI * 2);
    this.closePath();
    this.fill();
    this.restore();
    data.push([x / 80, (799 - y) / 80]);
};

CanvasRenderingContext2D.prototype.scatter = function(x, y, n = 5, l = 50) {
    for (var i = 0; i < n; i++) {
        var ang = Math.random() * Math.PI * 2;
        var len = Math.random() * l;
        var nx = x + Math.cos(ang) * len;
        var ny = y + Math.sin(ang) * len;
        if (isValid(nx) && isValid(ny)) {
            this.circle(nx, ny);
        }
    }
};

canvas.oncontextmenu = function(event) {
    var x = event.offsetX;
    var y = event.offsetY;
    ctx.scatter(x, y);
};

canvas.onmousedown = function(event) {
    var x = event.offsetX;
    var y = event.offsetY;
    ctx.circle(x, y);
};

function output() {
    var s = "";
    for (var p of data) {
        s += `${p[0]} ${p[1]}\n`;
    }
    ta.innerHTML = s;
    data = [];
    ctx.clearRect(0, 0, 800, 800);
}

function noise(n = 6) {
    var noise = [];
    for (var i = 0; i < n; i++) {
        noise.push([Math.random() * 10, Math.random() * 10]);
    }
    var s = "";
    for (var p of noise) {
        s += `${p[0]} ${p[1]}\n`;
    }
    ta.innerHTML = s;
}
