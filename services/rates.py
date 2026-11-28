"""
services/rates.py - Frankfurter exchange-rate client with SQLite cache
Owner: Rommel

API: https://api.frankfurter.dev/v2/rate/{base}/{quote}?date=YYYY-MM-DD
(free, no key; caching encouraged). Every lookup checks rate_cache first,
then calls the API (5 s timeout, 1 retry on network errors), then saves
the result to rate_cache.

Functions other modules can call:
    get_rate(base, quote, on_date)  -> float
        Rate for 1 unit of base in quote on that date (e.g. JPY -> USD).
        Raises RateServiceError if the API fails and nothing is cached.
    last_cached_rate(base, quote)   -> float or None
        Most recent cached rate; the fallback when the API is unreachable.

Planned for the 12/3 MVP:
    get_history(base, quote, days)  -> list of {"date": str, "rate": float}
"""

from datetime import datetime

import requests

from data.db import get_db

API_URL = "https://api.frankfurter.dev/v2/rate"
TIMEOUT_SECONDS = 5


class RateServiceError(Exception):
    """Raised when a rate can't be found: the API failed and nothing is cached."""


def get_rate(base, quote, on_date):
    """Return the rate for 1 unit of base in quote on on_date ("YYYY-MM-DD")."""
    base = base.upper()
    quote = quote.upper()
    on_date = str(on_date)

    if base == quote:
        return 1.0                      # same currency: nothing to convert

    cached = _read_cache(base, quote, on_date)
    if cached is not None:
        return cached                   # cache hit: no API call needed

    rate = _fetch_rate(base, quote, on_date)
    _save_cache(base, quote, on_date, rate)
    return rate


def last_cached_rate(base, quote):
    """Return the most recent cached rate for this pair, or None if there is none."""
    row = get_db().execute(
        "SELECT rate FROM rate_cache WHERE base = ? AND quote = ? "
        "ORDER BY rate_date DESC LIMIT 1",
        (base.upper(), quote.upper()),
    ).fetchone()
    return row["rate"] if row else None


# ---------------------------------------------------------------------------
# Helpers (the leading underscore means "only used inside this file")
# ---------------------------------------------------------------------------

def _fetch_rate(base, quote, on_date):
    """Call Frankfurter. Retries once on a timeout or connection error."""
    url = f"{API_URL}/{base}/{quote}"
    last_error = None

    for attempt in range(2):            # first try + 1 retry
        try:
            response = requests.get(url, params={"date": on_date},
                                    timeout=TIMEOUT_SECONDS)
        except (requests.Timeout, requests.ConnectionError) as error:
            last_error = error
            continue                    # network problem: try once more

        if response.status_code != 200:
            # e.g. 422 for an unknown currency: retrying won't help
            raise RateServiceError(
                f"Rate service returned {response.status_code} for {base} to {quote}"
            )
        return float(response.json()["rate"])

    raise RateServiceError(f"Rate service unreachable: {last_error}")


def _read_cache(base, quote, on_date):
    """Return the cached rate for this pair and date, or None."""
    row = get_db().execute(
        "SELECT rate FROM rate_cache WHERE base = ? AND quote = ? AND rate_date = ?",
        (base, quote, on_date),
    ).fetchone()
    return row["rate"] if row else None


def _save_cache(base, quote, on_date, rate):
    """Save a rate so the next lookup for this pair and date skips the API."""
    db = get_db()
    db.execute(
        "INSERT OR REPLACE INTO rate_cache (base, quote, rate_date, rate, fetched_at) "
        "VALUES (?, ?, ?, ?, ?)",
        (base, quote, on_date, rate, datetime.now().isoformat(timespec="seconds")),
    )
    db.commit()
