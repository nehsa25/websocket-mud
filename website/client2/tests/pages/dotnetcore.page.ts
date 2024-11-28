import BasePage from './base.page';

export default class DotNetCorePage extends BasePage {
    override name: string = "dotnetcore-page";
    pathstem: string = '#/core';
    private _headertitle: string = "C# (.NET Core)";
    private _title = 'nehsa.net | .NET Core';
    get headerTitle(): string { return this._headertitle }
    get title(): string { return this._title }    
    get path(): string { return `${this.settings.APP_ENVIRONMENT}/${this.pathstem}`; };

    // locators
    get getHeaderTitle() { return this.page.getByTestId('header-title'); }
}
