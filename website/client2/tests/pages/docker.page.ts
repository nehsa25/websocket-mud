import BasePage from './base.page';

export default class DockerPage extends BasePage {
    override name: string = "docker-page";
    pathstem: string = '#/docker';
    private _headertitle: string = "Docker";
    private _title = 'nehsa.net | Docker';
    get headerTitle(): string { return this._headertitle }
    get title(): string { return this._title }    
    get path(): string { return `${this.settings.APP_ENVIRONMENT}/${this.pathstem}`; };

    // locators
    get getHeaderTitle() { return this.page.getByTestId('header-title'); }
}
