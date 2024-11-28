import { Component, Inject } from '@angular/core';
import { MatCardModule } from '@angular/material/card';
import { CommentComponent } from '../../../shared-components/comment/comment.component';
import { CommonModule, NgFor } from '@angular/common';
import { MAT_DIALOG_DATA, MatDialogRef } from '@angular/material/dialog';
import { HelpEvent } from '../../../types/mudevent.type';

@Component({
  selector: 'app-help-modal',
  standalone: true,
  imports: [NgFor, CommonModule, MatCardModule, CommentComponent],
  templateUrl: './help-modal.component.html',
  styleUrl: './help-modal.component.scss'
})
export class HelpModalComponent {

  constructor(
    public dialogRef: MatDialogRef<HelpModalComponent>,
    @Inject(MAT_DIALOG_DATA) public data:
      {
        cmds: any
      }
  ) { }

  ngOnInit() {
    console.log(this.data);
  }

}
