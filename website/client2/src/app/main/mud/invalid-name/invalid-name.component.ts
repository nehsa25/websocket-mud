import { Component, EventEmitter, Inject, Output } from '@angular/core';
import { FormBuilder, FormControl, FormsModule, ReactiveFormsModule } from '@angular/forms';
import { MatButtonModule } from '@angular/material/button';
import { MAT_DIALOG_DATA, MatDialogRef } from '@angular/material/dialog';
import { MatExpansionModule } from '@angular/material/expansion';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { MatSnackBarModule } from '@angular/material/snack-bar';

@Component({
  selector: 'app-invalid-name',
  standalone: true,
  imports: [MatButtonModule,
    FormsModule,
    MatFormFieldModule,
    ReactiveFormsModule,
    MatExpansionModule,
    FormsModule,
    MatFormFieldModule,
    MatInputModule,
    MatSnackBarModule],
  templateUrl: './invalid-name.component.html',
  styleUrl: './invalid-name.component.scss'
})
export class InvalidNameComponent {
  @Output() emitService = new EventEmitter();
  name: string = "";
  placeholderName: string = "Hink CoggleSmelt";
  formGroup = this._formBuilder.group({
    name: new FormControl(),
  });
  constructor(
    public dialogRef: MatDialogRef<InvalidNameComponent>,
    private _formBuilder: FormBuilder,
    @Inject(MAT_DIALOG_DATA) public data:
      {
        name: string
      }) { }

  ngOnInit() {
    this.name = this.data.name;
  }

  onKeydown(event: KeyboardEvent) {
    if (event.key === 'Enter') {
      event.preventDefault();
      this.submit();
    }
  }

  submit() {
    this.name = this.formGroup.get('name')?.value
    if (this.name == null || this.name == "") {
      this.name = this.placeholderName;
    }
    this.dialogRef.close(this.name);
  }
}
