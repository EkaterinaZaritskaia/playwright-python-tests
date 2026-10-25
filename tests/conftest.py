from pathlib import Path

import pytest
from playwright.sync_api import Page

PAGES_DIR = Path(__file__).resolve().parents[1] / "pages"


@pytest.fixture
def open_page(page: Page):
    def _open(file_name: str, query: str = "") -> Page:
        page.goto((PAGES_DIR / file_name).as_uri() + query)
        return page

    return _open


@pytest.fixture
def kitchen_sink(open_page) -> Page:
    return open_page("01-kitchen-sink.html")


@pytest.fixture
def schema_viewer(open_page) -> Page:
    return open_page("02-schema-viewer-layouts.html")


@pytest.fixture
def empty_spec(open_page) -> Page:
    return open_page("03-empty-spec.html")