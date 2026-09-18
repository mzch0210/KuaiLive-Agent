from __future__ import annotations
import subprocess
import sys
from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
TMP = ROOT / ".smoke"
RAW = TMP / "raw"
PREP = TMP / "prepared"
RES = TMP / "results"


def main():
    import shutil
    shutil.rmtree(TMP, ignore_errors=True)
    RAW.mkdir(parents=True)
    rng = np.random.default_rng(42)
    rooms=[]; clicks=[]; live=1
    base=1_750_000_000_000
    for d in range(8):
        for sid in range(1, 31):
            start=base+d*86_400_000 + (sid%6)*3_600_000
            end=start+8*3_600_000
            rooms.append([20250601+d, live, sid, 1, start, end, "shop" if sid<=25 else "game", live])
            for uid in range(1, 81):
                if (uid+sid+d)%17==0:
                    t=start+int(rng.integers(1_000, max(2_000,end-start-1_000)))
                    clicks.append([uid,live,sid,t,int(rng.integers(5_000,120_000))])
            live+=1
    pd.DataFrame(rooms, columns=["p_date","live_id","streamer_id","live_type","start_timestamp","end_timestamp","live_content_category","live_name_id"]).to_csv(RAW/"room.csv",index=False)
    pd.DataFrame(clicks, columns=["user_id","live_id","streamer_id","timestamp","watch_live_time"]).to_csv(RAW/"click.csv",index=False)
    subprocess.check_call([sys.executable,"-m","kuailive_agent.prepare","--data-dir",str(RAW),"--out-dir",str(PREP),"--scope","shop"], cwd=ROOT)
    subprocess.check_call([sys.executable,"-m","kuailive_agent.evaluate","--prepared-dir",str(PREP),"--out-dir",str(RES),"--n-neg","19","--seed","42"], cwd=ROOT)
    out=pd.read_csv(RES/"summary_seed42.csv")
    assert {"Popularity","LongMemory","MemoryPlanner"}.issubset(set(out.model))
    assert out["ndcg@10"].between(0,1).all()
    print("SMOKE TEST PASSED")

if __name__ == "__main__":
    main()
