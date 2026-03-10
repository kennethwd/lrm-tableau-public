SENT_SPLIT = re.compile(r"(?<=[.!?])\s+")

METRICS = ["embedded_default", "burden_shift", "deflection", "interest_concealment"]

def score_text(text: str) -> dict:
    text = (text or "").strip()

    text = (
        text.replace("’", "'")
            .replace("“", '"')
            .replace("”", '"')
            .replace("–", "-")
    )

    if len(text) < 10:
        print("[DEBUG] text too short")
        return {m: 0.0 for m in METRICS}

    sentences = [s.strip() for s in SENT_SPLIT.split(text) if len(s.strip()) > 10]

    print("[DEBUG] sentence_count =", len(sentences))
    print("[DEBUG] first_3_sentences =", sentences[:3])

    if not sentences:
        return {m: 0.0 for m in METRICS}

    rows = []
    for i, s in enumerate(sentences):
        row = analyze_sentence(s, i, len(sentences))
        rows.append(row)

    print("[DEBUG] first_3_rows =", rows[:3])

    df = pd.DataFrame(rows)
    print("[DEBUG] df_columns =", df.columns.tolist())

    if not all(m in df.columns for m in METRICS):
        print("[DEBUG] metric columns missing")
        return {m: 0.0 for m in METRICS}

    scores = df[METRICS].max(numeric_only=True).to_dict()

    return {m: float(scores.get(m, 0.0)) for m in METRICS}
