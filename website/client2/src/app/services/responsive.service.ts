import { Injectable } from '@angular/core';
import { BehaviorSubject } from 'rxjs';
import { ResponsiveType, DeviceType } from '../types/responsive.type';

@Injectable({
    providedIn: 'root'
})
export class ResponsiveService {
    public deviceSettings = new ResponsiveType(window.innerWidth, window.innerHeight)
    private resolutionSubject = new BehaviorSubject<ResponsiveType>(this.deviceSettings);
    resolution$ = this.resolutionSubject.asObservable();

    constructor() {
        window.addEventListener('resize', () => {
            this.resolutionSubject.next(new ResponsiveType(window.innerWidth, window.innerHeight));
        });
    }

    getDeviceType() {
        console.log("this.deviceSettings.deviceType");
        console.log(this.deviceSettings.deviceType);
        return this.deviceSettings.deviceType;
    }
}