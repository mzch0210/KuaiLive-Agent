#!/usr/bin/env python3
"""G5 immutable pretest identity audit: no TEST rows, ranks or outcomes read."""
from __future__ import annotations
import argparse,hashlib,json
from pathlib import Path

SEEDS=(20261012,20261013,20261014)
FAMILIES=("sasrec","gru4rec")
METHODS=("utility","difficulty","specialist","uncertainty","history")

def sha(path):
    h=hashlib.sha256()
    with Path(path).open("rb") as f:
        for chunk in iter(lambda:f.read(8*1024*1024),b""):
            h.update(chunk)
    return h.hexdigest()

def policy_dir(cache,seed,family):
    parent=(cache/"klm3_g3_e2_five_gate_DEV_frozen_v1"
            if seed==20261012
            else cache/f"klm3_g4_extra_seed{seed}_five_gate_DEV_frozen_v1")
    return parent/family

def run(cache,registered,g1,out):
    if out.exists():
        raise FileExistsError("No overwrite of G5 preflight audit")
    reg=json.loads(registered.read_text())
    g1m=json.loads((g1/"manifest.json").read_text())
    index=json.loads((cache/"klm3_g2_train_index_v1/index_manifest.json").read_text())
    if (reg["schema"]!="kbs-plan-c-g5-pretest-frozen-registry-v1" or
        reg["status"]!="SIX_DEV_POLICIES_FROZEN_TEST_UNOPENED"
        or reg["test_performance_seen"] is not False or
        reg["seeds"]!=list(SEEDS) or reg["families"]!=list(FAMILIES) or
        reg["policy_methods"]!=list(METHODS) or
        g1m["protocol_sha256"]!=reg["g1_protocol_sha256"] or
        index["g1_protocol_sha256"]!=reg["g1_protocol_sha256"]):
        raise ValueError("G5 registry, G1 and indexed TRAIN mismatch")
    test_file=g1/"test_cohort_sealed.parquet"
    if (sha(test_file)!=reg["test_cohort_sha256"] or
        g1m["generated_files_sha256"]["test_cohort_sealed.parquet"]!=reg["test_cohort_sha256"]
        or g1m["selected_cohort_counts"]["TEST"]!=reg["target_test_events"]):
        raise ValueError("Frozen TEST byte identity / count mismatch")
    # No TEST data rows or label columns opened. Only hash encrypted/serialized
    # bytes for the precommitted frozen cohort identity.
    evidence={}
    for seed in SEEDS:
        select=(cache/"klm3_g2_checkpoint_dev_selected_v1.json"
                if seed==20261012 else cache/f"klm3_g2_seed{seed}_dev_selected_v1.json")
        doc=json.loads(select.read_text())
        if doc["schema"]!="kbs-plan-c-g2-checkpoint-selection-dev-only-v1" or doc["test_data_opened"]:
            raise ValueError("Checkpoint selected on TEST or invalid DEV provenance")
        for family in FAMILIES:
            chosen=doc["family_results"][family]["selected"]
            train=(cache/f"klm3_g2_seed{seed}_epoch3_v1"/family)
            chk=train/chosen["checkpoint"]
            expected=reg["checkpoint_sha256"][str(seed)][family]
            if chosen["checkpoint_sha256"]!=expected or sha(chk)!=expected:
                raise ValueError(f"Frozen Base checksum mismatch {seed}/{family}")
            d=policy_dir(cache,seed,family)
            policy=d/"frozen_thresholds.json"
            target_sha=reg["policy_frozen_threshold_sha256"][str(seed)][family]
            if sha(policy)!=target_sha:
                raise ValueError(f"Frozen policy SHA mismatch {seed}/{family}")
            p=json.loads(policy.read_text())
            if (p["schema"]!="kbs-plan-c-gates-v1"
                    or p["state"]!="DEV_FROZEN_POINTWISE"
                    or p["test_outcomes_seen"] is not False
                    or list(p["methods"])!=list(METHODS)):
                raise ValueError("Nonfrozen/missing policies")
            models={}
            for method in ("utility","difficulty","specialist"):
                filename=d/"models"/(method+".joblib")
                expect=reg["supervised_gate_model_sha256"][str(seed)][family][method]
                if sha(filename)!=expect:
                    raise ValueError(f"Frozen gate model SHA mismatch {seed}/{family}/{method}")
                models[method]=expect
            evidence[f"{seed}_{family}"]={"base_sha256":expected,
                 "policy_sha256":target_sha,"models_sha256":models,
                 "selected_epoch":chosen["epoch"],
                 "dev_policy_rate":{m:p["methods"][m]["dev_oof_call_rate"]
                                    for m in METHODS}}
    result={"schema":"kbs-plan-c-g5-immutable-preflight-v1",
      "status":"ALL_SIX_CHECKPOINT_AND_POLICY_DIGESTS_VERIFIED",
      "registry_sha256":sha(registered),
      "test_cohort_sha256":reg["test_cohort_sha256"],
      "test_rows_opened":False,"test_labels_read":False,
      "test_rankings_computed":False,"test_retuning_performed":False,
      "g1_protocol_sha256":g1m["protocol_sha256"],
      "n_selected_test":reg["target_test_events"],"evidence":evidence}
    out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text(json.dumps(result,indent=2)+"\n")
    print(json.dumps({"status":result["status"],
      "n_registered_bases":len(evidence),
      "test_rows_opened":False}),flush=True)

if __name__=="__main__":
    p=argparse.ArgumentParser()
    for arg in ("cache","registered","g1","out"):
        p.add_argument("--"+arg,type=Path,required=True)
    a=p.parse_args()
    run(a.cache,a.registered,a.g1,a.out)
