import { CdkDrag } from '@angular/cdk/drag-drop';
import { Component, EventEmitter, Inject, Output } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { MatButtonModule } from '@angular/material/button';
import { MatCardModule } from '@angular/material/card';
import { MAT_DIALOG_DATA, MatDialogActions, MatDialogClose, MatDialogContent, MatDialogRef, MatDialogTitle } from '@angular/material/dialog';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatIcon } from '@angular/material/icon';
import { MatInputModule } from '@angular/material/input';
import { AiImageType } from '../../../types/aiimage.type';
import { HttpClient } from '@angular/common/http';
import { HttpService } from '../../../services/http.service';

@Component({
  selector: 'app-ai-image',
  standalone: true,
  imports: [
    MatFormFieldModule,
    MatInputModule,
    FormsModule,
    MatButtonModule,
    MatDialogTitle,
    MatDialogContent,
    MatDialogActions,
    MatDialogClose,
    MatIcon,
    CdkDrag
  ],
  providers: [HttpService],
  templateUrl: './ai-image.component.html',
  styleUrl: './ai-image.component.scss'
})
export class AiImageComponent {
  @Output() emitService = new EventEmitter();
  image = "";
  image_width = 380;
  expanded = false;
  constructor(
    public dialogRef: MatDialogRef<AiImageComponent>,
    private http: HttpService,
    @Inject(MAT_DIALOG_DATA) public data:
      {
        roomImageName: string
      }
  ) { }

  ngOnInit() {
    this.image = this.data.roomImageName;
  }
}