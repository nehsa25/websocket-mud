import BasePage from './base.page';

export default class PythonPage extends BasePage {
    override name: string = "python-page";
    pathstem: string = '#/python';
    private _headertitle: string = "Python";
    private _title = 'nehsa.net | Python';
    get headerTitle(): string { return this._headertitle }
    get title(): string { return this._title }    
    get path(): string { return `${this.settings.APP_ENVIRONMENT}/${this.pathstem}`; };

    // locators
    get getHeaderTitle() { return this.page.getByTestId('header-title'); }
}
