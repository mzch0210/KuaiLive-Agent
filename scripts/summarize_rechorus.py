from pathlib import Path
import re, pandas as pd
rows=[]
for p in Path('rechorus_runs').rglob('*.log'):
    txt=p.read_text(errors='ignore')
    cfg=p.stem
    model='TiSASRec' if 'TiSASRec' in cfg else 'SASRec'
    lr=re.search(r'lr([0-9.eE+-]+)',cfg); hist=re.search(r'hist(\d+)',cfg)
    best=re.findall(r'Best Iter\(dev\)=\s*(\d+).*?dev=\((.*?)\)',txt)
    dev=re.findall(r'Dev\s+After Training:\s*\((.*?)\)',txt)
    test=re.findall(r'Test After Training:\s*\((.*?)\)',txt)
    def metric(s,name):
        m=re.search(rf'{name}@10=([0-9.]+)',s or '')
        return float(m.group(1)) if m else None
    d=dev[-1] if dev else (best[-1][1] if best else '')
    t=test[-1] if test else ''
    rows.append({'config':cfg,'model':model,'lr':lr.group(1) if lr else None,'history_max':int(hist.group(1)) if hist else None,'best_epoch':int(best[-1][0]) if best else None,'dev_ndcg10':metric(d,'NDCG'),'dev_hr10':metric(d,'HR'),'test_ndcg10':metric(t,'NDCG'),'test_hr10':metric(t,'HR'),'log':str(p)})
out=pd.DataFrame(rows)
if len(out): out=out.sort_values(['model','dev_ndcg10'],ascending=[True,False])
Path('rechorus_summary').mkdir(exist_ok=True); out.to_csv('rechorus_summary/grid_results.csv',index=False)
print(out.to_string(index=False))
