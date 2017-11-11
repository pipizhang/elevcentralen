import models
import helper
import config as cfg

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
        helper.download_image(driver, self.big_img_url, self.get_file_path())

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
                mchoice.status == self.status
                mchoice.save()

class Question:

    def __init__(self, content, image):
        self.content = content.strip()
        self.image = None
        self.code = ""
        self.choices = []

    def add_choice(self, choice):
        self.choices.append(choice)

    def add_image(self, image):
        self.image = Image(image)

    def get_code(self):
        arr = []
        arr.append(helper.md5(self.connect))
        for v in self.choices:
            arr.append(v.code)

        return helper.md5(''.join(arr))

    def is_new(self):
        n = models.Question.select().where(models.Question.code == self.code).count()
        return (True if n == 0 else False)

    def is_known(self):
        for v in self.choices:
            if v.status == 1:
                return True
        return False

    def add_or_update(self):

        if self.is_new():
            mquestion = models.Question.create(content = self.content, code = self.code, image = self.image.get_file_name(), is_known = self.is_known())
        else:
            mquestion = models.Question.select().where(models.Question.code == self.code).get()
            if not mquestion.is_known
                mchoice.is_known = self.is_known()
                mchoice.save()

        for v in self.choices:
            v.question_id = mquestion.id
            v.add_or_update()

