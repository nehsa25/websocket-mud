import { ChangeDetectorRef, Component, inject, OnDestroy, OnInit } from '@angular/core';
import { UserService } from '../../services/user.service';
import { NgIf } from '@angular/common';
import { Comet } from '../../types/comet.type';
import { MatDialog, MatDialogModule } from '@angular/material/dialog';
import { PromptComponent } from './prompt/prompt.component';
import { HttpService } from '../../services/http.service';
import { forkJoin, Observable, of } from 'rxjs';
import { AIQuestion } from '../../types/ai.type';
import { MatIconModule } from '@angular/material/icon';

@Component({
  selector: 'app-comet',
  standalone: true,
  imports: [NgIf, MatDialogModule, MatIconModule],
  templateUrl: './comet.component.html',
  styleUrl: './comet.component.scss'
})
export class CometComponent implements OnInit {
  cometWait = 5000;
  cometCurrentMessage = "Woof.";
  lastAnsweredMessage: string = "";
  answered = false;
  promptOpen = false;
  cometOpen = true;
  donotupdate = false;
  answer: string = "";
  readonly dialog = inject(MatDialog);
  cometMessages = [
    new Comet("My name is Comet. I am the AI for nehsa.net and I can help you if you let me.", this.cometWait * 1),
    new Comet("I am a dog&mdash;an almond-blond terrier actually... but I am also an AI, and I can help you if you let me. Click on me.", this.cometWait * 3),
    new Comet("Whine.", this.cometWait * 5),
    // new Comet("As you may see, I am a dog; click on me!", this.cometWait * 4.5),
    // new Comet("Click on me. I can help you with your problems.", this.cometWait * 5),
    // new Comet("I am a dog, click on me. I can help you with your problems.", this.cometWait * 6),
    // new Comet("", this.cometWait * 6),
    // new Comet("Really? There isn't anything I can help you with?", this.cometWait * 30),
    // new Comet("", this.cometWait * 35),
    // new Comet("Agile development! Would you like to know about Agile best practices? Ask me! I know!", this.cometWait * 60),
    // new Comet("Whine.", this.cometWait * 65),
    new Comet("", this.cometWait * 7),
  ];
  constructor(
    private ref: ChangeDetectorRef,
    public userService: UserService,
    public httpClient: HttpService) { }

  ngOnInit() {
    this.cometMessages.forEach((msg) => {
        setTimeout(() => {
          if (this.donotupdate) {
            return;
          }

          if (this.answered) {
            this.cometCurrentMessage = this.lastAnsweredMessage;;
          } else {
            this.cometCurrentMessage = msg.text;
          }
          this.ref.markForCheck();
        }, msg.delay);
    });
  }

  closeButton(event: any) {
    this.cometCurrentMessage = "Bark! Bark!<br> Goodbye!";
    this.donotupdate = true;
    this.ref.markForCheck(); // this is necessary to update the view
    
    event.stopPropagation(); // stop propagation to launchPrompt

    setTimeout(() => {
      this.closeComet();
    }, 1500);
  }

  closeComet() {
    this.cometOpen = false;
  }

  launchPrompt(event: any) {
    if (this.promptOpen)
      return;

    this.promptOpen = true;
    let dialogRef = this.dialog.open(PromptComponent, {
      height: '300px',
      width: '500px',
      enterAnimationDuration: "800ms",
      exitAnimationDuration: "300ms"
    });
    dialogRef.afterClosed().subscribe(result => {
      if (result !== "" && result !== undefined) {
        this.promptOpen = false;
        console.log("Prompt result: " + result);
        let question = new AIQuestion();
        question.question = result;
        question.previousAnswer = this.lastAnsweredMessage;
        this.cometCurrentMessage = "Woof! Please Wait..."
        this.ref.markForCheck();
        this.httpClient.postAIQuestion(question).subscribe(result => {
          let r: AIQuestion = result as AIQuestion;
          this.cometCurrentMessage = r.answer.toString();
          this.lastAnsweredMessage = r.answer.toString();
          this.answered = true;
          this.ref.markForCheck();
        });
      }
    });
  }
}
