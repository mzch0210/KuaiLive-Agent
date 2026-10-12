#!/usr/bin/env python3
"""G0-D privacy-safe schema/type probe. Emits no raw identities."""
from __future__ import annotations
import csv,json,re
from pathlib import Path
import pyarrow.parquet as pq

R=Path.home()/'.cache/kuailive-agent-kbs/klm3'
ICOLS=['user_id','author_id','live_id','live_play_start_timestamp','live_play_end_timestamp']
RCOLS=['live_id','author_id','start_timestamp','end_timestamp']

def category(value):
    if value is None:
        return 'null'
    s=str(value).strip()
    if not s:
        return 'empty'
    if re.fullmatch(r'[+-]?\d+',s):
        return 'integer_string'
    if re.fullmatch(r'[+-]?\d+\.0+',s):
        return 'float_integer_string'
    if re.fullmatch(r'\d{4}-\d{2}-\d{2}.*',s):
        return 'iso_date_string'
    if re.fullmatch(r'[+-]?(?:\d+\.)?\d+(?:[Ee][+-]?\d+)',s):
        return 'scientific_numeric_string'
    return 'other_string'
def audit_column(values):
    samples=[v for v in values if v is not None and str(v).strip()]
    s=samples[0] if samples else None
    result={'observed_type':type(s).__name__ if s is not None else 'none',
            'example_kind':category(s),
            'kind_counts_sample':{k:sum(category(v)==k for v in values)
                                  for k in sorted(set(category(v) for v in values))},
            'example_char_length':len(str(s)) if s is not None else 0}
    if s is not None and (category(s)=='iso_date_string' or
                          (isinstance(s,(int,float)) and 'timestamp' in '')):
        result['example_time_format_hint']=str(s)[:10]
    return result
with (R/'live_interaction.csv').open(newline='',encoding='utf-8-sig') as f:
    reader=csv.DictReader(f)
    rows=[next(reader) for _ in range(100)]
interaction={k:audit_column([r[k] for r in rows]) for k in ICOLS}
pf=pq.ParquetFile(R/'live_room_meta.parquet')
batch=next(pf.iter_batches(columns=RCOLS,batch_size=100))
arr=batch.to_pydict()
room={k:{**audit_column(arr[k]),'arrow_type':str(pf.schema_arrow.field(k).type)} for k in RCOLS}
result={'schema':'KBS_PLAN_C_G0D_TYPES_V1','interaction':interaction,'room':room,
        'n_rows_sampled_each':100,'raw_identifiers_exported':False,
        'test_metrics_computed':False}
Path('g0d_types.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result))
