import { ChangeDetectorRef, Component, CUSTOM_ELEMENTS_SCHEMA, ElementRef, HostListener, Input, NO_ERRORS_SCHEMA, OnDestroy, OnInit, ViewChild } from '@angular/core';
import { RouterLink, RouterOutlet } from '@angular/router';
import { NavbarComponent } from './shared-components/navbar/navbar.component';
import { CornerListenerComponent } from './shared-components/corner-listener/corner-listener.component';
import { MatIcon } from '@angular/material/icon';
import { BreadcrumbComponent, BreadcrumbItemDirective } from 'xng-breadcrumb';
import { CommonModule, NgIf } from '@angular/common';
import { HttpService } from './services/http.service';
import { version } from '../version';
import { MatButtonModule } from '@angular/material/button';
import { Observable, Subject, async, forkJoin, retry } from 'rxjs';
import { MatDialog } from '@angular/material/dialog';
import { NameAboutType } from './types/nameabout.type';
import { MatTooltipModule } from '@angular/material/tooltip';
import { UserService } from './services/user.service';
import { MatExpansionModule } from '@angular/material/expansion';
import { MatSidenavModule } from '@angular/material/sidenav';
import { MatSliderModule } from '@angular/material/slider';
import { FranticTim } from './types/tim.type';
import { Tree } from './types/tree';
import { Cloud } from './types/cloud';
import { MatSnackBar } from '@angular/material/snack-bar';
import { CometComponent } from './shared-components/comet/comet.component';
import { ScriptService } from 'ngx-script-loader';

@Component({
    selector: 'app-root',
    standalone: true,
    imports: [
        CommonModule,
        RouterOutlet,
        MatButtonModule,
        MatTooltipModule,
        MatExpansionModule,
        MatSidenavModule,
        MatSliderModule,
    ],
    providers: [
        HttpService
    ],
    schemas: [NO_ERRORS_SCHEMA],
    templateUrl: './app.component.html',
    styleUrl: './app.component.scss'
})
export class AppComponent implements OnInit, OnDestroy {
    @ViewChild('copyright') copyright: ElementRef | undefined;
    @Input() duration = 10;
    private _reversify = false;
    startPosition: number = 0;
    expandedBio = false;
    title = "";
    quote = "";
    openSideNav = true;
    names: Array<NameAboutType> = new Array<NameAboutType>();
    getQueries: Array<Observable<any>> = new Array<Observable<any>>();
    nameConfirmed = false;
    fullScreen: boolean = false;
    isFullScreenEvent = new Subject<boolean>();
    osCheckIsDark = () => window?.matchMedia?.('(prefers-color-scheme:dark)')?.matches ? true : false;
    appIsDark = false;
    osIsDark = false;
    darkmode_value = 0; // slider value
    timMessages: Array<FranticTim> = new Array<FranticTim>();
    trees = new Array<Tree>();
    clouds = new Array<Cloud>();
    timMessage = "";
    showTimTest = false;
    lastTimIndex = 0;
    fromTim = false;
    timMovingLeft = false;
    playState = "running";
    animationDuration = "10s";
    timSpeed = .7;
    pausedExpanded = false;
    isStoryHidden = false;

    constructor(
        private ref: ChangeDetectorRef,
        public httpClient: HttpService,
        public userService: UserService,
        public nameDialog: MatDialog,
        public snackBar: MatSnackBar,
        private scriptService: ScriptService,
        private changeDetectorRef: ChangeDetectorRef
    ) {
        var getName = this.httpClient.getNames(2);
        this.getQueries.push(getName);
    };

    // Angular lifecycle hooks
    ngOnInit() {
        forkJoin(this.getQueries).subscribe(next => {
            if (next == null)
                return;
            this.names = next[0];
            this.userService.name = this.names[0].Name;
            this.userService.about = this.names[0].About
        });
    }

    ngOnDestroy(): void {
    }

    // ensure we are at the top of the page
    onActivate(event: any) {
        window.scroll({
            top: 0,
            left: 0,
            behavior: 'smooth'
        });
    }
}
