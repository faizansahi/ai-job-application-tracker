# API
The interactive contract is at `/docs`; JSON OpenAPI is at `/openapi.json`.

| Method | Route | Behavior |
|---|---|---|
| GET | /health | Process liveness |
| POST / GET | /jobs | Create (201) / search by optional q |
| PUT / DELETE | /jobs/{id} | Replace / delete with application cascade |
| POST | /applications | Create application; duplicate job returns 409 |
| PATCH | /applications/{id} | Set stage, notes, or a score from 0 to 100 |
| POST | /resume/analyze | Compute taxonomy score; save it if application exists |
| GET | /analytics | Counts by stage and average saved match score |

Create a job with title, company, and a description of at least 20 characters. Resume analysis accepts job_id and text (20–200,000 characters). Missing resources return 404; malformed data returns 422.

The deterministic score is matched required skills divided by recognized required skills. No recognized required skills yields 0.0. It is not an ATS ranking prediction. Read [demo.json](results/demo.json) for complete fictional requests and real responses.
