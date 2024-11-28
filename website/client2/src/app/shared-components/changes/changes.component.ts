import { CommonModule } from '@angular/common';
import { Component } from '@angular/core';
import { Change } from '../../types/change';
import { CommentComponent } from '../comment/comment.component';
import { RelatedContentComponent } from '../related-content/related-content.component';
import { MatCardModule } from '@angular/material/card';
@Component({
  selector: 'app-changes',
  standalone: true,
  imports: [CommonModule, CommentComponent, RelatedContentComponent, MatCardModule],
  templateUrl: './changes.component.html',
  styleUrl: './changes.component.scss'
})
export class ChangesComponent {
  public changes: Change[] = [
    {
      date: "2024-11-26",
      description: [
        "Added a 'Working with Others' section in git content",
        "Fixed NehsaMUD so it starts again and basic functions work - map, navigation",
      ]
    },
    {
      date: "2024-11-24",
      description: [
        "Fixed NehsaMUD styling",
        "Fixed comment component",
        "Added Gimp content: transparent images / resizing images",
        "Added content for align-content",
        "Made (usually unhelpful) Comet AI hideable",
        "Prevented Comet AI from showing multiple 'Ask Comet' prompts",
        "Fixed the bottom-border still showing up on the last dt in the dl",
        "Added this change log page"
      ]
    },
    {
      date: "2024-04-07",
      description: ["Jesse decided he wanted a website..."],
    }
  ];
}
