import BasePage from './base.page';

export default class SchoolPage extends BasePage {
    override name: string = "school-page";
    pathstem: string = '#/school';
    private _headertitle: string = "School";
    private _title = 'nehsa.net | School';
    get headerTitle(): string { return this._headertitle }
    get title(): string { return this._title }    
    get path(): string { return `${this.settings.APP_ENVIRONMENT}/${this.pathstem}`; };

    // locators
    get getHeaderTitle() { return this.page.getByTestId('header-title'); }
}
