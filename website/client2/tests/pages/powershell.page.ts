import BasePage from './base.page';

export default class PowershellPage extends BasePage {
    override name: string = "powershell-page";
    pathstem: string = '#/powershell';
    private _headertitle: string = "Powershell";
    private _title = 'nehsa.net | Powershell';
    get headerTitle(): string { return this._headertitle }
    get title(): string { return this._title }    
    get path(): string { return `${this.settings.APP_ENVIRONMENT}/${this.pathstem}`; };

    // locators
    get getHeaderTitle() { return this.page.getByTestId('header-title'); }
}
