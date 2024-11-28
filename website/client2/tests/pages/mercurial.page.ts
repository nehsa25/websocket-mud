import BasePage from './base.page';

export default class MercurialPage extends BasePage {
    override name: string = "mercurial-page";
    pathstem: string = '#/mercurial';
    private _headertitle: string = "Mercurial / hg";
    private _title = 'nehsa.net | Mercurial';
    get headerTitle(): string { return this._headertitle }
    get title(): string { return this._title }    
    get path(): string { return `${this.settings.APP_ENVIRONMENT}/${this.pathstem}`; };

    // locators
    get getHeaderTitle() { return this.page.getByTestId('header-title'); }
}
