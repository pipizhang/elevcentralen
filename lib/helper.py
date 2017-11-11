import hashlib
import requests
import shutil

def md5(string):
    return hashlib.md5(string.encode('utf-8')).hexdigest()

def download_image(driver, url, out_file):
    _cookies = driver.get_cookies()
    _data = {}
    for v in _cookies:
        _data[v['name']] = v['value']

    r = requests.get(url, stream=True, cookies=_data)
    if r.status_code == 200:
        with open(out_file, 'wb') as f:
            r.raw.decode_content = True
            shutil.copyfileobj(r.raw, f)
        del r

