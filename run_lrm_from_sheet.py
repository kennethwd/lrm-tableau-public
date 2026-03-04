import os
import json
import re
from datetime import datetime, timezone

import pandas as pd
import gspread
from google.oauth2.service_account import Credentials

# We will copy these two files in the workflow step:
# - LRM_engine.py
# - scoring_rules.json
from LRM_engine import analyze_sentence

SENT_SPLIT = re.compile(r"(?<=[.!?])\s+")

METRICS = ["embedded_default", "burden_shift", "deflection", "interest_concealment"]

def score_text(text: str) -> dict:
    text = (text or "").strip()
    if len(text) < 10:
        return {m: 0.0 for m in METRICS}

    sentences = [s.strip() for s in SENT_SPLIT.split(text) if len(s.strip()) > 10]
    if not sentences:
        return {m: 0.0 for m in METRICS}

    rows = [analyze_sentence(s, i, len(sentences)) for i, s in enumerate(sentences)]
    df = pd.DataFrame(rows)

    # mean across sentences
    means = df.mean(numeric_only=True).to_dict()
    return {m: float(means.get(m, 0.0)) for m in METRICS}

def main():
    sheet_id = os.environ["GSHEET_ID"]
    sa_json = os.environ["GOOGLE_SERVICE_ACCOUNT_JSON"]
    profiles_tab = os.environ.get("PROFILES_TAB", "profiles")
    output_tab = os.environ.get("OUTPUT_TAB", "lrm_scores_long")

    creds_info = json.loads(sa_json)
    scopes = ["https://www.googleapis.com/auth/spreadsheets"]
    creds = Credentials.from_service_account_info(creds_info, scopes=scopes)

    gc = gspread.authorize(creds)
    sh = gc.open_by_key(sheet_id)

    ws_profiles = sh.worksheet(profiles_tab)
    records = ws_profiles.get_all_records()

    run_id = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")

    out_rows = []
    for r in records:
        profile_id = str(r.get("profile_id", "")).strip()
        name = str(r.get("name", "")).strip()
        source = str(r.get("source", "")).strip()
        text = str(r.get("text", "")).strip()
        batch_tag = str(r.get("batch_tag", "")).strip()

        scores = score_text(text)

        for metric, score in scores.items():
            out_rows.append({
                "run_id": run_id,
                "profile_id": profile_id,
                "name": name,
                "metric": metric,
                "score": score,
                "batch_tag": batch_tag
            })

    out_df = pd.DataFrame(out_rows)

    # Write output tab (create if missing)
    try:
        ws_out = sh.worksheet(output_tab)
    except gspread.WorksheetNotFound:
        ws_out = sh.add_worksheet(title=output_tab, rows=2000, cols=20)

    ws_out.clear()
    ws_out.update([out_df.columns.tolist()] + out_df.fillna("").values.tolist())

    print(f"✅ Wrote {len(out_df)} rows to '{output_tab}' (run_id={run_id})")

if __name__ == "__main__":
    main()
