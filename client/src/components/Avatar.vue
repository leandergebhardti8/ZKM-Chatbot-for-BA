<template>
    <canvas id="p_canvas"></canvas>
</template>

<script>
import { Circle, Particle } from '../assets/class/class'
    export default {
        data() {
            return {
                canvasWidth: 0,
                canvasHeight: 0,
                radius: 1,
                amount: 0,
                circleArray: [],
                excited: false,
                angry: false,
                x: 0,
                y: 0,
                dx: 0,
                dy: 0,
                q: 1000,
                ctx: {}
            }
        },
        mounted () {
            let canvas = document.getElementById("p_canvas");
            this.ctx = canvas.getContext('2d');
            this.canvasWidth = canvas.offsetWidth;
            this.canvasHeight = canvas.offsetHeight;
            let newCircleArray = this.circleArray;
            for (var i = 0; i < newCircleArray.length; i++) {
                newCircleArray[i].color = 'rgba(255,255,255,' + Math.random() + ')';
                newCircleArray[i].dx = (Math.random() * 1 -.5);
                newCircleArray[i].dy = (Math.random() * 1 - .5);
            }
            this.circleArray = newCircleArray;
            this.drawCircles();
            this.animate();
        },
        methods: {
            draw() {
                this.ctx.beginPath();
                this.ctx.arc(this.x, this.y, this.radius, 0, Math.PI * 2, false);
                this.ctx.fillStyle = this.color;
                this.ctx.fill();
            },
            update() {
                if (this.x + this.radius > this.canvaWidth || this.x - this.radius < 0) {
                    this.dx = -this.dx;
                }

                if (this.y + this.radius > this.canvasHeight || this.y - this.radius < 0) {
                    this.dy = -this.dy;
                }
                this.x += this.dx;
                this.y += this.dy;

                this.draw();
            },
            drawCircles() {
                for (var i = 0; i < this.q; i++) {
                    this.circleArray.push(new Circle(this.x, this.y, this.radius, this.ctx));
                }
            },
            animate() {
                requestAnimationFrame(this.animate);
                this.ctx.clearRect(0, 0, this.canvasWidth*2, this.canvasHeight*2);
                for (var i = 0; i < this.circleArray.length; i++) {
                    this.circleArray[i].update();
                }
            }
        }
    }
</script>

<style lang="scss" scoped>
canvas {
    width: 100%;
    height: 100%;
    display: block;
    margin: auto;
    border-radius: 50%;
}
</style>