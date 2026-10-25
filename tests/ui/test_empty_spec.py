from playwright.sync_api import Page, expect


def test_empty_report_has_no_operations(empty_spec: Page):
    expect(empty_spec.locator(".accordion")).to_have_count(0)
    expect(empty_spec.locator(".filter-chip .ct")).to_have_text(["0", "0", "0", "0"])


def test_empty_report_metrics_show_not_declared(empty_spec: Page):
    expect(empty_spec.locator(".mc .sub")).to_have_text(["not declared"]*5)


def test_report_time_shows_days_ago(page: Page, open_page):
    page.clock.set_fixed_time("2026-09-28T10:56:36Z")
    open_page("03-empty-spec.html")

    expect(page.locator(".time .rel")).to_have_text("1 day ago")


def test_report_time_uses_plural_for_several_days(page: Page, open_page):
    page.clock.set_fixed_time("2026-09-29T10:56:36Z")
    open_page("03-empty-spec.html")

    expect(page.locator(".time .rel")).to_have_text("2 days ago")


def test_report_time_for_just_now_time(page: Page, open_page):
    page.clock.set_fixed_time("2026-09-27T10:57:20Z")
    open_page("03-empty-spec.html")

    expect(page.locator(".time .rel")).to_have_text("just now")


def test_report_time_for_minute_ago_time(page: Page, open_page):
    page.clock.set_fixed_time("2026-09-27T10:57:21Z")
    open_page("03-empty-spec.html")

    expect(page.locator(".time .rel")).to_have_text("1 minute ago")


def test_feedback_link_opens_in_new_tab(empty_spec: Page):
    link = empty_spec.get_by_role("link", name="Help improve TraceCov: Share feedback")

    expect(link).to_have_attribute("target", "_blank")
    expect(link).to_have_attribute("rel", "noopener")


def test_brand_link_opens_in_new_tab(empty_spec: Page):
    link = empty_spec.locator(".report-footer-brand")

    expect(link).to_have_attribute("target", "_blank")
    expect(link).to_have_attribute("rel", "noopener")

