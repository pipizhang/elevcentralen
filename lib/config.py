import os
import yaml

ROOT_PATH = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
settings = {}
cfg_file = "%s/config/app.yml" % ROOT_PATH
cfg_example = "%s/config/app.example.yml" % ROOT_PATH

if os.path.isfile(cfg_file):
    settings = yaml.safe_load(open(cfg_file))
elif os.path.isfile(cfg_example):
    settings = yaml.safe_load(open(cfg_example))
else:
    raise IOError("Not found config file '%s'" % cfg_file)

def get(key):
    if key in ["database", "images", "screenshots", "chromedriver"]:
        if not os.path.isabs(settings[key]):
            settings[key] = "%s/%s" % (ROOT_PATH, settings[key])
    return settings[key]
