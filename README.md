# playwright-python-tests

UI tests for an interactive API coverage report, written in Python with pytest and Playwright.

Test pages are TraceCov reports © Schemathesis.io s.r.o., used with permission.

## What is tested

`tests/ui/test_kitchen_sink.py` covers an interactive API coverage report page:

- search by operation path, including the "no results" empty state
- search is case-insensitive and ignores surrounding spaces
- groups without matches are hidden during search
- clearing the search
- coverage status filters and their `aria-pressed` state
- deprecated operations hidden by default and shown by the Deprecated filter
- filter state saved in the page URL and restored when opening a link with filters
- expanding a single operation and Expand all / Collapse all

## Run

```bash
pip install -r requirements.txt
playwright install chromium
pytest -v
```

To watch the browser: `pytest -v --headed --slowmo 500`

`tests/ui/test_schema_viewer.py` covers a report page with schema details:

- no Deprecated filter when the report has no deprecated operations
- `$ref` links open the referenced schema component
- tooltips on schema cells: hit count (1 time / 2 times), never tested, not applicable