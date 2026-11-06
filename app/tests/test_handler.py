import os
import sys

os.environ.setdefault("AWS_DEFAULT_REGION", "eu-west-1")
os.environ.setdefault("TABLE_NAME", "test")
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

import lambda_function as lf


def test_valid_urls():
    assert lf.is_valid_url("https://example.com/a")
    assert lf.is_valid_url("http://example.com")


def test_invalid_urls():
    assert not lf.is_valid_url("javascript:alert(1)")
    assert not lf.is_valid_url("ftp://example.com")
    assert not lf.is_valid_url(None)


def test_short_id_length():
    assert len(lf.generate_short_id()) == 6