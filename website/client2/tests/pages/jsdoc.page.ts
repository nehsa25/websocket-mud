import BasePage from './base.page';

export default class JsDocPage extends BasePage {
    override name: string = "jsdoc-page";
    pathstem: string = '#/jsdoc';
    private _headertitle: string = "jsdoc";
    private _title = 'nehsa.net | jsdoc';
    get headerTitle(): string { return this._headertitle }
    get title(): string { return this._title }    
    get path(): string { return `${this.settings.APP_ENVIRONMENT}/${this.pathstem}`; };

    // locators
    get getHeaderTitle() { return this.page.getByTestId('header-title'); }
}
