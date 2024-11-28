import { Component, EventEmitter, Inject, Output } from '@angular/core';
import {
  MAT_DIALOG_DATA,
  MatDialogRef,
  MatDialogTitle,
  MatDialogContent,
  MatDialogActions,
  MatDialogClose,
} from '@angular/material/dialog';
import { MatButtonModule } from '@angular/material/button';
import { FormsModule } from '@angular/forms';
import { MatInputModule } from '@angular/material/input';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatIcon } from '@angular/material/icon';
import { CdkDrag } from '@angular/cdk/drag-drop';

export interface DialogData { }

@Component({
  selector: 'app-map',
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
  templateUrl: './map.component.html',
  styleUrl: './map.component.scss'
})
export class MapComponent {
  @Output() emitService = new EventEmitter();
  image = "";

  expanded = false;
  constructor(
    public dialogRef: MatDialogRef<MapComponent>,
    @Inject(MAT_DIALOG_DATA) public data:
      {
        map_name: string
      }
  ) { }

  ngOnInit() {
    this.image = `https://api.nehsa.net/${this.data.map_name}_small.svg`;
  }

  min() {
    this.emitService.emit('min');
    this.dialogRef.close();
  }

  enlargen() {
    if (this.expanded) {
      this.dialogRef.updateSize('90%');
      this.image = `https://api.nehsa.net/${this.data.map_name}_small.svg`;
      this.expanded = false;
    } else {
      this.dialogRef.updateSize('90%', '90%');
      this.image = `https://api.nehsa.net/${this.data.map_name}.svg`;
      this.expanded = true;
    }
  }
}
