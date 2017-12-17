import pytest
import lib.helper as helper

def test_md5():
    assert helper.md5("hello world") == "5eb63bbbe01eeed093cb22bb8f5acdc3"
