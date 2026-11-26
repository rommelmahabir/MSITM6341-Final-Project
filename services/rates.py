"""
services/rates.py - Frankfurter exchange-rate client with SQLite cache
Owner: Rommel

API: https://api.frankfurter.dev/v2/rates (free, no key; caching encouraged)
Every call: check rate_cache first -> else call API (5 s timeout, 1 retry)
-> save to rate_cache. Weekends/holidays use the most recent published rate.

Planned functions (what routes and other services can call):
    get_rate(base, quote, on_date)  -> float
        Rate for 1 base in quote on that date. Raises an error if the API
        is down and nothing is cached.
    last_cached_rate(base, quote)   -> float or None
        Most recent cached rate; the fallback when the API is unreachable.
    get_history(base, quote, days)  -> list of {"date": str, "rate": float}
        Daily rates for the last `days` days (7-365), oldest first.
"""
