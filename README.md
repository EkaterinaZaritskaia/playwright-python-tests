# playwright-python-tests

UI tests for an interactive API coverage report, written in Python with pytest and Playwright.

Test pages are TraceCov reports © Schemathesis.io s.r.o., used with permission.

## What is tested

`tests/ui/test_kitchen_sink.py` covers an interactive API coverage report page:

- search by operation path, including the "no results" empty state
- clearing the search
- coverage status filters and their `aria-pressed` state
- filter state saved in the page URL
- Expand all / Collapse all

## Run

```bash
pip install -r requirements.txt
playwright install chromium
pytest -v
```

To watch the browser: `pytest -v --headed --slowmo 500`
