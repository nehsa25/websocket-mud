import BasePage from './base.page';

export default class GithubPage extends BasePage {
    override name: string = "github-page";
    pathstem: string = '#/github';
    private _headertitle: string = "Github";
    private _title = 'nehsa.net | Github';
    get headerTitle(): string { return this._headertitle }
    get title(): string { return this._title }    
    get path(): string { return `${this.settings.APP_ENVIRONMENT}/${this.pathstem}`; };

    // locators
    get getHeaderTitle() { return this.page.getByTestId('header-title'); }

}
