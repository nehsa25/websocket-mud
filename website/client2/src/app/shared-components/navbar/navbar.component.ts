import { Component, ViewChild } from '@angular/core';
import { RouterModule, RouterLink, Router } from '@angular/router';
import { UserService } from '../../services/user.service';
import { MatExpansionModule, MatExpansionPanelHeader } from '@angular/material/expansion';
import { MatIconModule } from '@angular/material/icon';
import { NgClass } from '@angular/common';
import { ResponsiveService } from '../../services/responsive.service';
import { ResponsiveType } from '../../types/responsive.type';

@Component({
  selector: 'app-navbar',
  standalone: true,
  imports: [RouterModule, RouterLink, MatExpansionModule, MatIconModule, NgClass],
  templateUrl: './navbar.component.html',
  styleUrl: './navbar.component.scss'
})
export class NavbarComponent {
  allowExpand = true;
  expanded = true;
  constructor(public userService: UserService,
    private router: Router,
    public responsiveService: ResponsiveService
  ) { }

  ngOnInit() {
    this.responsiveService.resolution$.subscribe((resolution: ResponsiveType) => {
      if (resolution.width < 768) {
        this.allowExpand = true;
        this.expanded = false;
      } else if (resolution.width < 1024) {
        this.allowExpand = true;
        this.expanded = true;
      } else {
        this.allowExpand = false;
        this.expanded = true;
      }
    });
  }

  sendUser = (page: string) => {
    this.userService.pagePath = page;
    this.router.navigate([page]);
  }

  // allowExpansion = (event: any) => {
  //   if (event) {
  //     console.log('expanded');
  //     this.shouldExpand = false;
  //   } else {
  //     console.log('!expanded');
  //     event.stopPropagation();
  //   }
  //   this.shouldExpand = false;
  //   event.stopPropagation();
  // }
}
