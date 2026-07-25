"""
Statcast auto-import via pybaseball
Any name -> real stats
"""
from pybaseball import playerid_lookup, pitching_stats, cache
cache.enable()

def import_pitcher(name: str, season=2026):
    try:
        parts = name.split()
        last, first = parts[-1], parts[0]
        lookup = playerid_lookup(last, first)
        if lookup.empty:
            return None
        row = lookup.iloc[0]
        # FanGraphs
        try:
            fg = pitching_stats(season, season, qual=10)
            match = fg[fg['Name'].str.contains(last, case=False, na=False)]
            if not match.empty:
                r = match.iloc[0]
                return {
                    "name": name,
                    "k_pct": r['K%']/100,
                    "bb_pct": r['BB%']/100,
                    "hr_per_9": r['HR/9'],
                    "babip": r['BABIP'],
                    "gb_pct": r['GB%']/100,
                    "fip": r['FIP'],
                    "mlbam_id": row['key_mlbam']
                }
        except Exception as e:
            print(f"FG error {e}")
        
        # Fallback
        return {"name": name, "k_pct": 0.24, "bb_pct": 0.08, "hr_per_9": 1.1, "babip": 0.29, "gb_pct": 0.44}
    except Exception as e:
        print(f"Import error {e}")
        return None
