export function Circle(x, y, radius, c){
    this.x = Math.random() * (innerWidth - radius * 2) + radius;
    this.y = Math.random() * (innerHeight - radius * 2) + radius;
    this.y = Math.random() * (innerHeight - radius * 2) + radius;
    this.radius = Math.floor(Math.random() * 3.5);
    this.color = 'rgba(255,255,255,' + Math.random() + ')';;
    this.dx = (Math.random() * 3 - 1.5);
    this.dy = (Math.random() * 3 - 1.5);

    this.dest = {
        x: x,
        y: y
    };
    this.accX = 0;
    this.accY = 0;
    this.friction = Math.random() * 0.0005 + .95;

    //create method within Object to actually put x and y parameters to use

    this.draw = function () {
        c.beginPath();
        c.arc(this.x, this.y, this.radius, 0, Math.PI * 2, false);
        c.fillStyle = this.color;
        c.fill();
    }

    this.update = function () {
        if (this.x + this.radius > innerWidth || this.x - this.radius < 0) {
            this.dx = -this.dx;
        }

        if (this.y + this.radius > innerHeight || this.y - this.radius < 0) {
            this.dy = -this.dy;
        }
        this.x += this.dx;
        this.y += this.dy;

        this.draw();
    }
}

export function Particle(x, y) {
    this.x = Math.random() * ww;
    this.y = Math.random() * wh;
    this.dest = {
        x: x,
        y: y
    };
    this.r = Math.random() + 1;
    this.dx = (Math.random() * 3 - 1.5);
    this.dy = (Math.random() * 3 - 1.5);
    this.accX = 0;
    this.accY = 0;
    this.friction = Math.random() * 0.0005 + .95;

    this.color = '#FFFFFF';
}