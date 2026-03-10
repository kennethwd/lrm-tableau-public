Linguistic Risk Measurement (LRM) – Tableau Visualisation Pipeline

This project demonstrates how linguistic risk indicators can be extracted from text and visualised using an automated analytics pipeline.

The solution combines:

Google Sheets for data collection

GitHub Actions for automated LRM scoring

Python for linguistic analysis

Tableau Public for interactive visualisation

The pipeline provides a simple workflow for analysing text sources such as LinkedIn profiles, statements, or documents and visualising linguistic risk signals.

Live Visualisation

Example Tableau dashboard:

https://public.tableau.com/views/LRMScoringVisualisation/LRMVisualisation

Sample Data Source

Example Google Sheet used to collect the input text and store scoring results:

https://docs.google.com/spreadsheets/d/1EaK1LHleTlAWhroHwY3ja1WeO5ej7QUq9geMzjBKy1c

Repository

GitHub pipeline:

https://github.com/kennethwd/lrm-tableau-public

Architecture

The pipeline works as follows:

Text Collection
      │
      ▼
Google Sheet (profiles tab)
      │
      ▼
GitHub Actions Pipeline
      │
      ▼
LRM Engine (Python)
      │
      ▼
Google Sheet (lrm_scores_long tab)
      │
      ▼
Tableau Public Dashboard
Workflow
1. Collect Text Data

Input text (e.g. LinkedIn profile descriptions) is added to the profiles tab of the Google Sheet.

Each record includes:

Column	Description
profile_id	unique identifier
name	individual name
source	text source
text	full text content
batch_tag	optional run tag
2. Run LRM Scoring Pipeline

A GitHub Actions workflow executes the scoring engine.

The pipeline:

Loads the text records

Applies the Linguistic Risk Measurement (LRM) engine

Calculates four linguistic indicators

Metric	Description
embedded_default	implicit assumption framing
burden_shift	responsibility transfer
deflection	evasive or indirect language
interest_concealment	concealed motivations

Scores are written to the lrm_scores_long tab.

3. Tableau Visualisation

Tableau connects directly to the Google Sheet and visualises the scoring results.

Example visualisations include:

Linguistic risk radar charts

Metric comparison bars

Risk heatmaps

Total risk scores

These visualisations allow quick comparison of linguistic patterns across individuals or documents.

Example Output
name	metric	score
Alex Morgan	embedded_default	0.75
Alex Morgan	burden_shift	0.00
Alex Morgan	deflection	0.00
Alex Morgan	interest_concealment	0.00
David Clarke	embedded_default	0.36
David Clarke	burden_shift	1.86
David Clarke	deflection	1.80
David Clarke	interest_concealment	1.05

These scores form the basis of the Tableau dashboard visualisations.

Potential Use Cases

This workflow can be extended to analyse:

Executive communications

Financial disclosures

Regulatory statements

Corporate messaging

Political speeches

Online profiles

The pipeline provides a lightweight framework for linguistic risk analysis at scale.

Future Enhancements

Possible improvements include:

Automated LinkedIn data ingestion

NLP preprocessing and sentence classification

Historical scoring comparisons

Document-level analysis

AI-powered interpretation layer

Web-based dashboard interface
