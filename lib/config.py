import os
import yaml

ROOT_PATH = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
settings = {}
cfg_file = "%s/config/app.yml" % ROOT_PATH

if os.path.isfile(cfg_file):
    settings = yaml.safe_load(open(cfg_file))
else:
    raise IOError("Not found config file")

def get(key):
    if key in ["database", "images", "screenshots", "chromedriver"]:
        if not os.path.isabs(settings[key]):
            settings[key] = "%s/%s" % (ROOT_PATH, settings[key])
    return settings[key]
