# Evidence provenance
The demo used a fictional CV and fictional Sample Logistics GmbH vacancy. No personal CV or application records were used.

`demo.json` contains actual HTTP requests and responses from a local Uvicorn server backed by a disposable SQLite database. `../images/application-analytics.png` is a Matplotlib chart of its analytics response. `../images/swagger-api.png` is a real browser screenshot of that running API's Swagger page.

Reproduce with `python scripts/demo_workflow.py` after starting the API with a fresh database. The chart is output visualization, not an application dashboard screenshot.

`../images/job-match-result.png` charts the actual matched and missing skills from the same API execution.
