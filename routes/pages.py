"""
routes/pages.py - HTML page routes (Flask Blueprint)
Owner: Rajendra

Planned routes (proposal Section 04):
    GET  /                          trip list
    POST /trips                     create a trip
    GET  /trips/<id>                trip dashboard
    POST /trips/<id>/expenses       add an expense
    POST /expenses/<id>/delete      delete an expense

The placeholder below only proves the app starts. Replace it.
"""

from flask import Blueprint

pages_bp = Blueprint("pages", __name__)


@pages_bp.route("/")
def index():
    """Placeholder home page."""
    return "<h1>Trip Budget &amp; Currency Planner</h1><p>Scaffold is running.</p>"