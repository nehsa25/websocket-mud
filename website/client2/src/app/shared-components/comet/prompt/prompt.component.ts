import { Component } from '@angular/core';
import { MatButtonModule } from '@angular/material/button';
import { MatDialog, MatDialogActions, MatDialogClose, MatDialogContent, MatDialogModule, MatDialogRef, MatDialogTitle } from '@angular/material/dialog';
import { UserService } from '../../../services/user.service';
import { FormsModule, NgModel } from '@angular/forms';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatIconModule } from '@angular/material/icon';
import { MatInputModule } from '@angular/material/input';
import { MatCardModule } from '@angular/material/card';

@Component({
  selector: 'app-prompt',
  standalone: true,
  imports: [MatCardModule, MatFormFieldModule, MatInputModule,
    FormsModule, MatIconModule],
  templateUrl: './prompt.component.html',
  styleUrl: './prompt.component.scss'
})
export class PromptComponent {
  constructor(public dialogRef: MatDialogRef<PromptComponent>,
    public userService: UserService
  ) { }

  prompt: string = "";
  submit(prompt: any) {
    this.prompt = prompt.value.trim();
    this.dialogRef.close(this.prompt);
  }

  cancel() {
    this.dialogRef.close('');
  }
}
