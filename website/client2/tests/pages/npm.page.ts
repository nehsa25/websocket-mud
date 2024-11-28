import BasePage from './base.page';

export default class NpmPage extends BasePage {
    override name: string = "npm-page";
    pathstem: string = '#/npm';
    private _headertitle: string = "npm";
    private _title = 'nehsa.net | npm';
    get headerTitle(): string { return this._headertitle }
    get title(): string { return this._title }    
    get path(): string { return `${this.settings.APP_ENVIRONMENT}/${this.pathstem}`; };

    // locators
    get getHeaderTitle() { return this.page.getByTestId('header-title'); }
}
