import { NgFor, NgIf } from '@angular/common';
import { Component, EventEmitter, Inject, Output } from '@angular/core';
import { FormBuilder, FormControl, FormsModule, ReactiveFormsModule } from '@angular/forms';
import { MatButtonModule } from '@angular/material/button';
import { MAT_DIALOG_DATA, MatDialogRef } from '@angular/material/dialog';
import { MatExpansionModule } from '@angular/material/expansion';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatIcon } from '@angular/material/icon';
import { MatInputModule } from '@angular/material/input';
import { MatStepperModule } from '@angular/material/stepper';

@Component({
  selector: 'app-user-create',
  standalone: true,
  imports: [
    MatButtonModule,
    MatStepperModule,
    NgIf,
    NgFor,
    FormsModule,
    MatFormFieldModule,
    ReactiveFormsModule,
    MatExpansionModule,
    FormsModule,
    MatFormFieldModule,
    MatInputModule,
    MatIcon
  ],
  templateUrl: './user-create.component.html',
  styleUrl: './user-create.component.scss'
})

export class UserCreateComponent {
  @Output() emitService = new EventEmitter();
  nameLabel = "Character Name";
  raceLabel = "Race";
  race = "human";
  races = [];
  class = "fighter";
  classes = ["bruiser", "light-weaver"];
  formGroup1 = this._formBuilder.group({
    name: new FormControl(),
  });
  formGroup2 = this._formBuilder.group({
  });
  formGroup3 = this._formBuilder.group({
  });
  constructor(
    private _formBuilder: FormBuilder,
    public userDialog: MatDialogRef<UserCreateComponent>,
    @Inject(MAT_DIALOG_DATA) public data:
      {
        username: string
      }
  ) { }
}