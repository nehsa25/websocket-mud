import BasePage from './base.page';

export default class AboutPage extends BasePage {
    name: string = "about-page";
    pathstem: string = '#/about';
    private _headertitle: string = "About";
    private _title = 'nehsa.net | About';
    get headerTitle(): string { return this._headertitle }
    get title(): string { return this._title }    
    get path(): string { return `${this.settings.APP_ENVIRONMENT}/${this.pathstem}`; };

    // locators
    get getHeaderTitle() { return this.page.getByTestId('header-title'); }

}
