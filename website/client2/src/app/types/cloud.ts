import { ElementRef } from "@angular/core";

// Tree - max 50px
export class Cloud {
    width: number = 0;
    height: number = 0;
    zindex: number = 0;
    top: number = 0;
    speed: string = "";
    speedNumber: number = 0;
    directionLeft: boolean = true;
    left: number = 0;

    constructor(directionLeft: boolean) {

        // width   
        this.width = 28;
        this.height = 15;
        this.zindex = 1;

        // top
        this.top = Math.floor(this.width);
        if (this.top < 0) {
            this.top = 0;
        }
        if (this.top > 3) {
            this.top = 3;
        }

        // left
        this.left = this.getRandomNumberBetween(1, 1200, .1);

        this.directionLeft = directionLeft;

        // max speed is if width is 50px
        const maxSpeed = 50; // Maximum speed
        const minSpeed = 30; // Minimum speed
        const maxWidth = 50; // Maximum width
        
        const speedFactor = Math.max(0, 1 - (this.width / maxWidth));
        this.speed = minSpeed + (speedFactor * (maxSpeed - minSpeed))  + 's';
        console.log(`maxSpeed: ${maxSpeed}, Tree speed: ${this.speed}, width: ${this.width}, speedFactor: ${speedFactor}`);
    }

    getRandomNumberBetween(min: number, max: number, step: number = 1): number {
        const range = (max - min) / step;
        return Math.ceil(Math.random() * range) * step + min;
    }

    updateSpeed(speedBoost: number) {
        this.speedNumber = speedBoost;
        this.speed = this.speedNumber + speedBoost + 's';
    }
}