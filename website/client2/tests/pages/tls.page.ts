import BasePage from './base.page';

export default class TlsPage extends BasePage {
    override name: string = "tls-page";
    pathstem: string = '#/tls';
    private _headertitle: string = "TLS";
    private _title = 'nehsa.net | TLS';
    get headerTitle(): string { return this._headertitle }
    get title(): string { return this._title }    
    get path(): string { return `${this.settings.APP_ENVIRONMENT}/${this.pathstem}`; };

    // locators
    get getHeaderTitle() { return this.page.getByTestId('header-title'); }
}
