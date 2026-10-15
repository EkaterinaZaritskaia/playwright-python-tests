import re
from pathlib import Path

from playwright.sync_api import Page, expect

PAGE_URL = (Path(__file__).resolve().parents[2] / "pages" / "02-schema-viewer-layouts.html").as_uri()


def test_page_without_deprecated_operations_has_no_deprecated_filter(page: Page):
    page.goto(PAGE_URL)

    expect(page.locator(".filter-chip")).to_have_count(4)
    expect(page.locator(".filter-chip.deprecated")).to_have_count(0)


def test_clicking_ref_link_opens_referenced_component(page: Page):
    page.goto(PAGE_URL)

    operation = page.locator("#op-post--multi-ref")
    operation.locator(".accordion-header").click()

    operation.locator("a.ref-link[href='#acc2-ref-Child']").click()

    expect(page.locator("#acc2-ref-Child")).to_have_attribute("open", "")
    expect(page.locator("#acc2-ref-Child .ref-component-content")).to_be_visible()
    expect(page).to_have_url(re.compile("#acc2-ref-Child$"))


def test_hovering_hit_cell_shows_hit_count_tooltip(page: Page):
    page.goto(PAGE_URL)

    operation = page.locator("#op-post--multi-ref")
    operation.locator(".accordion-header").click()

    cell = operation.locator(".cell.v.hit").first
    cell.hover()

    expect(cell).to_have_attribute("data-tip", "Valid hit - 1 time")


def test_tooltip_uses_plural_for_several_hits(page: Page):
    page.goto(PAGE_URL)

    operation = page.locator("#op-post--multi-ref")
    operation.locator(".accordion-header").click()

    cell = operation.locator(".cell.v.hit", has_text="2").first
    cell.hover()

    expect(cell).to_have_attribute("data-tip", "Valid hit - 2 times")


def test_hovering_miss_cell_shows_never_tested_tooltip(page: Page):
    page.goto(PAGE_URL)

    operation = page.locator("#op-post--multi-ref")
    operation.locator(".accordion-header").click()

    cell = operation.locator(".cell.i.miss").first
    cell.hover()

    expect(cell).to_have_attribute("data-tip", "Invalid never tested")

def test_hovering_na_cell_shows_not_applicable_tooltip(page: Page):
    page.goto(PAGE_URL)

    operation = page.locator("#op-post--multi-ref")
    operation.locator(".accordion-header").click()
    operation.locator("a.ref-link[href='#acc2-ref-Sibling']").click()

    cell =operation.locator(".cell.i.na").first
    cell.hover()

    expect(cell).to_have_attribute("data-tip", "Invalid not applicable for this keyword")


