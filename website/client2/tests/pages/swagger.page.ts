import BasePage from './base.page';

export default class SwaggerPage extends BasePage {
    override name: string = "swagger-page";
    pathstem: string = '#/swagger';
    private _headertitle: string = "Swagger";
    private _title = 'nehsa.net | Swagger Documentation';
    get headerTitle(): string { return this._headertitle }
    get title(): string { return this._title }    
    get path(): string { return `${this.settings.APP_ENVIRONMENT}/${this.pathstem}`; };

    // locators
    get getHeaderTitle() { return this.page.getByTestId('header-title'); }
}
