#!/usr/bin/env python
import os
from lib import config as cfg
from lib import pages
from selenium import webdriver

class ElevcentralenScraper:

    def __init__(self):
        pass

    def run(self):
        self.init_browser()
        try:

            pages.LoginPage(self.driver).open()
            pages.DashboardPage(self.driver).open()
            pages.TestProgressPage(self.driver).open()

        except Exception as e:
            print(str(e))
        finally:
            self.driver.quit()

    def init_browser(self):
        self.use_chrome()
        self.driver.set_window_size(1024, 768)

    def use_chrome(self):
        chromedriver = cfg.get("chromedriver")
        os.environ["webdriver.chrome.driver"] = chromedriver
        self.driver = webdriver.Chrome(chromedriver)

    def use_phantomjs(self):
        dcap = dict(DesiredCapabilities.PHANTOMJS)
        dcap["phantomjs.page.settings.userAgent"] = cfg.get("user_agent")
        self.driver = webdriver.PhantomJS(desired_capabilities=dcap)


if __name__ == '__main__':
    app = ElevcentralenScraper()
    app.run()


