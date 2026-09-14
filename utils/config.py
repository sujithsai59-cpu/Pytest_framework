"""
Central config for the framework.

Keeping URLs, credentials, and browser settings here (instead of scattered
across test files) means switching environments or browsers is a one-line
change, not a find-and-replace across the suite.
"""

import os

BASE_URL = "https://www.saucedemo.com/"

# SauceDemo publishes these as standard demo accounts.
USERS = {
    "standard": {"username": "standard_user", "password": "secret_sauce"},
    "locked_out": {"username": "locked_out_user", "password": "secret_sauce"},
    "problem": {"username": "problem_user", "password": "secret_sauce"},
    "performance_glitch": {"username": "performance_glitch_user", "password": "secret_sauce"},
}

# Allow overriding via env var so CI can run headless while local runs can watch the browser.
HEADLESS = os.getenv("HEADLESS", "true").lower() == "true"
BROWSER = os.getenv("BROWSER", "chrome").lower()
IMPLICIT_WAIT = 0  # we use explicit waits throughout; keep this at 0 to avoid mixed-wait bugs
