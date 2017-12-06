import os
import time
import sys
import random
import re
from . import config as cfg
from . import models
from . import helper
from . import items

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.common.exceptions import NoSuchElementException

class Page(object):
    name = "NULL"

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(self.driver, 10)
        print(">> page %s" % type(self).name)

    def open(self):
        self._open()
        if not self._validate():
            raise Exception("PAGE %s is invalid" % type(self).name)
        self._process()
        self._next()
        time.sleep(5)

    def _open(self):
        pass

    def _validate(self):
        return True

    def _process(self):
        pass

    def _next(self):
        pass

class LoginPage(Page):
    name = "login"

    def _open(self):
        self.driver.get("https://www.elevcentralen.se/en/Login/Index")

    def _validate(self):
        try:
            self.wait.until(EC.visibility_of_element_located((By.ID, "Username")))
            return True
        except:
            return False

    def _process(self):
        self.driver.find_element_by_id("Username").send_keys(cfg.get("elevcentralen")['username'])
        self.driver.find_element_by_id("Password").send_keys(cfg.get("elevcentralen")['password'])
        self.driver.find_element_by_xpath("//input[@type='submit']").submit()

class DashboardPage(Page):
    name = "dashboard"

    def _validate(self):
        return True

    def _process(self):
        self.driver.find_elements_by_xpath("//div[@class='progress']")[0].click()

class TestProgressPage(Page):
    name = "test_progess"

    def _process(self):
        tests = self.driver.find_elements_by_xpath("//a[text()='Overview']")

        """ save js to memory to avoid the error of losing DOM reference """
        _onclick_dict = {}
        for el in tests:
            _onclick = el.get_attribute("onclick").strip().replace(" return false;", "")
            _m = re.search("TestOverview\/(\d+)\/", _onclick)
            if _m != None:
                _onclick_dict[_m[1]] = _onclick

        _onclick_sorted = sorted(_onclick_dict.items(), key=lambda kv:kv[0], reverse=True)

        for v in _onclick_sorted:
            _onclick = v[1]
            self._open_education_overview_page(_onclick)
            time.sleep(5)

    def _open_education_overview_page(self, js):
        self.driver.execute_script(js)
        EducationOverviewPage(self.driver).open()


class EducationOverviewPage(Page):
    name = "education_overview"

    def _validate(self):
        try:
            self.wait.until(EC.visibility_of_any_elements_located((By.CSS_SELECTOR, "div.modal-dialog")))
            return True
        except:
            return False

    def _process(self):
        questions = self.driver.find_elements_by_xpath("//div[@id='educationOverviewPage']//a")
        _onclick_list = []
        for el in questions:
            _onclick_list.append(el.get_attribute("onclick").strip().replace(" return false;", ""))
        self.driver.find_element_by_xpath("//div[@class='modal-footer']/button").click()

        n = 1
        for _onclick in _onclick_list:
            print(" # [%d - %d]" % (n, len(_onclick_list)))
            self._open_question_page(_onclick)
            n += 1
            time.sleep(5)

        self._quite_test()

    def _open_question_page(self, js):
        self.driver.execute_script(js)
        QuestionPage(self.driver).open()

    def _quite_test(self):
        js = "$.cookie('i18n.testId', null, { path: '/' }); $.removeCookie('i18n.testId', { path: '/' }); $.sc.getView('/Education/DrivingLicenceTest/Index', function() { $.sc.education.tests.init(); });"
        self.driver.execute_script(js)
        time.sleep(5)

class QuestionPage(Page):
    name = "question"

    def _validate(self):
        try:
            time.sleep(2)
            self.wait.until(EC.visibility_of_element_located((By.ID, "drivinglicencetest_question_form")))
            return True
        except:
            return False

    def _process(self):
        el_question = self.driver.find_elements_by_xpath("//form[@id='drivinglicencetest_question_form']//div[@class='col-sm-7']/p")[0]
        el_choices = self.driver.find_elements_by_xpath("//form[@id='drivinglicencetest_question_form']//div[contains(@class, 'questions')]/label")
        el_image = self.driver.find_elements_by_xpath("//form[@id='drivinglicencetest_question_form']//div[@class='col-sm-5']//img")[0]

        question_content = el_question.text
        question_image = el_image.get_attribute("src")

        # create Question
        iQuestion = items.Question(question_content, question_image)

        for el in el_choices:
            choice = {'content': el.text.strip(), 'status': 0}
            if self._check_child_exists(el, "span.success"):
                choice['status'] = 1
            elif self._check_child_exists(el, "span.danger"):
                choice['status'] = -1
            else:
                choice['status'] = 0
            # append choices to question
            iQuestion.add_choice(items.Choice(choice['content'], choice['status']))

        # set unique code
        iQuestion.set_code()

        if iQuestion.is_new():
            iQuestion.image.download(self.driver)

        iQuestion.add_or_update()

        # screenshot
        items.Screenshot(iQuestion).take(self.driver)

    def _check_child_exists(self, element, css):
        el = element.find_elements_by_css_selector(css)
        if len(el) > 0:
            return True
        else:
            return False

