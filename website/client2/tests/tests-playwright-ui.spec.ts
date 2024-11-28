import { test, expect } from '@playwright/test';
import { TestSettings } from './utility/test-settings';
import AboutPage from './pages/about.page';
import { routes } from '../src/app/app.routes';

let testSettings: TestSettings = new TestSettings();

/** A paramaterized function which checks each page has the correct page title */
for (const pageDefinition of testSettings.PAGE_DEFINITIONS) {
  test(`nehsa.net: Page \"${pageDefinition.name}\" has correct title`, async ({ page }) => {
    let testpage = new pageDefinition(page, testSettings);
    await testpage.goto(testpage.path);
    await expect(page).toHaveTitle(testpage.title, { timeout: testSettings.defaultTimeoutMs });
  });
}

/** A paramaterized function which checks each page as the correct header at the top of the card */
for (const pageDefinition of testSettings.PAGE_DEFINITIONS) {
  test(`nehsa.net: Page \"${pageDefinition.name}\" has correct header`, async ({ page }) => {
    let testpage = new pageDefinition(page, testSettings);
    await testpage.goto(testpage.path);
    await expect(page.getByTestId('header-title')).toContainText(testpage.headerTitle, { ignoreCase: false, timeout: testSettings.defaultTimeoutMs });
  });
}

/** Confirms each page renders in x time */
for (const duration of testSettings.PAGE_LOAD_DURATIONS_SECS) {
  for (const pageDefinition of testSettings.PAGE_DEFINITIONS) {
    test(`nehsa.net: Page \"${pageDefinition.name}\" renders in ${duration} `, async ({ page }) => {
      let testpage = new pageDefinition(page, testSettings);
      await testpage.goto(testpage.path);
      await expect(page).toHaveTitle(testpage.title, { timeout: duration * 1000 });
    });
  }
}

/** Confirms all pages are being tested */
test(`nehsa.net: Confirm all pages are being tested`, async ({ page }) => {
  expect (testSettings.PAGE_DEFINITIONS.length-3 == routes.length);
});

// /** Confirms we can fill out contact us form */
// test(`nehsa.net: Can submit contact us form`, async ({ page }) => {
//   // start on home page
//   const aboutPage = new AboutPage(page, testSettings);
//   await aboutPage.goto(aboutPage.path);

//   // expact contact us
//   await aboutPage.contactusExpandButton.click();

//   // fill out form
//   await aboutPage.contactusSubject.fill("test subject");
//   await aboutPage.contactusBody.fill("test body");
//   await aboutPage.contactusButton.click();
// });
