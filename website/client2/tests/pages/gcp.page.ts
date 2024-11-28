import BasePage from './base.page';

export default class GcpPage extends BasePage {
    override name: string = "gcp-page";
    pathstem: string = '#/gcp';
    private _headertitle: string = "Google Cloud Platform (gcp)";
    private _title = 'nehsa.net | gcp';
    get headerTitle(): string { return this._headertitle }
    get title(): string { return this._title }   
    get path(): string { return `${this.settings.APP_ENVIRONMENT}/${this.pathstem}`; };

    // locators
    get getHeaderTitle() { return this.page.getByTestId('header-title'); }
}
