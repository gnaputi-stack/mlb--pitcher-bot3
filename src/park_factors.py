"""
PARK FACTORS 2026 - Blended 2024-2026, 1.00 = neutral
Source: Baseball Savant / FantasyPros
"""

PARK_FACTORS = {
    "Coors Field": {"runs": 1.15, "hr": 1.12, "k": 0.92, "team": "COL"},
    "Great American Ball Park": {"runs": 1.08, "hr": 1.22, "k": 0.98, "team": "CIN"},
    "Citizens Bank Park": {"runs": 1.05, "hr": 1.14, "k": 0.99, "team": "PHI"},
    "Oriole Park": {"runs": 1.04, "hr": 1.14, "k": 1.01, "team": "BAL"},
    "Daikin Park": {"runs": 1.04, "hr": 1.15, "k": 0.98, "team": "HOU"},
    "Dodger Stadium": {"runs": 1.03, "hr": 1.08, "k": 1.01, "team": "LAD"},
    "Yankee Stadium": {"runs": 1.03, "hr": 1.18, "k": 0.99, "team": "NYY"},
    "Sutter Health Park": {"runs": 1.12, "hr": 1.18, "k": 0.95, "team": "ATH"}, # A's temp - HUGE edge
    "Kauffman Stadium": {"runs": 1.01, "hr": 0.95, "k": 0.98, "team": "KCR"},
    "Petco Park": {"runs": 0.92, "hr": 1.08, "k": 1.03, "team": "SDP"},
    "T-Mobile Park": {"runs": 0.90, "hr": 0.92, "k": 1.07, "team": "SEA"},
    "LoanDepot Park": {"runs": 0.88, "hr": 0.85, "k": 1.04, "team": "MIA"},
    "Oracle Park": {"runs": 0.89, "hr": 0.86, "k": 1.04, "team": "SFG"},
    "Comerica Park": {"runs": 0.96, "hr": 0.93, "k": 1.02, "team": "DET"},
    "Steinbrenner Field": {"runs": 1.02, "hr": 0.98, "k": 1.0, "team": "TBR"},
    "Chase Field": {"runs": 1.02, "hr": 1.03, "k": 0.98, "team": "ARI"},
    "Fenway Park": {"runs": 1.06, "hr": 0.95, "k": 0.97, "team": "BOS"},
}

def get_factor(park, stat="runs"):
    return PARK_FACTORS.get(park, {}).get(stat, 1.0)
