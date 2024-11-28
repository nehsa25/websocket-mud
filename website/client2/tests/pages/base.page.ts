
import { Page } from '@playwright/test';

/** This class is the base of all page and contains the header/footer elements/functions */
export default class BasePage {
    name: string = "#/basepage";
    constructor(public page: Page, public settings: any = null) {
        this.page = page;
        this.settings = settings;
    }

    // common locators
    get contactusSubject() { return this.page.getByTestId('contactus-subject'); }
    get contactusBody() { return this.page.getByTestId('contactus-body'); }
    get contactusExpandButton() { return this.page.getByTestId('contactus-expand-btn'); }
    get contactusButton() { return this.page.getByTestId('contactus-btn'); }

    // use website to navigate
    async navigateTo() { 
        throw new RangeError("N/A");
    }

    // go directly
    async goto(path: string) {
        await this.page.goto(path);
    }
}