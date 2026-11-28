"""
services/budget.py - trip budget summary
Owner: Rommel

Planned functions:
    summarize(trip_id) -> dict or None (None if the trip does not exist)
        {"budget": float, "spent": float, "remaining": float,
         "pct_used": float, "by_category": {category: total, ...}}
        Totals use each expense's stored converted_amount (home currency).
        by_category is built with pandas groupby.

Expense categories (shared with route validation):
    Food, Lodging, Transport, Activities, Other
"""
