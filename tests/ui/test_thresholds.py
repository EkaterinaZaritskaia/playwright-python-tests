import re

import pytest
from playwright.sync_api import expect


@pytest.mark.parametrize(
    ("file_name", "message", "result"),
    [
        ("06a-threshold-all-met.html", "5 thresholds met", "pass"),
        ("06b-threshold-single-met.html", "1 threshold met", "pass"),
        ("06c-threshold-some-missed.html", "1 of 3 thresholds missed", "fail"),
        ("06d-threshold-all-missed.html", "2 thresholds missed", "fail"),
        ("06e-threshold-single-missed.html", "1 threshold missed", "fail"),
        ("06f-threshold-response-keywords-only.html", "1 threshold met", "pass"),
    ]
)


def test_treshold_verdict(open_page, file_name, message, result):
    report = open_page(file_name)
    verdict = report.locator(".time .tv")

    expect(verdict).to_have_text(message)
    expect(verdict).to_have_class(re.compile(result))
