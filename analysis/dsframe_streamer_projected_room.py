from __future__ import annotations

import argparse, ast, json, math, sys
from pathlib import Path
from types import SimpleNamespace

import numpy as np
import pandas as pd
import torch
import torch.nn.functional as F

SEED = 20260918
BUDGETS = [0.05, 0.10, 0.15, 0.20, 0.30]
EPS = 1e-12


class Selector(torch.nn.Module):
    def __init__(self, d: int):
        super().__init__()
        self.net = torch.nn.Sequential(
            torch.nn.Linear(d, 32), torch.nn.ReLU(), torch.nn.Linear(32, 1)
        )

    def forward(self, x):
        return self.net(x).squeeze(-1)


def fit_selector(X, label, budget, seed):
    torch.manual_seed(seed)
    X = np.asarray(X, np.float32)
    mu = X.mean(0)
    sd = X.std(0)
    sd[sd < 1e-6] = 1
    xt = torch.from_numpy((X - mu) / sd)
    yt = torch.from_numpy(np.asarray(label, np.float32))
    model = Selector(X.shape[1])
    opt = torch.optim.Adam(model.parameters(), lr=1e-3)
    for _ in range(400):
        opt.zero_grad()
        logit = model(xt)
        prob = torch.sigmoid(logit)
        loss = F.binary_cross_entropy_with_logits(logit, yt) + 0.01 * torch.abs(prob.mean() - budget)
        loss.backward()
        opt.step()
    return model, mu, sd


def predict_selector(model, mu, sd, X):
    X = np.asarray(X, np.float32)
    with torch.no_grad():
        return torch.sigmoid(model(torch.from_numpy(((X - mu) / sd).astype(np.float32)))).numpy()


def parse_list(x):
    if isinstance(x, (list, tuple, np.ndarray)):
        return np.asarray(x, dtype=np.int64)
    return np.asarray(ast.literal_eval(str(x)), dtype=np.int64)


def ndcg10(scores: np.ndarray) -> np.ndarray:
    # Match the frozen Dual-ID room evaluation tie convention: all candidates
    # with score >= the positive score contribute to the positive rank.
    tgt = scores[:, 0:1]
    rank = np.sum(scores >= tgt - 1e-12, axis=1)
    out = np.zeros(len(scores), dtype=np.float64)
    m = rank <= 10
    out[m] = 1.0 / np.log2(rank[m].astype(float) + 1.0)
    return out


def candidate_ce(scores: np.ndarray) -> np.ndarray:
    # Positive is candidate 0. Stable log-sum-exp implementation.
    z = scores - scores.max(axis=1, keepdims=True)
    return -z[:, 0] + np.log(np.exp(z).sum(axis=1))


def bootstrap(diff, n=2000, seed=SEED):
    x = np.asarray(diff, float)
    rng = np.random.default_rng(seed)
    vals = np.empty(n, float)
    N = len(x)
    for i in range(n):
        vals[i] = x[rng.integers(0, N, N)].mean()
    return float(x.mean()), float(np.quantile(vals, 0.025)), float(np.quantile(vals, 0.975))


def encode(model, item_seq_ids, item_seq_len):
    # PRL forward without materializing full-item logits. This is algebraically
    # identical to the representation path used by the official forward(stage='infer').
    from utils.constants import MAX_ITEM_SEQ_LEN
    padding_mask = item_seq_ids != (model.item_num - 1)
    valid_pos_ids = torch.cumsum(padding_mask.long(), dim=1) - 1
    pos_ids = torch.where(padding_mask, valid_pos_ids, MAX_ITEM_SEQ_LEN)
    input_embs = model.item_emb(item_seq_ids) + model.pos_emb(pos_ids)
    return model.model(input_embs, item_seq_len, noise_factor=0.0)


def phase_vectors(model, corpus, key, room_file: Path, room_map: pd.DataFrame,
                  ds_inverse: np.ndarray, batch_size: int):
    from utils.constants import ITEM_SEQ, ITEM_SEQ_LEN, ITEM_ID

    rdf = pd.read_csv(room_file, sep='\t').sort_values('user_id').reset_index(drop=True)
    if not np.array_equal(rdf.user_id.to_numpy(dtype=int), np.arange(1, len(rdf) + 1)):
        raise ValueError(f'{key}: expected frozen room user ids 1..N')

    r2s = dict(zip(room_map.item_id.astype(int), room_map.streamer_id.astype(int)))
    s2d = {int(s): int(i) for i, s in enumerate(ds_inverse)}
    candidates = []
    target_streamers = []
    for r in rdf.itertuples(index=False):
        rooms = np.concatenate(([int(r.item_id)], parse_list(r.neg_items)))
        streamers = np.asarray([r2s[int(x)] for x in rooms], dtype=np.int64)
        try:
            candidates.append(np.asarray([s2d[int(x)] for x in streamers], dtype=np.int64))
        except KeyError as e:
            raise KeyError(f'{key}: room candidate streamer absent from frozen DS universe: {e}')
        target_streamers.append(int(streamers[0]))
    C = np.stack(candidates)

    data = corpus.data_dict[key]
    labels = np.asarray(data[ITEM_ID], dtype=np.int64)
    if len(C) != len(labels):
        raise ValueError((key, len(C), len(labels)))
    # Strong alignment check between the independently exported room task and
    # the frozen streamer DS task.
    old_targets = ds_inverse[labels]
    if not np.array_equal(old_targets.astype(np.int64), np.asarray(target_streamers, np.int64)):
        bad = np.flatnonzero(old_targets.astype(np.int64) != np.asarray(target_streamers, np.int64))[:10]
        raise ValueError(f'{key}: target streamer alignment mismatch at rows {bad.tolist()}')

    W = model.item_emb.weight.detach()
    fast_hidden = []
    fast_scores = []
    mean_scores = []
    final_scores = []
    for st in range(0, len(C), batch_size):
        en = min(len(C), st + batch_size)
        seq = data[ITEM_SEQ][st:en]
        slen = data[ITEM_SEQ_LEN][st:en]
        with torch.no_grad():
            mo = encode(model, seq, slen)
            fast = mo[:, 0, :]
            mean = mo.mean(1)
            final = mo[:, -1, :]
            cc = torch.from_numpy(C[st:en])
            emb = W[cc]
            sf = torch.einsum('bd,bkd->bk', fast, emb) / model.temperature
            sm = torch.einsum('bd,bkd->bk', mean, emb) / model.temperature
            sl = torch.einsum('bd,bkd->bk', final, emb) / model.temperature
        fast_hidden.append(fast.cpu().numpy())
        fast_scores.append(sf.cpu().numpy())
        mean_scores.append(sm.cpu().numpy())
        final_scores.append(sl.cpu().numpy())

    return {
        'hidden': np.concatenate(fast_hidden).astype(np.float32),
        'fast_scores': np.concatenate(fast_scores).astype(np.float32),
        'mean_scores': np.concatenate(mean_scores).astype(np.float32),
        'final_scores': np.concatenate(final_scores).astype(np.float32),
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--ds-source', type=Path, required=True)
    ap.add_argument('--ds-data-root', type=Path, required=True)
    ap.add_argument('--ds-dataset', default='KuaiLiveDSFull')
    ap.add_argument('--model-path', type=Path, required=True)
    ap.add_argument('--room-data-dir', type=Path, required=True)
    ap.add_argument('--ours-test', type=Path, required=True)
    ap.add_argument('--out-dir', type=Path, required=True)
    ap.add_argument('--batch-size', type=int, default=128)
    a = ap.parse_args()
    a.out_dir.mkdir(parents=True, exist_ok=True)

    sys.path.insert(0, str(a.ds_source.resolve()))
    from helpers.BaseReader import BaseReader
    from models.PRL import PRL

    args = SimpleNamespace(
        sep=',', path=str(a.ds_data_root.resolve()), dataset=a.ds_dataset,
        device=torch.device('cpu'), model_path=str(a.model_path.resolve()), buffer=0,
        dropout=.2, test_all=1, emb_size=64, num_layers=1, num_heads=4,
        inner_size=128, hidden_act='gelu', layer_norm_eps=1e-12,
        initializer_range=.02, temperature=.07, reason_step=2, pl_weight=1.0,
        temp_scale=5.0, noise_factor=.01, cl_weight=1.0, warmup=2,
    )
    corpus = BaseReader(args)
    model = PRL(args, corpus).to(args.device)
    model.load_state_dict(torch.load(a.model_path, map_location='cpu'))
    model.eval()

    cand = np.load(a.ds_data_root / a.ds_dataset / 'eval_candidates.npz', allow_pickle=False)
    ds_inverse = cand['item_inverse'].astype(np.int64)
    room_map = pd.read_csv(a.room_data_dir / 'room_item_map.tsv', sep='\t')

    dev = phase_vectors(model, corpus, 'valid', a.room_data_dir / 'dev.csv', room_map, ds_inverse, a.batch_size)
    test = phase_vectors(model, corpus, 'test', a.room_data_dir / 'test.csv', room_map, ds_inverse, a.batch_size)

    dev_metrics = {
        'mean': float(ndcg10(dev['mean_scores']).mean()),
        'final': float(ndcg10(dev['final_scores']).mean()),
    }
    slow_variant = max(dev_metrics, key=dev_metrics.get)
    ds_dev_fast = ndcg10(dev['fast_scores'])
    ds_test_fast = ndcg10(test['fast_scores'])
    ds_dev_slow = ndcg10(dev[f'{slow_variant}_scores'])
    ds_test_slow = ndcg10(test[f'{slow_variant}_scores'])
    ds_dev_fast_ce = candidate_ce(dev['fast_scores'])
    ds_dev_slow_ce = candidate_ce(dev[f'{slow_variant}_scores'])
    oracle_label = (ds_dev_slow_ce < ds_dev_fast_ce).astype(np.float32)

    ours = pd.read_csv(a.ours_test).sort_values('user_id').reset_index(drop=True)
    if len(ours) != len(ds_test_fast):
        raise ValueError(('ours/ds row mismatch', len(ours), len(ds_test_fast)))
    required = {'dual_score10', 'MemoryFusion_score10', 'primary_pred_delta'}
    if not required.issubset(ours.columns):
        raise ValueError(f'ours table missing {sorted(required-set(ours.columns))}')
    base = ours.dual_score10.to_numpy(float)
    mem = ours.MemoryFusion_score10.to_numpy(float)
    ours_gate = ours.primary_pred_delta.to_numpy(float)

    rows = []
    for j, b in enumerate(BUDGETS):
        k = max(1, int(round(b * len(ours))))
        om = np.zeros(len(ours), bool)
        om[np.argsort(-ours_gate, kind='mergesort')[:k]] = True
        ours_sel = np.where(om, mem, base)

        selector, mu, sd = fit_selector(dev['hidden'], oracle_label, b, SEED + j)
        ptest = predict_selector(selector, mu, sd, test['hidden'])
        dm = np.zeros(len(ptest), bool)
        dm[np.argsort(-ptest, kind='mergesort')[:k]] = True
        ds_sel = np.where(dm, ds_test_slow, ds_test_fast)

        d_ds, lo_ds, hi_ds = bootstrap(ds_sel - ds_test_fast, seed=SEED + 10 + j)
        d_o, lo_o, hi_o = bootstrap(ours_sel - base, seed=SEED + 20 + j)
        d_cross, lo_c, hi_c = bootstrap(ours_sel - ds_sel, seed=SEED + 30 + j)
        rows.append({
            'target_budget': b, 'k': k, 'realized_rate': k / len(ours),
            'ds_fast_test_ndcg10': float(ds_test_fast.mean()),
            'ds_slow_test_ndcg10': float(ds_test_slow.mean()),
            'ds_selective_test_ndcg10': float(ds_sel.mean()),
            'ds_delta_vs_fast': d_ds, 'ds_delta_ci95': [lo_ds, hi_ds],
            'dual_id_test_ndcg10': float(base.mean()),
            'memory_test_ndcg10': float(mem.mean()),
            'ours_selective_test_ndcg10': float(ours_sel.mean()),
            'ours_delta_vs_dual': d_o, 'ours_delta_ci95': [lo_o, hi_o],
            'ours_minus_ds_selective': d_cross, 'cross_ci95': [lo_c, hi_c],
        })

    report = {
        'experiment': 'DS-Frame streamer-projected live-room collision defense',
        'task': 'next_live_room with frozen 574 active-room negatives',
        'adapter': 'official frozen streamer-level PRL backbone; each room receives its streamer fast/slow score; no room-ID PRL retraining',
        'why_adapter': 'official PRL room-ID full-softmax requires ~1.18M item vocabulary and was not tractable on hosted CPU runner; projection preserves the already validated official DS backbone and tests generic slow/fast reasoning over the same persistent streamer identity',
        'selector': 'paper-faithful 32-hidden MLP on fast hidden; dev oracle is projected-room candidate CE(slow)<CE(fast); exact-K routing on test; no test labels used',
        'slow_variant_selected_on_room_dev': slow_variant,
        'dev_slow_ndcg10_variants': dev_metrics,
        'ds_fast_test_ndcg10': float(ds_test_fast.mean()),
        'ds_slow_test_ndcg10': float(ds_test_slow.mean()),
        'results': rows,
    }
    pd.DataFrame(rows).to_csv(a.out_dir / 'matched_budget.csv', index=False)
    (a.out_dir / 'report.json').write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()
