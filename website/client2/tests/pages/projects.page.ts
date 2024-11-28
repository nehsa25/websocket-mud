import BasePage from './base.page';

export default class ProjectsPage extends BasePage {
    override name: string = "projects-page";
    pathstem: string = '#/projects';
    private _headertitle: string = "Projects";
    private _title = 'nehsa.net | Projects';
    get headerTitle(): string { return this._headertitle }
    get title(): string { return this._title }    
    get path(): string { return `${this.settings.APP_ENVIRONMENT}/${this.pathstem}`; };

    // locators
    get getHeaderTitle() { return this.page.getByTestId('header-title'); }
}
