import os
from . import models
from . import helper
from . import config as cfg

class Image:

    def __init__(self, url):
        self.small_img_url = url
        self.big_img_url = url.replace("n.jpg", ".jpg")

    def get_file_name(self):
        name = helper.md5(self.big_img_url)
        return "%s.jpg" % name

    def get_file_path(self):
        return "%s/%s" % (cfg.get("images"), self.get_file_name())

    def download(self, driver):
        print(" - download %s" % self.big_img_url)
        helper.download_image(driver, self.big_img_url, self.get_file_path())

class Screenshot:

    def __init__(self, iquestion):
        self.iquestion = iquestion

    def take(self, driver):
        name = self.iquestion.code
        out_file = "%s/%s.png" % (cfg.get("screenshots"), name)
        if not os.path.isfile(out_file):
            self._process(driver, out_file)
        else:
            if self.iquestion.is_known():
                self._process(driver, out_file)

    def _process(self, driver, out_file):
        print(" - screenshot %s" % out_file)
        driver.get_screenshot_as_file(out_file)
        if os.path.isfile("/usr/bin/mogrify"):
            os.system("/usr/bin/mogrify -crop 940x540+60+65 '%s'" % out_file)

class Choice:

    def __init__(self, content, status):
        self.content = content.strip()
        self.status = status
        self.code = helper.md5(self.content)
        self.question_id = 0

    def in_new(self):
        n = models.Choice.select().where(models.Choice.code == self.code, models.Choice.question_id == self.question_id).count()
        return (True if n == 0 else False)

    def add_or_update(self):
        if self.in_new():
            mchoice = models.Choice.create(question_id = self.question_id, content = self.content, status = self.status, code = self.code)
        else:
            mchoice = models.Choice.get(models.Choice.question_id == self.question_id, models.Choice.code == self.code)
            if mchoice.status == 0 and self.status != 0:
                mchoice.status = self.status
                mchoice.save()

class Question:

    def __init__(self, content, image):
        self.content = content.strip()
        self.image = Image(image)
        self.code = ""
        self.choices = []

    def add_choice(self, choice):
        self.choices.append(choice)

    def get_code(self):
        arr = []
        arr.append(helper.md5(self.content))
        for v in self.choices:
            arr.append(v.code)

        return helper.md5(''.join(arr))

    def set_code(self):
        if len(self.choices) == 0:
            raise RuntimeError("question must has choices")
        self.code = self.get_code()

    def is_new(self):
        n = models.Question.select().where(models.Question.code == self.code).count()
        return (True if n == 0 else False)

    def is_known(self):
        for v in self.choices:
            if v.status == 1:
                return True
        return False

    """ Update the known incorrect choice """
    def update_choice_status(self, question_id):
        mquestion = models.Question.select().where(models.Question.id == question_id).get()
        if mquestion.is_known:
            mchoices = models.Choice.select().where(models.Choice.question_id == question_id)
            for mchoice in mchoices:
                if mchoice.status == 0:
                    mchoice.status = -1
                    mchoice.save()

    def add_or_update(self):

        if self.is_new():

            mquestion = models.Question.create(content = self.content, code = self.code, image = self.image.get_file_name(), is_known = self.is_known())
            print(" - add a new question, id: %d" % mquestion.id)

        else:

            mquestion = models.Question.select().where(models.Question.code == self.code).get()
            print(" - find a old question, id: %d" % mquestion.id)
            if (not mquestion.is_known) and self.is_known():
                mquestion.is_known = self.is_known()
                mquestion.save()

        for v in self.choices:
            v.question_id = mquestion.id
            v.add_or_update()

        self.update_choice_status(mquestion.id)




