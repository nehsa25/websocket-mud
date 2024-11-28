import { Injectable } from '@angular/core';
import { Question } from '../types/question.type';

@Injectable()
export class FlashcardsService {
    Questions: Question[] = [];
    QuestionAnswer: any = null;
    ViewedQuestions: Question[] = [];
    current = 1;

    constructor() { }
    public setQuestion() {
        if (this.QuestionAnswer != null) {
            this.current++;
        }

        this.QuestionAnswer = this.Questions[Math.floor(Math.random() * this.Questions.length)];
        while (this.ViewedQuestions.includes(this.QuestionAnswer)) {
            this.QuestionAnswer = this.Questions[Math.floor(Math.random() * this.Questions.length)];
        }
        this.ViewedQuestions.push(this.QuestionAnswer);

        return this.QuestionAnswer;
    }
    public setQuestions(questions: Question[]) {
        this.Questions = questions;
    }
    public getTotal() {
        return this.Questions.length + 1;
    }
}