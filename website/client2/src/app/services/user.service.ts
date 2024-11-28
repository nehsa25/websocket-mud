import { Injectable } from '@angular/core';
import { Router } from '@angular/router';

@Injectable()
export class UserService {
    private _name: string = "";
    private _about: string = "";
    private _currentPage: string = "";
    private _currentPagePath: string = "";
    private _isDark: boolean = false;

    constructor(private router: Router) {
    }


    setDarkMode(value: boolean) {
        this._isDark = value;
    }

    navigateTo(routerlink: string) {
        console.log("Navigating to " + routerlink);
        this.router.navigate([routerlink]);
    }

    appIsDark(): boolean {
        return this._isDark;
    }

    get name(): string {
        return this._name;
    }
    set name(value: string) {
        this._name = value;
    }

    get about(): string {
        return this._about;
    }
    set about(value: string) {
        this._about = value;
    }

    get page(): string {
        return this._currentPage;
    }
    set page(value: string) {
        this._currentPage = value;
    }

    get pagePath(): string {
        return this._currentPagePath;
    }
    set pagePath(value: string) {
        this._currentPagePath = value;
    }
}