import BasePage from './base.page';

export default class AngularPage extends BasePage {
    name: string = "angular-page";
    pathstem: string = '#/angular';
    private _headertitle: string = "Angular";
    private _title = 'nehsa.net | Angular';
    get headerTitle(): string { return this._headertitle }
    get title(): string { return this._title }    
    get path(): string { return `${this.settings.APP_ENVIRONMENT}/${this.pathstem}`; };

    // locators
    get getHeaderTitle() { return this.page.getByTestId('header-title'); }
}
