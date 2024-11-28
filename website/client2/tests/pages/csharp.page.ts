import BasePage from './base.page';

export default class CSharpPage extends BasePage {
    override name: string = "c#-page";
    pathstem: string = '#/csharp';
    private _headertitle: string = "C# (.NET)";
    private _title = 'nehsa.net | C#';
    get headerTitle(): string { return this._headertitle }
    get title(): string { return this._title }    
    get path(): string { return `${this.settings.APP_ENVIRONMENT}/${this.pathstem}`; };

    // locators
    get getHeaderTitle() { return this.page.getByTestId('header-title'); }
}
