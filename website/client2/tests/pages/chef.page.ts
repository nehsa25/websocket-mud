import BasePage from './base.page';

export default class ChefPage extends BasePage {
    override name: string = "chef-page";
    pathstem: string = '#/chef';
    private _headertitle: string = "Chef";
    private _title = 'nehsa.net | Chef';
    get headerTitle(): string { return this._headertitle }
    get title(): string { return this._title }    
    get path(): string { return `${this.settings.APP_ENVIRONMENT}/${this.pathstem}`; };

    // locators
    get getHeaderTitle() { return this.page.getByTestId('header-title'); }
}
