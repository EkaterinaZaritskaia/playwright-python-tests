from pathlib import Path
import re
import pytest
from playwright.sync_api import Page, expect


PAGE_URL = (Path(__file__).resolve().parents[2] / "pages" / "01-kitchen-sink.html").as_uri()


@pytest.fixture
def report_page(page: Page):
    page.goto(PAGE_URL)
    return page


def test_report_title(report_page: Page):

    expect(report_page).to_have_title("Kitchen sink - all row states")


def test_search_shows_only_matching_operations(report_page: Page):
    report_page.locator("#search-input").fill("audit")

    visible_rows = report_page.locator(".accordion:visible")
    expect(visible_rows).to_have_count(1)
    expect(visible_rows.locator(".operation")).to_have_text("/api/v1/{id}/audit")


def test_search_without_matches_shows_empty_state(report_page: Page):
    report_page.locator("#search-input").fill("no-such-operation")

    expect(report_page.locator("#empty-state")).to_be_visible()
    expect(report_page.locator("#empty-state-title")).to_have_text("No operations match")


def test_clear_button_restores_all_operations(report_page: Page):
    report_page.locator("#search-input").fill("audit")

    report_page.locator(".clear-btn").click()

    expect(report_page.locator("#search-input")).to_have_value("")
    expect(report_page.locator(".accordion:visible")).to_have_count(14)


def test_search_is_case_insensitive(report_page: Page):
    report_page.locator("#search-input").fill("AUDIT")

    expect(report_page.locator(".accordion:visible")).to_have_count(1)


def test_uncovered_filter_hides_uncovered_operations(report_page: Page):
    report_page.locator(".filter-chip.uncovered").click()

    expect(report_page.locator(".accordion:visible")).to_have_count(7)
    expect(report_page.locator(".accordion[data-covered='uncovered']:visible")).to_have_count(0)


def test_clicking_status_filters_turns_them_off(report_page: Page):
    report_page.locator(".filter-chip.covered").click()
    report_page.locator(".filter-chip.partial").click()
    report_page.locator(".filter-chip.uncovered").click()

    expect(report_page.locator(".filter-chip.covered")).to_have_attribute("aria-pressed", "false")
    expect(report_page.locator(".filter-chip.partial")).to_have_attribute("aria-pressed", "false")
    expect(report_page.locator(".filter-chip.uncovered")).to_have_attribute("aria-pressed", "false")


def test_clicking_filter_adds_filter_param_to_url(report_page: Page):
    report_page.locator(".filter-chip.covered").click()

    expect(report_page).to_have_url(re.compile(r"filter=partial%2Cuncovered%2Cunmeasurable$"))


def test_restoring_default_filters_removes_filter_param_from_url(report_page: Page):
    report_page.locator(".filter-chip.covered").click()
    report_page.locator(".filter-chip.covered").click()

    expect(report_page).not_to_have_url(re.compile("filter="))


def test_clicking_toggle_all_twice_collapses_operations_back(report_page: Page):
    report_page.locator("#toggle-all").click()
    expect(report_page.locator("#toggle-all")).to_have_text("Collapse all")

    report_page.locator("#toggle-all").click()
    expect(report_page.locator("#toggle-all")).to_have_text("Expand all")
    expect(report_page.locator(".accordion-content:visible")).to_have_count(0)


def test_opening_url_with_filter_applies_it(page: Page):
    page.goto(PAGE_URL + "?filter=covered")

    expect(page.locator(".accordion:visible")).to_have_count(4)
    expect(page.locator(".filter-chip.partial")).to_have_attribute("aria-pressed", "false")


def test_search_ignores_surrounding_spaces(report_page: Page):
    report_page.locator("#search-input").fill(" audit ")

    expect(report_page.locator(".accordion:visible")).to_have_count(1)


def test_search_hides_groups_without_matches(report_page: Page):
    report_page.locator("#search-input").fill("pets")

    expect(report_page.locator("details.group:visible")).to_have_count(1)
    expect(report_page.locator("details.group:visible .group-name")).to_have_text("pets")


def test_clicking_operation_expands_its_details(report_page: Page):
    first_operation = report_page.locator(".accordion:visible").first
    first_operation.locator(".accordion-header").click()

    expect(first_operation.locator(".accordion-content")).to_be_visible()


def test_deprecated_operations_hidden_by_default(report_page: Page):
    expect(report_page.locator(".accordion:visible")).to_have_count(14)


def test_deprecated_filter_shows_all_operations(report_page: Page):
    report_page.locator(".filter-chip.deprecated").click()

    expect(report_page.locator(".accordion:visible")).to_have_count(16)
