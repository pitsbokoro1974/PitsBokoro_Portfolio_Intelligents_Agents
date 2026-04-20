Academic Research Pipeline

A Python pipeline that retrieves academic papers from arXiv, cleans and processes them, ranks them by relevance, and stores results in multiple formats.

1. Requirements
Python: 3.10 – 3.13 

Install dependencies
pip install -r requirements.txt

2. Setup

Config options (config.py)
MAX_RESULTS: number of papers fetched per query
ARXIV_API_URL: arXiv endpoint (usually unchanged)

3. Run the pipeline
python main.py (or you could just run main.py)

You will be prompted:

Enter research topic:

If you press Enter without any input, the default query is used:

droop control

4. Outputs

After running, the pipeline generates:

papers.csv
papers.json
papers.db

All files are overwritten each run.

5. Logs

Logs are stored in:

logs.txt

Example:

[2026-04-13 12:00:00] [LOG] Starting pipeline for: machine learning
[2026-04-13 12:00:03] [LOG] Retrieved 20 papers
[2026-04-13 12:00:04] [LOG] After cleaning: 18 papers

6. Testing

Run tests:

pytest
or
pytest -v

What is tested
Cleaning removes invalid/duplicate papers
Classification produces relevance scores (0–1)
Storage creates CSV/JSON/DB files
Full pipeline runs end-to-end

7. Evaluation

Run evaluation:

python evaluate.py (or you could just run the evaluation.py)

Metrics:

retrieval_clean_ratio = cleaned / retrieved
validity_ratio = classified / cleaned
quality_score = weighted combination of both ratios