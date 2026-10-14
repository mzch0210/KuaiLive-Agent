#!/usr/bin/env python3
"""N10 C3-A public-only predeclared null validity audit, NEVER reopen A4 labels.

The DEV 1024 original-polarity popularity floor is verifiable; the B4-A
4096 same-cohort TRAIN-only popularity floor is not pre-reveal verified.
"""
from __future__ import annotations
import hashlib,json,argparse
from pathlib import Path
PUBLIC={
 "structure":("experiments/kbs_plan_c/N9_ROUTE_B_B2_1024_CLOSED_HOUR_STRUCTURAL_PUBLIC_2026-10-14.json","4fbb2b9c62331b51b44cdcc378485e881a6a9a9f"),
 "same_scorer":("experiments/kbs_plan_c/N9_ROUTE_B_B2_1024_THREE_SEED_SAME_SCORER_VERIFIED_2026-10-14.json","d8cdad1eb0ea66c80581b261bc51f7648cbac08b"),
 "a4":("manuscript/kbs_latex/N9_ROUTE_B_B4A_A4_A5_FROZEN_RESULTS_AND_SCIENTIFIC_LIMITS_2026-10-14.md","c49591905ba2cb0afa315696ff13c4de6fabb5e9"),
 "a7qa":("manuscript/kbs_latex/N9_ROUTE_B_B4A_A7_POSTINTEGRATION_SUBMISSION_QA_2026-10-14.md","16b77f1700bff3b0143fe00843f276df9a374b47")
}
SEEDS=[20261014,20261015,20261016]
def verified(root,name):
    path,sha=PUBLIC[name];b=(root/path).read_bytes()
    got=hashlib.sha1(b"blob "+str(len(b)).encode()+b"\0"+b).hexdigest()
    if got!=sha:raise AssertionError("frozen evidence changed: "+name)
    return json.loads(b) if name in ("structure","same_scorer") else b.decode()
def check(root):
    x=verified(root,"structure");y=verified(root,"same_scorer")
    z=verified(root,"a4");qa=verified(root,"a7qa")
    assert x["n_target_events"]==y["n_events"]==1024
    assert x["n_target_users"]==y["n_users"]==992
    assert x["source_hour_activated_after_close_only"] and x["per_user_causal_order_monotone"]
    assert x["no_G5_TEST_read"] and y["G5_TEST_opened"] is False
    assert x["source_sample_SHA256"]==y["frozen_DEV_sample_SHA256"]
    assert x["seed_results"] and len(x["seed_results"])==len(y["seeds"])==3
    assert y["same_scorer_empty_null_original_Full_Long_F_S_parity"]
    assert y["same_scorer_unaltered_max_absolute_NDCG_error"]<1e-12
    structural={t["seed"]:t for t in x["seed_results"]}
    seed_out=[]
    for s in y["seeds"]:
        v=structural[s["seed"]]
        assert s["seed"] in SEEDS and v["private_changed_map_sha256"]==s["private_map_SHA256"]
        assert v["author_hour_marginals_exact"] and v["both_authors_active_at_source_clock"]
        assert v["changed_fraction_of_selected_user_history"]>.75
        assert s["nonfloor_preset_diagnostic_pass"]
        assert s["null_Full_F_NDCG"]>.1
        assert s["null_Full_F_NDCG"]>s["popularity_only_F_NDCG"]
        assert s["null_Full_F_top10_positive_events"]>100
        assert s["original_Full_F_NDCG"]>s["null_Full_F_NDCG"]
        assert abs(s["structural_change_fraction"]-v["changed_fraction_of_selected_user_history"])<1e-14
        seed_out.append({"seed":s["seed"],
            "preserved":{"within_user_timestamps":True,"author_hour_marginals":True,
              "both_original_author_availability":True,"closed_hour_activation":True,
              "current_candidate_F_fixed":True,"original_scorer_exact_parity":True},
            "not_preserved":{"viewer_creator_pair_repeats":True,"higher_order_neighborhoods":True},
            "rewire_frac":v["changed_fraction_of_selected_user_history"],
            "original_NDCG_F":s["original_Full_F_NDCG"],
            "null_NDCG_F":s["null_Full_F_NDCG"],
            "popularity_train_only_NDCG_F":s["popularity_only_F_NDCG"],
            "null_above_popularity_predeclared_checked":True,
            "null_top10_positives":s["null_Full_F_top10_positive_events"]})
    assert "0.334942" in z and "0.303905" in z and "0.304689" in z and "0.302796" in z
    assert "0.031145" in z and ">1,900" in qa and "NOT VERIFIED" in z
    assert "76.78" in z and "TRAIN-popularity" in z
    return {"schema":"n10-c3a-public-null-controls-v1","status":"PASS_C3A_PUBLIC_READ_ONLY",
      "B2_DEV":{"n":1024,"users":992,"null_seeds":seed_out,
            "popularity_floor_from_exact_same_DEV_cohort":True,
            "result_scope":"POST_G5_DEV_EXPLORATORY"},
      "B4A_H2":{"n":4096,"users":3059,"original_weighted_F_NDCG":.334942,
        "three_null_weighted_F_NDCG":[.303905,.304689,.302796],
        "mean_null_weighted_F_NDCG":.303797,
        "primary_paired_real_minus_null":.031145,
        "realized_source_change_fraction":"76.78–76.80 percent",
        "nonfloor_absolute_ndcg_and_positive_top10":"PASS_PUBLIC_A5",
        "same_cohort_train_popularity_margin_prelabel_sealed":False,
        "predeclared_complete_nonfloor_family_verified":False,
        "outcomes_revealed_once":True,
        "three_seeds_independent_cohorts":False,
        "historical_author_permutation_alters_pair_repetition_and_higher_order_structure":True,
        "future_period_independent_TEST":False},
      "new_A4_author_or_event_labels_read":False,
      "new_TEST_metric_calculated":False,
      "new_hypothesis_test":False}
if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("--repo-root",type=Path,default=Path(__file__).resolve().parents[2])
    print(json.dumps(check(p.parse_args().repo_root),indent=2,ensure_ascii=False,sort_keys=True))
