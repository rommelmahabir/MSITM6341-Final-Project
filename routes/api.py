"""
routes/api.py - JSON API routes (Flask Blueprint)
Owner: Rajendra

Registered in app.py with url_prefix="/api", so "/convert" here
becomes "/api/convert" in the browser.

Planned routes (proposal Section 04):
    GET /api/convert                amount, from, to
    GET /api/rates/history          base, quote, days (7-365)
    GET /api/signal                 base, quote
    GET /api/trips/<id>/summary     trip ID

The /health route below is a quick "is the app alive?" check.
"""

from flask import Blueprint, jsonify

api_bp = Blueprint("api", __name__)


@api_bp.route("/health")
def health():
    """Return a simple JSON status. Visit /api/health to test."""
    return jsonify({"status": "ok"})