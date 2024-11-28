import { Injectable } from '@angular/core';
import { MatSnackBar } from '@angular/material/snack-bar';

@Injectable()
export class SnackService {
    private duration = 5000;
    constructor(public snackBar: MatSnackBar) {
    }

    /** 
     * Displays message to use from the bottom of the scren
     * @param {string} message - The message to display 
     * @param {number} delayinMS - The duration in milliseconds 
     * */      
    public openSnackBar(message: string, delayinMS: number){
        this.snackBar.open(message, undefined, { duration: delayinMS, verticalPosition: 'bottom' });
    }
}