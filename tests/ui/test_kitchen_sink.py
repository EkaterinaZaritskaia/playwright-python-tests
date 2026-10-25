import re
from playwright.sync_api import Page, expect


def test_report_title(kitchen_sink: Page):

    expect(kitchen_sink).to_have_title("Kitchen sink - all row states")


def test_search_shows_only_matching_operations(kitchen_sink: Page):
    kitchen_sink.locator("#search-input").fill("audit")

    visible_rows = kitchen_sink.locator(".accordion:visible")
    expect(visible_rows).to_have_count(1)
    expect(visible_rows.locator(".operation")).to_have_text("/api/v1/{id}/audit")


def test_search_without_matches_shows_empty_state(kitchen_sink: Page):
    kitchen_sink.locator("#search-input").fill("no-such-operation")

    expect(kitchen_sink.locator("#empty-state")).to_be_visible()
    expect(kitchen_sink.locator("#empty-state-title")).to_have_text("No operations match")


def test_clear_button_restores_all_operations(kitchen_sink: Page):
    kitchen_sink.locator("#search-input").fill("audit")

    kitchen_sink.locator(".clear-btn").click()

    expect(kitchen_sink.locator("#search-input")).to_have_value("")
    expect(kitchen_sink.locator(".accordion:visible")).to_have_count(14)


def test_search_is_case_insensitive(kitchen_sink: Page):
    kitchen_sink.locator("#search-input").fill("AUDIT")

    expect(kitchen_sink.locator(".accordion:visible")).to_have_count(1)


def test_uncovered_filter_hides_uncovered_operations(kitchen_sink: Page):
    kitchen_sink.locator(".filter-chip.uncovered").click()

    expect(kitchen_sink.locator(".accordion:visible")).to_have_count(7)
    expect(kitchen_sink.locator(".accordion[data-covered='uncovered']:visible")).to_have_count(0)


def test_clicking_status_filters_turns_them_off(kitchen_sink: Page):
    kitchen_sink.locator(".filter-chip.covered").click()
    kitchen_sink.locator(".filter-chip.partial").click()
    kitchen_sink.locator(".filter-chip.uncovered").click()

    expect(kitchen_sink.locator(".filter-chip.covered")).to_have_attribute("aria-pressed", "false")
    expect(kitchen_sink.locator(".filter-chip.partial")).to_have_attribute("aria-pressed", "false")
    expect(kitchen_sink.locator(".filter-chip.uncovered")).to_have_attribute("aria-pressed", "false")


def test_clicking_filter_adds_filter_param_to_url(kitchen_sink: Page):
    kitchen_sink.locator(".filter-chip.covered").click()

    expect(kitchen_sink).to_have_url(re.compile(r"filter=partial%2Cuncovered%2Cunmeasurable$"))


def test_restoring_default_filters_removes_filter_param_from_url(kitchen_sink: Page):
    kitchen_sink.locator(".filter-chip.covered").click()
    kitchen_sink.locator(".filter-chip.covered").click()

    expect(kitchen_sink).not_to_have_url(re.compile("filter="))


def test_clicking_toggle_all_twice_collapses_operations_back(kitchen_sink: Page):
    kitchen_sink.locator("#toggle-all").click()
    expect(kitchen_sink.locator("#toggle-all")).to_have_text("Collapse all")

    kitchen_sink.locator("#toggle-all").click()
    expect(kitchen_sink.locator("#toggle-all")).to_have_text("Expand all")
    expect(kitchen_sink.locator(".accordion-content:visible")).to_have_count(0)


def test_opening_url_with_filter_applies_it(open_page):
    report = open_page("01-kitchen-sink.html", "?filter=covered")

    expect(report.locator(".accordion:visible")).to_have_count(4)
    expect(report.locator(".filter-chip.partial")).to_have_attribute("aria-pressed", "false")


def test_search_ignores_surrounding_spaces(kitchen_sink: Page):
    kitchen_sink.locator("#search-input").fill(" audit ")

    expect(kitchen_sink.locator(".accordion:visible")).to_have_count(1)


def test_search_hides_groups_without_matches(kitchen_sink: Page):
    kitchen_sink.locator("#search-input").fill("pets")

    expect(kitchen_sink.locator("details.group:visible")).to_have_count(1)
    expect(kitchen_sink.locator("details.group:visible .group-name")).to_have_text("pets")


def test_clicking_operation_expands_its_details(kitchen_sink: Page):
    first_operation = kitchen_sink.locator(".accordion:visible").first
    first_operation.locator(".accordion-header").click()

    expect(first_operation.locator(".accordion-content")).to_be_visible()


def test_deprecated_operations_hidden_by_default(kitchen_sink: Page):
    expect(kitchen_sink.locator(".accordion:visible")).to_have_count(14)


def test_deprecated_filter_shows_all_operations(kitchen_sink: Page):
    kitchen_sink.locator(".filter-chip.deprecated").click()

    expect(kitchen_sink.locator(".accordion:visible")).to_have_count(16)
