import BasePage from './base.page';

export default class OhaiPage extends BasePage {
    override name: string = "ohai-page";
    pathstem: string = '#/ohai';
    private _headertitle: string = "OHAI";
    private _title = 'nehsa.net | Ohai';
    get headerTitle(): string { return this._headertitle }
    get title(): string { return this._title }    
    get path(): string { return `${this.settings.APP_ENVIRONMENT}/${this.pathstem}`; };

    // locators
    get getHeaderTitle() { return this.page.getByTestId('header-title'); }
}
