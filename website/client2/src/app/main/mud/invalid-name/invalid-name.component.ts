import { NgIf } from '@angular/common';
import { Component, EventEmitter, Inject, Output } from '@angular/core';
import { FormBuilder, FormControl, FormsModule, ReactiveFormsModule } from '@angular/forms';
import { MatButtonModule } from '@angular/material/button';
import { MAT_DIALOG_DATA, MatDialogRef } from '@angular/material/dialog';
import { MatExpansionModule } from '@angular/material/expansion';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatIcon } from '@angular/material/icon';
import { MatInputModule } from '@angular/material/input';
import { MatSnackBarModule } from '@angular/material/snack-bar';

@Component({
  selector: 'app-invalid-name',
  standalone: true,
  imports: [MatButtonModule,
    NgIf,
    FormsModule,
    MatFormFieldModule,
    ReactiveFormsModule,
    MatExpansionModule,
    FormsModule,
    MatFormFieldModule,
    MatInputModule,
    MatIcon,
    MatSnackBarModule],
  templateUrl: './invalid-name.component.html',
  styleUrl: './invalid-name.component.scss'
})
export class InvalidNameComponent {
  @Output() emitService = new EventEmitter();
  name: string = "";
  formGroup = this._formBuilder.group({
    name: new FormControl(),
  });
  constructor(
    public dialogRef: MatDialogRef<InvalidNameComponent>,
    private _formBuilder: FormBuilder,
    @Inject(MAT_DIALOG_DATA) public data:
      {
        name: string
      }) {}
      
  ngOnInit() {
    this.name = this.data.name;
  }
  
  submit() {
    this.emitService.emit(this.formGroup.get('name')?.value);
    this.dialogRef.close();
  }
}
