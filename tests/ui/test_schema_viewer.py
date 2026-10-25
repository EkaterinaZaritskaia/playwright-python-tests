import re

from playwright.sync_api import Page, expect


def test_page_without_deprecated_operations_has_no_deprecated_filter(schema_viewer: Page):

    expect(schema_viewer.locator(".filter-chip")).to_have_count(4)
    expect(schema_viewer.locator(".filter-chip.deprecated")).to_have_count(0)


def test_clicking_ref_link_opens_referenced_component(schema_viewer: Page):
    operation = schema_viewer.locator("#op-post--multi-ref")
    operation.locator(".accordion-header").click()

    operation.locator("a.ref-link[href='#acc2-ref-Child']").click()

    expect(schema_viewer.locator("#acc2-ref-Child")).to_have_attribute("open", "")
    expect(schema_viewer.locator("#acc2-ref-Child .ref-component-content")).to_be_visible()
    expect(schema_viewer).to_have_url(re.compile("#acc2-ref-Child$"))


def test_hovering_hit_cell_shows_hit_count_tooltip(schema_viewer: Page):
    operation = schema_viewer.locator("#op-post--multi-ref")
    operation.locator(".accordion-header").click()

    cell = operation.locator(".cell.v.hit").first
    cell.hover()

    expect(cell).to_have_attribute("data-tip", "Valid hit - 1 time")


def test_tooltip_uses_plural_for_several_hits(schema_viewer: Page):
    operation = schema_viewer.locator("#op-post--multi-ref")
    operation.locator(".accordion-header").click()

    cell = operation.locator(".cell.v.hit", has_text="2").first
    cell.hover()

    expect(cell).to_have_attribute("data-tip", "Valid hit - 2 times")


def test_hovering_miss_cell_shows_never_tested_tooltip(schema_viewer: Page):
    operation = schema_viewer.locator("#op-post--multi-ref")
    operation.locator(".accordion-header").click()

    cell = operation.locator(".cell.i.miss").first
    cell.hover()

    expect(cell).to_have_attribute("data-tip", "Invalid never tested")

def test_hovering_na_cell_shows_not_applicable_tooltip(schema_viewer: Page):
    operation = schema_viewer.locator("#op-post--multi-ref")
    operation.locator(".accordion-header").click()
    operation.locator("a.ref-link[href='#acc2-ref-Sibling']").click()

    cell =operation.locator(".cell.i.na").first
    cell.hover()

    expect(cell).to_have_attribute("data-tip", "Invalid not applicable for this keyword")


