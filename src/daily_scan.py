"""
Main daily scan - runs on GitHub Actions
"""
import argparse, os, json, random, pandas as pd, numpy as np
from datetime import datetime
from park_factors import get_factor, PARK_FACTORS
from statcast_import import import_pitcher
from books import fetch_all_books

def simulate_pitcher(p, park="Dodger Stadium", opp_k=0.23, n=10000):
    results=[]
    for _ in range(n):
        outs=k=0
        pitches=0
        while pitches<95 and outs<27:
            pf_hr=get_factor(park,"hr")
            pf_k=get_factor(park,"k")
            adj_k=p['k_pct']*pf_k*(opp_k/0.23)
            adj_hr=(p['hr_per_9']/9/3.3)*pf_hr
            r=random.random()
            if r<adj_k:
                k+=1; outs+=1; pitches+=np.random.randint(3,7)
            elif r<adj_k+p['bb_pct']:
                pitches+=5
            elif r<adj_k+p['bb_pct']+adj_hr:
                pitches+=2
            else:
                if random.random()<p['babip']:
                    pitches+=2
                else:
                    outs+=1; pitches+=3
        results.append({"K":k,"IP":outs/3})
    return pd.DataFrame(results)

def calc_ev(df, line, col="K"):
    over=(df[col]>line).mean()
    ev=over*0.909-(1-over)
    return over, ev, df[col].mean()

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--today", action="store_true")
    parser.add_argument("--pitcher", type=str, default="Paul Skenes")
    parser.add_argument("--park", type=str, default="Dodger Stadium")
    parser.add_argument("--line", type=float, default=7.5)
    parser.add_argument("--n-sims", type=int, default=10000)
    parser.add_argument("--ev-threshold", type=float, default=0.05)
    args=parser.parse_args()

    os.makedirs("results", exist_ok=True)

    if args.today:
        print(f"=== Daily Scan {datetime.now()} ===")
        books=fetch_all_books()
        print(f"Sharp games: {len(books['sharp'])} | PrizePicks props: {len(books['soft'])}")
        
        # Example: scan today's probable starters (you would pull from MLB StatsAPI)
        # For demo, scan 5 aces
        test_pitchers=["Paul Skenes","Tarik Skubal","Zack Wheeler","Corbin Burnes","Logan Gilbert"]
        edges=[]
        for name in test_pitchers:
            prof=import_pitcher(name)
            if not prof: continue
            df=simulate_pitcher(prof, park=args.park, n=args.n_sims)
            over, ev, mean=calc_ev(df, args.line)
            print(f"{name}: mean K {mean:.1f} | Over {args.line} {over:.1%} | EV {ev:.1%}")
            if abs(ev)>=args.ev_threshold:
                edges.append({"pitcher":name,"line":args.line,"over%":over,"ev":ev,"mean":mean})

        # Save report
        with open("results/report.md","w") as f:
            f.write(f"# Daily MLB Edges {datetime.now().date()}\n\n")
            for e in edges:
                f.write(f"- **{e['pitcher']}** K>{e['line']}: {e['over%']:.1%} | EV {e['ev']:.1%} | mean {e['mean']:.1f}\n")
            if not edges:
                f.write("No edges > threshold today.\n")
        
        with open("results/edges.json","w") as f:
            json.dump(edges,f,indent=2)

        # Discord alert
        webhook=os.getenv("DISCORD_WEBHOOK")
        if webhook and edges:
            msg="**MLB Pitcher EV Edges**\n" + "\n".join([f"{e['pitcher']} K>{e['line']} EV {e['ev']:.1%}" for e in edges])
            try:
                import requests
                requests.post(webhook, json={"content":msg})
            except: pass

    else:
        prof=import_pitcher(args.pitcher)
        print(prof)
        df=simulate_pitcher(prof, park=args.park, n=args.n_sims)
        print(df.describe())
        over,ev,mean=calc_ev(df, args.line)
        print(f"Over {args.line}: {over:.1%} EV {ev:.1%}")

if __name__=="__main__":
    main()
