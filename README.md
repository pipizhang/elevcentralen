# elevcentralen
[![Build Status](https://travis-ci.org/pipizhang/elevcentralen.svg?branch=master)](https://travis-ci.org/pipizhang/elevcentralen)

Scrape Elevcentralen content with python-selenium. This app is a exercise of scraping a SPA content.

> Note: Please do not use it for persisting data and any business purpose.

### Features
* Scraping driving licence questions data (text and images)
* Get the correct answer from unknown question by analysis data
* Screenshot of question page
* Croping screenshot

### Install
```
pip install -r requirements.txt
```

```python
# create db and tables
from lib import models
models.setup(True)
```

