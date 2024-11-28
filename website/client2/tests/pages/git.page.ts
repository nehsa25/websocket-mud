import BasePage from './base.page';

export default class GitPage extends BasePage {
    override name: string = "git-page";
    pathstem: string = '#/git';
    private _headertitle: string = "git";
    private _title = 'nehsa.net | git';
    get headerTitle(): string { return this._headertitle }
    get title(): string { return this._title }    
    get path(): string { return `${this.settings.APP_ENVIRONMENT}/${this.pathstem}`; };

    // locators
    get getHeaderTitle() { return this.page.getByTestId('header-title'); }
}
