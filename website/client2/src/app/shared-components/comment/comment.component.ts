import { NgIf } from '@angular/common';
import { Component, EventEmitter, Input } from '@angular/core';
import { FormBuilder, FormControl, FormsModule, ReactiveFormsModule } from '@angular/forms';
import { MatButtonModule } from '@angular/material/button';
import { MatExpansionModule } from '@angular/material/expansion';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatIcon } from '@angular/material/icon';
import { MatInputModule } from '@angular/material/input';
import { MatSnackBar, MatSnackBarModule } from '@angular/material/snack-bar';
import { MatStepperModule } from '@angular/material/stepper';
import { CommentType } from '../../types/comment.type';
import { HttpService } from '../../services/http.service';
import { UserService } from '../../services/user.service'
import { Observable, Subscription } from 'rxjs';
import { MatTableDataSource, MatTableModule } from '@angular/material/table';
import { MatPaginatorModule } from '@angular/material/paginator';

@Component({
  selector: 'app-comment',
  standalone: true,
  imports: [
    MatButtonModule,
    MatStepperModule,
    NgIf,
    FormsModule,
    MatFormFieldModule,
    ReactiveFormsModule,
    MatExpansionModule,
    FormsModule,
    MatFormFieldModule,
    MatInputModule,
    MatIcon,
    MatSnackBarModule,
    MatTableModule,
    MatPaginatorModule
  ],
  providers: [HttpService],
  templateUrl: './comment.component.html',
  styleUrl: './comment.component.scss'
})
export class CommentComponent {
  commentform = this._formBuilder.group({
    comment: new FormControl(),
  });
  username = "";
  page = "";
  addComment = false;
  commenttext = "";
  totalItems = 0;
  private eventsSubscription: Subscription = new Subscription();
  dataSource: MatTableDataSource<CommentType> = new MatTableDataSource<CommentType>();
  clicked = false;
  result = "Yes!";
  @Input() events: Observable<CommentType> = new Observable<CommentType>();
  constructor(
    public userService: UserService,
    private _formBuilder: FormBuilder,
    private _httpService: HttpService,
    private _snackbar: MatSnackBar) { }

  ngOnInit() {
    this.username = this.userService.name;
    this.page = this.userService.page;
    this.result = Math.random() < 0.5 ? 'Yes! Am I correct? Post a comment and let me know.' : 'No. You will not. Am I correct? Post a comment and let me know.';
    this._httpService.getComments(this.page).subscribe((data: any) => {
      let comments: Array<CommentType> = new Array<CommentType>();
      comments.push(data);
      this.dataSource = new MatTableDataSource(comments);
      this.dataSource.data = data;
      this.totalItems = data.length;
    });
  }

  ngOnDestroy() {
    this.eventsSubscription.unsubscribe();
  }

  addcomment() {
    this.addComment = true;
  }

  checkAddComment() {
    this.clicked = true;
  }

  getDisplayedColumnsAll() {
    return ['commentid', 'date', 'username', 'comment'];
  }


  submit() {
    const user_comment = this.commentform.value.comment;
    if (user_comment == null || user_comment === "") {
      this._snackbar.open("Please enter a comment.", "Dismiss", { duration: 2000 });
      return;
    }

    this._snackbar.open("Thank you for your comment!", "Dismiss", { duration: 2000 });
    this.commenttext = "";
    let comment = new CommentType();
    comment.comment = user_comment;
    comment.page = this.userService.page;
    comment.username = this.userService.name;
    this._httpService.postComment(comment).subscribe((_next: any) => {
      this._snackbar.open("Comment added", "Dismiss");
      this._httpService.getComments(this.page).subscribe((data: any) => {
        this.dataSource.data = data;
      })
    });
  }

  cancel() {
    this.commentform.value.comment = "";
    this.addComment = false;
  }
}
