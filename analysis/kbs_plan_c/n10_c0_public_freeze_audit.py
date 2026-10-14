#!/usr/bin/env python3
"""N10/C0: strictly PUBLIC, read-only frozen evidence guard. Never opens private caches.

Validate Git blob identity of frozen public source records and essential
quantitative/negative results. No labels, target IDs, model fitting or
decision-threshold tuning are performed or supported.
"""
from __future__ import annotations
import argparse, hashlib, json
from pathlib import Path

FROZEN_GIT_BLOBS = {
    "experiments/kbs_plan_c/G5_PRETEST_SIX_BASE_FROZEN_REGISTRY_2026-10-12.json":"f851aee3d364b5531771efbd1bef3cec122afde7",
    "experiments/kbs_plan_c/N9_ROUTE_B_B4A_A0_AGGREGATE_ELIGIBILITY_2026-10-14.json":"b143c744cbdffd2430303e190e982362552cd994",
    "experiments/kbs_plan_c/N9_ROUTE_B_B4A_A1_SEALED_SAMPLE_PUBLIC_2026-10-14.json":"6445cd291c922b96ff91b956b45767c9642755a9",
    "experiments/kbs_plan_c/N9_ROUTE_B_B4A_A2_DEV_FINAL_GATE_AGGREGATE_2026-10-14.json":"aaf1cc310133f1c7ddd5050be4feb27407bc48b3",
    "experiments/kbs_plan_c/N9_ROUTE_B_B4A_A2_MODEL_CONTRACT_PUBLIC_2026-10-14.json":"69b31dec0031f8b7cab69a2cde89ad74af5840ca",
    "experiments/kbs_plan_c/N9_ROUTE_B_B4A_A2_POPULATION_WEIGHTS_2026-10-14.json":"fd8d0f73c8d95e3e6504b40be20a8fa2d26f699f",
    "manuscript/kbs_latex/N9_ROUTE_B_B4A_A4_A5_FROZEN_RESULTS_AND_SCIENTIFIC_LIMITS_2026-10-14.md":"c49591905ba2cb0afa315696ff13c4de6fabb5e9",
    "manuscript/kbs_latex/N9_ROUTE_B_B4A_A6_REFEREE_RISK_ADJUDICATION_2026-10-14.md":"232882adb98710966fff5e8cd7cec75c786e9ad3",
    "manuscript/kbs_latex/N9_ROUTE_B_B4A_A7_POSTINTEGRATION_SUBMISSION_QA_2026-10-14.md":"16b77f1700bff3b0143fe00843f276df9a374b47",
}
A7_PAPER_BLOBS = {
    "manuscript/kbs_latex/main.tex":"6183e76e9985aff9995196187bcaa2e8a156bf98",
    "manuscript/kbs_latex/SUPPLEMENTARY_INFORMATION_S1-S10_2026-10-13.md":"1fecd9d9f6bc76b7322645deac6ca41e8e0ea515"
}
FROZEN_RUNS = {
    "A3_H1_seal":38517170015, "A3_H2_final_lock":38517502835,
    "A3_pre_reveal_audit":38518563975, "A4_one_shot":38518785650,
    "A5_independent_reconstruction":38519174441,
    "A5_safe_aggregate":38519266946, "A7_PDF_QA":38523544564
}
B4A_PRIMARY = {
    "sasrec_F_minus_S": {"diff":0.005391,"CI":[0.003646,0.007174],"Holm_p":0.000600},
    "gru4rec_F_minus_S":{"diff":0.003585,"CI":[0.001599,0.005576],"Holm_p":0.000800},
    "historical_authentic_minus_three_nulls":{"diff":0.031145,"CI":[0.027389,0.035098],"Holm_p":0.000600},
}

def require(test,reason):
    if not test: raise AssertionError("N10 frozen evidence: "+reason)

def git_blob_sha(path):
    blob=path.read_bytes()
    return hashlib.sha1(b"blob "+str(len(blob)).encode()+b"\0"+blob).hexdigest()

def check(root, check_a7_paper=False):
    verified=[]
    for name, expected in {**FROZEN_GIT_BLOBS,**(A7_PAPER_BLOBS if check_a7_paper else {})}.items():
        require(git_blob_sha(root/name)==expected, "changed/missing frozen public blob "+name)
        verified.append(name)
    def readj(name):return json.loads((root/name).read_text(encoding="utf-8"))
    x="experiments/kbs_plan_c/"
    a0=readj(x+"N9_ROUTE_B_B4A_A0_AGGREGATE_ELIGIBILITY_2026-10-14.json")
    a1=readj(x+"N9_ROUTE_B_B4A_A1_SEALED_SAMPLE_PUBLIC_2026-10-14.json")
    a2=readj(x+"N9_ROUTE_B_B4A_A2_DEV_FINAL_GATE_AGGREGATE_2026-10-14.json")
    pop=readj(x+"N9_ROUTE_B_B4A_A2_POPULATION_WEIGHTS_2026-10-14.json")
    g5=readj(x+"G5_PRETEST_SIX_BASE_FROZEN_REGISTRY_2026-10-12.json")
    require(a0["residual_warm_history_eligible_events"]==4723652
            and a0["residual_users"]==21565 and not a0["unseen_future_time_period"],
            "eligible source population or chronology")
    require(g5["target_test_events"]==47575 and not g5["test_performance_seen"],
            "G5 prior freeze was modified (performance_seen in pretest registry)")
    require(a1["main_events"]==30000 and a1["main_users"]==10387
            and a1["mechanism_events"]==4096 and a1["mechanism_users"]==3059
            and a1["old_G5_target_id_overlap"]==0
            and not a1["target_author_in_sampling_hash"]
            and not a1["target_author_labels_in_frozen_files"]
            and a1["no_new_independent_collection_period"],
            "A1 frozen cohort and blind sampling contract")
    require(a1["main_private_SHA256"]=="be96c9dbf13a14e0db85df24202e318b691b41a4250a3f5e9bc877d4e28d1e14"
            and a1["mechanism_private_SHA256"]=="40c950e6a9d79ce3e4330b8b8f434dda764570fd369bdeb83a7b4d587c00d059",
            "A1 private SHA digests published without reading those private records")
    require(a2["n_dev_events"]==50049 and a2["n_dev_users"]==12628
            and not a2["test_labels_or_ranking_metrics_opened"] and a2["group_oof_folds"]==4
            and a2["max_OOF_call_fraction"]==0.3, "A2 frozen DEV model contract")
    require(pop["main"]["N"]==30000 and pop["mechanism"]["N"]==4096
            and abs(pop["main"]["N_effective_kish_for_population_weights"]-26849.293759)<.001
            and abs(pop["mechanism"]["N_effective_kish_for_population_weights"]-3659.420543)<.001,
            "population weighting and Kish ESS")
    report=(root/"manuscript/kbs_latex/N9_ROUTE_B_B4A_A4_A5_FROZEN_RESULTS_AND_SCIENTIFIC_LIMITS_2026-10-14.md").read_text()
    qa=(root/"manuscript/kbs_latex/N9_ROUTE_B_B4A_A7_POSTINTEGRATION_SUBMISSION_QA_2026-10-14.md").read_text()
    for word in ("0.005391","0.003585","0.031145","0.348744",
                 "8,704","9,105","8,629","9,168","1.337","1.797",
                 "NOT VERIFIED","same-period","one-shot"):
        require(word.lower() in (report+qa).lower(),"missing frozen value or unfavorable counterexample "+word)
    for run in FROZEN_RUNS.values():
        require(str(run) in report+qa,"no immutable public run linkage "+str(run))
    # Reporting-tier distinctions apply to current evolving manuscript too.
    manuscript=(root/"manuscript/kbs_latex/main.tex").read_text()
    supplement=(root/"manuscript/kbs_latex/SUPPLEMENTARY_INFORMATION_S1-S10_2026-10-13.md").read_text()
    for k in ("0.005391","0.003585","0.031145","0.348744"):
        require(k in manuscript and k in supplement,"claim values drift across paper/supp "+k)
    require("S10.15" in supplement and "S10.16" in supplement
            and "20-cell" in supplement
            and "Always Memory" in manuscript, "missing supplement/regime/support")
    require("popularity" in supplement.lower() and "NOT VERIFIED" in supplement,
            "missing original popularity control limitation")
    return {"status":"C0_PUBLIC_READ_ONLY_PASS",
            "fixed_source_blobs_verified":len(verified),
            "A7_original_paper_SHA_checked":check_a7_paper,
            "original_A7_main_blob":A7_PAPER_BLOBS["manuscript/kbs_latex/main.tex"],
            "original_A7_supp_blob":A7_PAPER_BLOBS["manuscript/kbs_latex/SUPPLEMENTARY_INFORMATION_S1-S10_2026-10-13.md"],
            "samples":{"old_G5_targets":47575,"B4A_main":30000,"B4A_H2":4096,
                       "original_same_period_not_external":True},
            "primary_frozen_effects":B4A_PRIMARY,"immutable_evidence_runs":FROZEN_RUNS,
            "privacy":{"opened_private_TEST_author_or_event_files":False,
                       "performed_TEST_rank_scoring":False,
                       "new_model_training":False,"reran_A4":False},
            "negative_evidence_preserved":True,"H2_popularity_floor_predeclared_verified":False,
            "strict_equal_budget_F_vs_S":False}

if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("--repo-root",type=Path,default=Path(__file__).resolve().parents[2])
    p.add_argument("--check-a7-paper",action="store_true",
                   help="Only for initial C0 baseline; future revisions may change manuscript")
    a=p.parse_args()
    print(json.dumps(check(a.repo_root,a.check_a7_paper),sort_keys=True,indent=2))
