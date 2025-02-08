import os
import time
import random
from playwright.sync_api import sync_playwright

class NaukriUpdate:
    def __init__(self, username, password):
        self.username = username
        self.password = password

        # Start Playwright
        self.playwright = sync_playwright().start()

        # Launch Chromium in headed mode (headless=False)
        self.browser = self.playwright.chromium.launch(
            headless=False,
            args=[
                "--disable-blink-features=AutomationControlled",
                "--disable-notifications",
                "--no-sandbox",
                "--disable-dev-shm-usage",
                "--window-size=1920,1080"
            ]
        )

        # Create a browser context with a custom user agent and viewport.
        self.context = self.browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36",
            viewport={"width": 1920, "height": 1080}
        )
        
        # Hide the webdriver flag
        self.context.add_init_script("""
            Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined
            });
        """)
        
        self.page = self.context.new_page()

    def login_and_update_profile(self):
        page = self.page
        try:
            # Open the Naukri homepage and wait a random period.
            page.goto("https://www.naukri.com/")
            time.sleep(random.uniform(5, 10))
            
            # Click the login layer.
            page.wait_for_selector("#login_Layer", timeout=40000)
            page.click("#login_Layer")
            
            # Fill in the login fields.
            page.wait_for_selector("xpath=//*[text()='Email ID / Username']/following-sibling::input", timeout=40000)
            page.fill("xpath=//*[text()='Email ID / Username']/following-sibling::input", self.username)
            page.wait_for_selector("xpath=//*[text()='Password']/following-sibling::input", timeout=40000)
            page.fill("xpath=//*[text()='Password']/following-sibling::input", self.password)
            
            # Click the login button.
            page.wait_for_selector("xpath=//button[@type='submit' and text()='Login']", timeout=40000)
            page.click("xpath=//button[@type='submit' and text()='Login']")
            
            # Wait briefly and reload the page.
            time.sleep(random.uniform(3, 5))
            page.reload()
            
            # Navigate to the profile page.
            page.wait_for_selector("xpath=//a[@href='/mnjuser/profile']", timeout=40000)
            page.click("xpath=//a[@href='/mnjuser/profile']")
            
            # Click the edit button for the resume headline.
            page.wait_for_selector("xpath=//div[@class='widgetHead']//span[text()='Resume headline']/following-sibling::span", timeout=40000)
            page.click("xpath=//div[@class='widgetHead']//span[text()='Resume headline']/following-sibling::span")
            
            # Update the resume headline.
            page.wait_for_selector("#resumeHeadlineTxt", timeout=40000)
            current_headline = page.input_value("#resumeHeadlineTxt")
            new_headline = current_headline.rstrip('.') + '.'
            page.fill("#resumeHeadlineTxt", new_headline)
            
            # Click the save button.
            page.wait_for_selector("xpath=//button[text()='Save']", timeout=40000)
            page.click("xpath=//button[text()='Save']")
            
            print("Profile updated successfully")
            
        except Exception as e:
            print(f"Error occurred: {e}")
            raise
            
        finally:
            self.context.close()
            self.browser.close()
            self.playwright.stop()

if __name__ == '__main__':
    time.sleep(random.uniform(0, 10))
    username = os.environ.get("NAUKRI_USERNAME")
    password = os.environ.get("NAUKRI_PASSWORD")

    if not username or not password:
        print("Missing credentials in environment variables")
        exit(1)

    updater = NaukriUpdate(username, password)
    updater.login_and_update_profile()
