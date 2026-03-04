import pandas as pd
import re
from datetime import datetime

from LRM_engine import analyze_sentence

METRICS = [
    "embedded_default",
    "burden_shift",
    "deflection",
    "interest_concealment"
]

SENT_SPLIT = re.compile(r"(?<=[.!?])\s+")

def score_text(text):

    sentences = [
        s.strip() for s in SENT_SPLIT.split(text)
        if len(s.strip()) > 10
    ]

    rows = [
        analyze_sentence(s, i, len(sentences))
        for i, s in enumerate(sentences)
    ]

    df = pd.DataFrame(rows)

    means = df.mean().to_dict()

    return {m: means.get(m, 0) for m in METRICS}


profiles = pd.read_json("profiles.jsonl", lines=True)

run_id = datetime.utcnow().strftime("%Y%m%d_%H%M")

rows = []

for _, r in profiles.iterrows():

    scores = score_text(str(r["text"]))

    for metric, score in scores.items():

        rows.append({
            "run_id": run_id,
            "profile_id": r["profile_id"],
            "name": r["name"],
            "metric": metric,
            "score": score,
            "batch_tag": r["batch_tag"]
        })

out = pd.DataFrame(rows)

out.to_csv("results.csv", index=False)
