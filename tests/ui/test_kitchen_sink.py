from pathlib import Path
import re
from playwright.sync_api import Page, expect


PAGE_URL = (Path(__file__).resolve().parents[2] / "pages" / "01-kitchen-sink.html").as_uri()

def test_report_title(page: Page):
    page.goto(PAGE_URL)

    expect(page).to_have_title("Kitchen sink - all row states")


def test_search_shows_only_matching_operations(page: Page):
    page.goto(PAGE_URL)

    page.locator("#search-input").fill("audit")

    visible_rows = page.locator(".accordion:visible")
    expect(visible_rows).to_have_count(1)
    expect(visible_rows.locator(".operation")).to_have_text("/api/v1/{id}/audit")


def test_search_without_matches_shows_empty_state(page: Page):
    page.goto(PAGE_URL)

    page.locator("#search-input").fill("no-such-operation")

    expect(page.locator("#empty-state")).to_be_visible()
    expect(page.locator("#empty-state-title")).to_have_text("No operations match")


def test_clear_button_restores_all_operations(page: Page):
    page.goto(PAGE_URL)

    page.locator("#search-input").fill("audit")

    page.locator(".clear-btn").click()

    expect(page.locator("#search-input")).to_have_value("")
    expect(page.locator(".accordion:visible")).to_have_count(14)


def test_uncovered_filter_hides_uncovered_operations(page: Page):
    page.goto(PAGE_URL)

    page.locator(".filter-chip.uncovered").click()

    expect(page.locator(".accordion:visible")).to_have_count(7)
    expect(page.locator(".accordion[data-covered='uncovered']:visible")).to_have_count(0)


def test_clicking_status_filters_turns_them_off(page: Page):
    page.goto(PAGE_URL)

    page.locator(".filter-chip.covered").click()
    page.locator(".filter-chip.partial").click()
    page.locator(".filter-chip.uncovered").click()

    expect(page.locator(".filter-chip.covered")).to_have_attribute("aria-pressed", "false")
    expect(page.locator(".filter-chip.partial")).to_have_attribute("aria-pressed", "false")
    expect(page.locator(".filter-chip.uncovered")).to_have_attribute("aria-pressed", "false")


def test_clicking_filter_adds_filter_param_to_url(page: Page):
    page.goto(PAGE_URL)

    page.locator(".filter-chip.covered").click()

    expect(page).to_have_url(re.compile(r"filter=partial%2Cuncovered%2Cunmeasurable$"))


def test_restoring_default_filters_removes_filter_param_from_url(page: Page):
    page.goto(PAGE_URL)

    page.locator(".filter-chip.covered").click()
    page.locator(".filter-chip.covered").click()

    expect(page).not_to_have_url(re.compile("filter="))


def test_clicking_toggle_all_twice_collapses_operations_back(page: Page):
    page.goto(PAGE_URL)

    page.locator("#toggle-all").click()
    expect(page.locator("#toggle-all")).to_have_text("Collapse all")

    page.locator("#toggle-all").click()
    expect(page.locator("#toggle-all")).to_have_text("Expand all")
    expect(page.locator(".accordion-content:visible")).to_have_count(0)

