import BasePage from './base.page';

export default class JenkinsPage extends BasePage {
    override name: string = "jenkins-page";
    pathstem: string = '#/jenkins';
    private _headertitle: string = "Jenkins";
    private _title = 'nehsa.net | Jenkins';
    get headerTitle(): string { return this._headertitle }
    get title(): string { return this._title }    
    get path(): string { return `${this.settings.APP_ENVIRONMENT}/${this.pathstem}`; };

    // locators
    get getHeaderTitle() { return this.page.getByTestId('header-title'); }

}
