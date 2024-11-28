import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { ContactType } from '../types/contact.type';
import { AddUserType } from '../types/adduser.type';
import { NameType } from '../types/name.type';
import { AiImageType } from '../types/aiimage.type';
import { AIQuestion } from '../types/ai.type';
import { Observable } from 'rxjs';
import { environment } from '../../../src/environments/environment';

@Injectable()
export class HttpService {
    apiUrl = "";
    contactmeUrl = "";
    addUserUrl = "";
    quoteUrl = "";
    nameUrl = "";
    posAdjUrl = "";
    stabilityaiUrl = "";
    dbhealth = "";
    commentUrl = "";
    aiQuestionUrl = "";
    getRelatedUrl = "";
    httpOptions = {
        headers: new HttpHeaders({
            'Content-Type': 'application/json'
        })
    };
    constructor(private http: HttpClient) {
        this.contactmeUrl = `${environment.apiUrl}/${environment.apiVersion}/contactme`;
        this.addUserUrl = `${environment.apiUrl}/${environment.apiVersion}/adduser`;
        this.quoteUrl = `${environment.apiUrl}/${environment.apiVersion}/quote`;
        this.nameUrl = `${environment.apiUrl}/${environment.apiVersion}/name`;
        this.posAdjUrl = `${environment.apiUrl}/${environment.apiVersion}/positiveadjective`;
        this.dbhealth = `${environment.apiUrl}/${environment.apiVersion}/dbhealth`;
        this.commentUrl = `${environment.apiUrl}/${environment.apiVersion}/comment`;
        this.aiQuestionUrl = `${environment.apiUrl}/${environment.apiVersion}/ai`;
        this.getRelatedUrl = `${environment.apiUrl}/${environment.apiVersion}/related`;
    }

    /** 
     * Posts the contact me form to API
     * @param {ContactType} body - The body to the message
     * @returns {object} - The response from the API
     * */
    postContactMe(body: ContactType) {
        return this.http.post<ContactType>(this.contactmeUrl, body);
    }

    /** 
     * Posts the contact me form to API
     * @param {AddUserType} body - The body to the message
     * @returns {object} - The response from the API
     * */
    postAddUser(body: AddUserType) {
        return this.http.post<AddUserType>(this.addUserUrl, body);
    }

    /** Returns the quote */
    getQuote() {
        return this.http.get(this.quoteUrl);
    }

    /** Returns the related pages for a page */
    getRelated(page_name: string) {
        let url = `${this.getRelatedUrl}?page=${page_name}`;
        return this.http.get(url);
    }

    /** Returns the comments for a page */
    getComments(page_name: string, numToReturn: number = 5) {
        let url = `${this.commentUrl}/${page_name}/${numToReturn}`;
        return this.http.get(url);
    }

    getDBHealth() {
        return this.http.get(this.dbhealth);
    }

    postComment(body: any) {
        return this.http.post(this.commentUrl, body);
    }

    /** Returns a random name */
    getName() {
        return this.http.get(this.nameUrl);
    }

    /** Returns scraped data */
    getScrapeData(url: string) {
        const getScrapeUrl = `https://api.nehsa.net/v1/scaper?scrapeUrl=${url}`;
        return this.http.get(getScrapeUrl);
    }

    /** Returns the weather */
    getWeather(city: string, units: string = 'imperial', typeStyle: string = 'words') {
        const getWeatherUrl = `https://api.nehsa.net/v1/getweather?city=${city}&units=${units}&weatherType=${typeStyle}`;
        return this.http.get(getWeatherUrl);
    }

    /** Returns the specified number random names */
    getNames(numToReturn: number) {
        return this.http.get(`${this.nameUrl}/${numToReturn}`);
    }

    /** Asks an AI questions */
    postAIQuestion(body: AIQuestion): Observable<AIQuestion> {
        return this.http.post<any>(this.aiQuestionUrl, body);
    }

    /** Returns a random list of positive adjectives */
    getPosTerms() {
        return this.http.get(this.posAdjUrl);
    }

    /** updates name */
    updateName(name: string) {
        let user: NameType = new NameType();
        user.Name = name;
        return this.http.post(this.nameUrl, user);
    }
}
