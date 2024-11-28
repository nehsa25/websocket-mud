import BasePage from './base.page';

export default class AWSPage extends BasePage {
    name: string = "aws-page";
    pathstem: string = '#/aws';
    private _headertitle: string = "AWS";
    private _title = 'nehsa.net | aws';
    get headerTitle(): string { return this._headertitle }
    get title(): string { return this._title }    
    get path(): string { return `${this.settings.APP_ENVIRONMENT}/${this.pathstem}`; };

    // locators
    get getHeaderTitle() { return this.page.getByTestId('header-title'); }
}
