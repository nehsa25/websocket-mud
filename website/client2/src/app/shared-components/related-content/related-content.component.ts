import { Component } from '@angular/core';
import { MatExpansionModule } from '@angular/material/expansion';
import { RouterLink } from '@angular/router';
import { HttpService } from '../../services/http.service';
import { Observable, forkJoin } from 'rxjs';
import { RelatedPage } from '../../types/related-page';
import { NgFor, NgIf } from '@angular/common';
import { UserService } from '../../services/user.service';

@Component({
  selector: 'app-related-content',
  standalone: true,
  imports: [MatExpansionModule, RouterLink, NgIf, NgFor],
  templateUrl: './related-content.component.html',
  styleUrl: './related-content.component.scss'
})
export class RelatedContentComponent {
  getQueries: Array<Observable<any>> = new Array<Observable<any>>();
  pages: Array<RelatedPage> = new Array<RelatedPage>();

  constructor(private httpClient: HttpService, public userService: UserService) {}

  ngOnInit() {
    var getRelated = this.httpClient.getRelated(`/${this.userService.page}`);
    this.getQueries.push(getRelated);
    forkJoin(this.getQueries).subscribe(next => {
      if (next == null) {
        return;
      }
      this.pages = next[0];
    });
  }
}
