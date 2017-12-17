import pytest
import lib.items as items

def test_image():
    image = items.Image("http://www.example.com/img/testn.jpg")
    assert image.big_img_url  == "http://www.example.com/img/test.jpg"
