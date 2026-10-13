"""
Aegis AI - Generate Self-Healing Sanitization Summary Table & Analysis
Reads experiments/sanitization_results.json and aggregates metrics:
- Sanitization Success Rate (SSR)
- Re-check Passed Rate
- Fail-Safe Blocked Rate
- Intent Preservation Score (IPS)
"""

import sys
import os
import json
from collections import defaultdict
from typing import Dict, List, Any

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

RESULTS_PATH = os.path.join(os.path.dirname(__file__), "sanitization_results.json")

def generate_summary():
    if not os.path.exists(RESULTS_PATH):
        print(f"Error: {RESULTS_PATH} does not exist. Run run_sanitization_experiment.py first.")
        return

    with open(RESULTS_PATH, "r", encoding="utf-8") as f:
        records: List[Dict[str, Any]] = json.load(f)

    cat_groups = defaultdict(list)
    for r in records:
        cat_groups[r["category"]].append(r)

    print("\n" + "=" * 95)
    print("📊 TABLE: SELF-HEALING PROMPT SANITIZATION, RE-CHECK VERIFICATION & INTENT PRESERVATION")
    print("=" * 95)
    header = f"{'Category':<26} | {'Attempts':<8} | {'Sanitized':<9} | {'SSR (%)':<8} | {'Re-check Passed':<16} | {'Fail-Safe Block':<15} | {'IPS (%)':<8}"
    print(header)
    print("-" * 95)

    tot_att = 0
    tot_san = 0
    tot_pass = 0
    tot_blk = 0
    tot_ips = 0

    table_data = []

    categories = ["Prompt Injection", "Jailbreak", "System Prompt Extraction", "Role Manipulation", "Safety Bypass"]

    for cat in categories:
        recs = cat_groups[cat]
        n_att = len(recs)
        n_san = sum(1 for r in recs if r["sanitized"])
        n_pass = sum(1 for r in recs if r["recheck_decision"] == "ALLOW")
        n_blk = sum(1 for r in recs if r["fail_safe"])
        n_ips = sum(1 for r in recs if r["intent_preserved"])

        ssr = (n_san / n_att * 100.0) if n_att > 0 else 0.0
        pass_pct = (n_pass / n_att * 100.0) if n_att > 0 else 0.0
        blk_pct = (n_blk / n_att * 100.0) if n_att > 0 else 0.0
        ips = (n_ips / n_san * 100.0) if n_san > 0 else 0.0

        tot_att += n_att
        tot_san += n_san
        tot_pass += n_pass
        tot_blk += n_blk
        tot_ips += n_ips

        row_str = f"{cat:<26} | {n_att:<8} | {n_san:<9} | {ssr:<7.1f}% | {f'{n_pass} ({pass_pct:.1f}%)':<16} | {f'{n_blk} ({blk_pct:.1f}%)':<15} | {ips:<7.1f}%"
        print(row_str)

        table_data.append({
            "category": cat,
            "attempts": n_att,
            "sanitized": n_san,
            "ssr": f"{ssr:.1f}%",
            "recheck_passed": f"{n_pass} ({pass_pct:.1f}%)",
            "fail_safe_blocked": f"{n_blk} ({blk_pct:.1f}%)",
            "ips": f"{ips:.1f}%"
        })

    print("-" * 95)
    overall_ssr = (tot_san / tot_att * 100.0) if tot_att > 0 else 0.0
    overall_pass = (tot_pass / tot_att * 100.0) if tot_att > 0 else 0.0
    overall_blk = (tot_blk / tot_att * 100.0) if tot_att > 0 else 0.0
    overall_ips = (tot_ips / tot_san * 100.0) if tot_san > 0 else 0.0

    tot_row = f"{'Overall Total (N=100)':<26} | {tot_att:<8} | {tot_san:<9} | {overall_ssr:<7.1f}% | {f'{tot_pass} ({overall_pass:.1f}%)':<16} | {f'{tot_blk} ({overall_blk:.1f}%)':<15} | {overall_ips:<7.1f}%"
    print(tot_row)
    print("=" * 95)

    summary_file = os.path.join(os.path.dirname(__file__), "sanitization_summary.json")
    with open(summary_file, "w", encoding="utf-8") as f:
        json.dump({
            "table": table_data,
            "overall": {
                "attempts": tot_att,
                "sanitized": tot_san,
                "ssr": f"{overall_ssr:.1f}%",
                "recheck_passed": f"{tot_pass} ({overall_pass:.1f}%)",
                "fail_safe_blocked": f"{tot_blk} ({overall_blk:.1f}%)",
                "ips": f"{overall_ips:.1f}%"
            }
        }, f, indent=2)

if __name__ == "__main__":
    generate_summary()
