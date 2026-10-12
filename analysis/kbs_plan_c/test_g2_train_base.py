"""G2 synthetic TRAIN-only index/model smoke on a tiny fabricated dataset.

No actual M3 or TEST data are opened.
"""
import json
import tempfile
import unittest
from argparse import Namespace
from pathlib import Path

import numpy as np
import pyarrow as pa
import pyarrow.parquet as pq
import torch

from g2_train_base import Encoder, digest, draw_contexts, load_or_prepare_train_index, sample_negatives, train


def write_table(path, data):
    pq.write_table(pa.table(data), path)


class G2UnitTest(unittest.TestCase):
    def test_sasrec_short_history_causal_mask_no_nans(self):
        model=Encoder(50,"sasrec")
        model.train()
        histories=torch.tensor([[0]*14+[2,3],
                                [0]*13+[3,4,5],
                                [0]*15+[7],
                                list(range(1,17))],dtype=torch.long)
        targets=torch.tensor([[4,6,8],[6,8,10],[9,11,13],[17,19,21]],
                             dtype=torch.long)
        optimizer=torch.optim.AdamW(model.parameters(),lr=1e-3)
        for _ in range(3):
            scores=model.score(histories,targets)
            self.assertTrue(torch.isfinite(scores).all())
            loss=torch.nn.functional.cross_entropy(scores,torch.zeros(4,dtype=torch.long))
            self.assertTrue(torch.isfinite(loss))
            optimizer.zero_grad()
            loss.backward()
            for name,param in model.named_parameters():
                if param.grad is not None:
                    self.assertTrue(torch.isfinite(param.grad).all(),name)
            optimizer.step()

    def test_train_index_and_both_model_updates(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            g1 = root / "g1"
            g1.mkdir()
            known = g1 / "train_known_authors.parquet"
            events = g1 / "train_author_events.parquet"
            write_table(known, {"author_id": [11, 12, 13, 14]})
            users = np.repeat(np.arange(1, 5), 15)
            authors = np.array([11 + (i % 4) for i in range(60)])
            write_table(events, {"user_id": users, "author_id": authors})
            manifest = {"schema": "kbs-plan-c-g1-derived-v1",
                        "protocol_sha256": "e"*64,
                        "test_outcomes_inspected": False,
                        "generated_files_sha256": {
                            "train_known_authors.parquet": digest(known),
                            "train_author_events.parquet": digest(events)}}
            (g1/"manifest.json").write_text(json.dumps(manifest))
            cache = root / "train-index"
            index = load_or_prepare_train_index(g1, cache, synthetic=True)
            self.assertTrue(index["training_only"])
            self.assertFalse(index["test_files_opened"])
            self.assertEqual(index["unique_train_authors"],4)
            idx = np.load(cache/"sequence_ids.npy")
            off = np.load(cache/"user_offsets.npy")
            rng = np.random.default_rng(2)
            contexts,positives = draw_contexts(idx,off,rng,8)
            self.assertEqual(contexts.shape,(8,16))
            self.assertTrue(np.all(contexts[:,-1] != 0))
            negatives=sample_negatives(np.load(cache/"popularity_cdf.npy"),
                                       rng,positives,contexts,8)
            self.assertEqual(negatives.shape,(8,8))
            for family in ("sasrec","gru4rec"):
                enc = Encoder(4,family)
                scores = enc.score(torch.as_tensor(contexts,dtype=torch.long),
                                   torch.as_tensor(np.column_stack(
                                       (positives,negatives)),dtype=torch.long))
                self.assertEqual(tuple(scores.shape),(8,9))
                self.assertTrue(torch.isfinite(scores).all())
                args = Namespace(g1=g1,index=cache,out=root/family,
                      mode="smoke",model=family,seed=11,batch=8,
                      negatives=8,steps_per_epoch=1,epochs=1,
                      learning_rate=.001,log_interval=1,
                      synthetic=True,cpu=True)
                report=train(args)
                self.assertFalse(report["test_outcomes_read"])
                self.assertEqual(len(report["train_records"]),1)
                self.assertTrue((args.out/f"{family}_smoke_report.json").exists())


if __name__ == "__main__":
    unittest.main()
