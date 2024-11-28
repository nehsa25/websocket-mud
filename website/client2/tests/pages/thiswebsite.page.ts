import BasePage from './base.page';

export default class ThisWebsitePage extends BasePage {
    override name: string = "thiswebsite-page";
    pathstem: string = '#/website';
    private _headertitle: string = "This Website";
    private _title = 'nehsa.net | This Website';
    get headerTitle(): string { return this._headertitle }
    get title(): string { return this._title }    
    get path(): string { return `${this.settings.APP_ENVIRONMENT}/${this.pathstem}`; };

    // locators
    get getHeaderTitle() { return this.page.getByTestId('header-title'); }
}
