"""
Books aggregator: Sharp + Soft
- Sharp: Pinnacle, Circa via The Odds API (us2 region)
- Soft DFS: PrizePicks scraper, DK Pick6, Betr

PrizePicks: public API used by their web app (see github.com/lazarobeas/prizepicks-prop-scraper)
DK Pick6: peer-to-peer
"""

import os, requests

def fetch_sharp_books(api_key):
    if not api_key:
        return []
    url = "https://api.the-odds-api.com/v4/sports/baseball_mlb/odds"
    params = {
        "apiKey": api_key,
        "regions": "us,us2",
        "markets": "pitcher_strikeouts,pitcher_outs",
        "oddsFormat": "american",
        "bookmakers": "pinnacle,circasports,bookmakers,draftkings,fanduel"
    }
    try:
        r = requests.get(url, params=params, timeout=15)
        r.raise_for_status()
        return r.json()
    except Exception as e:
        print(f"Odds API error {e}")
        return []

def fetch_prizepicks():
    # PrizePicks endpoint - may need to update league_id
    headers = {"User-Agent": "Mozilla/5.0"}
    results = []
    for lid in [2,8]:
        try:
            url = f"https://api.prizepicks.com/projections?per_page=500&league_id={lid}&state_code=CA"
            r = requests.get(url, headers=headers, timeout=10)
            if r.status_code==200:
                j=r.json()
                for item in j.get('data',[]):
                    attr=item.get('attributes',{})
                    if 'strikeout' in str(attr.get('stat_type','')).lower():
                        results.append({
                            "book":"PrizePicks",
                            "player": attr.get('description','')[:100],
                            "line": attr.get('line_score'),
                            "stat": attr.get('stat_type')
                        })
                if results:
                    break
        except: pass
    return results

def fetch_all_books():
    api_key=os.getenv("ODDS_API_KEY")
    sharp=fetch_sharp_books(api_key)
    soft=fetch_prizepicks()
    return {"sharp": sharp, "soft": soft}
