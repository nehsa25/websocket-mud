import { Component, ViewChild, ElementRef, Input } from '@angular/core';
import { MatIcon } from '@angular/material/icon';
import { Clipboard } from '@angular/cdk/clipboard';
import { MatSnackBar } from '@angular/material/snack-bar';

@Component({
    selector: 'app-copy',
    standalone: true,
    imports: [MatIcon],
    templateUrl: './copy.component.html',
    styleUrl: './copy.component.scss'
})
export class CopyComponent {
    @Input() copyData: string = "";
    @ViewChild('copyButton', { static: false }) copyButton: ElementRef | undefined;
    @ViewChild('.copy-container', { static: false, read: ElementRef }) copyContainer: ElementRef | undefined;

    copyText: string = "";
    isMouseDown = false;
    constructor(public clipboard: Clipboard, public _snackbar: MatSnackBar) {

    }
    getCopyText(event: MouseEvent) {
        // prevent form navigation
        event.preventDefault();

        const copyContainer = this.copyButton?.nativeElement.closest('.copy-container');
        if (this.copyData !== "") {
            this.copyText = this.copyData;

        }
        else if (copyContainer) {
            const content = copyContainer.textContent;
            this.copyText = content.trim().replace("content_copy", "");
        } else {
            this._snackbar.open('No .copy-container found');
        }

        if (this.copyText !== "") {
            let slang = ['homey', 'homes', 'suga', 'mate'];
            
            // message with random slang at the end
            this._snackbar.open(`Copied to clipboard, ${slang[Math.floor(Math.random() * slang.length)]}!`, 'Dismiss');
            this.clipboard.copy(this.copyText);
        }
    }
}
