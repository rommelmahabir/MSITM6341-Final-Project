"""
services/exchange_signal.py - "is today a good day to buy currency?"
Owner: Rommel

Planned function:
    exchange_signal(base, quote) -> dict
        {"signal": str, "today_rate": float, "avg_30d": float,
         "z_score": float, "reason": str}

Method (proposal Section 05):
    history = last ~45 calendar days (about 30 published rates)
    fewer than 20 data points -> "Not enough data" (route returns 422)
    z = (today_rate - mean_30d) / std_dev_30d      (std_dev 0 -> z = 0)
    z >= 0.5  -> "Favorable"   (more foreign currency per home unit than usual)
    z <= -0.5 -> "Unfavorable"
    otherwise -> "Neutral"
"""
