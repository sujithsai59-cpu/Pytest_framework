# Selenium + Pytest UI Automation Framework

A Page Object Model (POM) test automation framework built with **Selenium
WebDriver** and **Pytest**, targeting [SauceDemo](https://www.saucedemo.com/) —
a public demo e-commerce site built for practicing UI automation.

This project demonstrates the kind of automation suite I build for real
clients: structured for maintainability, covering both smoke and regression
scenarios, integrated into CI, and with failure diagnostics built in.

## Why this design

| Decision | Reason |
|---|---|
| Page Object Model | Keeps locators and page logic out of test files, so a UI change only requires updating one page class, not every test that touches that page |
| Explicit waits only (no implicit wait) | Avoids flaky mixed-wait bugs that are one of the most common sources of unreliable Selenium suites |
| Config module (`utils/config.py`) | Environment/browser/user data lives in one place — switching test environments is a one-line change |
| Pytest markers (`smoke`, `regression`, `e2e`) | Lets a CI pipeline run a fast smoke suite on every push and a full regression suite on a schedule, instead of running everything every time |
| Auto screenshot-on-failure (`conftest.py` hook) | Every failed test leaves visual evidence, cutting down "was it a bug or a flaky test?" debugging time |
| GitHub Actions CI | Suite runs headless on every push/PR, with the HTML report and any failure screenshots uploaded as build artifacts |

## Coverage

- **Login**: valid login, locked-out user, empty/invalid credentials (parametrized)
- **Inventory**: add-to-cart badge counts, price sort (low↔high), name sort (A–Z)
- **Checkout**: full end-to-end purchase flow, and a required-field validation case

## Project structure

```
selenium-pytest-framework/
├── pages/                  # Page Object classes
│   ├── base_page.py        # Shared wait/interaction helpers
│   ├── login_page.py
│   ├── inventory_page.py
│   └── cart_page.py        # Cart + checkout page objects
├── tests/
│   ├── test_login.py
│   ├── test_inventory.py
│   └── test_checkout.py
├── utils/
│   └── config.py           # URLs, test users, env-driven settings
├── conftest.py              # Driver fixture + screenshot-on-failure hook
├── pytest.ini
├── requirements.txt
└── .github/workflows/tests.yml   # CI pipeline
```

## Running locally

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Run the full suite (headless by default)
pytest

# 3. Run just the smoke suite
pytest -m smoke

# 4. Run visibly (watch the browser) in Chrome
pytest --headless=false

# 5. Run in Firefox instead
pytest --browser=firefox
```

An HTML report is generated at `reports/report.html` after every run.
Selenium 4's built-in Selenium Manager handles the driver binary automatically —
no manual chromedriver setup needed.

## CI

Every push to `main` (and every PR) triggers the GitHub Actions workflow, which:
1. Installs dependencies
2. Runs the full suite headless
3. Uploads the HTML report as a build artifact
4. Uploads failure screenshots if any test fails

## Extending this framework

- Add a new page → create a class in `pages/` inheriting `BasePage`
- Add new test data/users → `utils/config.py`
- Add a new test type → add a marker in `pytest.ini` and tag tests with `@pytest.mark.<name>`

## About

Built by [Your Name] as a demonstration of UI automation and UAT-style test
design. Background: Selenium, Pytest, Robot Framework, REST API testing,
Jenkins CI/CD — open to freelance QA automation work.
