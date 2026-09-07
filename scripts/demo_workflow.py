"""Exercise a running API using fictional candidate data and save actual responses."""

import argparse
import json
from pathlib import Path

import httpx
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--base-url", default="http://127.0.0.1:8000")
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    output = root / "docs/results"
    images = root / "docs/images"
    output.mkdir(parents=True, exist_ok=True)
    images.mkdir(parents=True, exist_ok=True)
    record = []
    with httpx.Client(base_url=args.base_url, timeout=30, trust_env=False) as client:

        def request(method, path, **kwargs):
            response = client.request(method, path, **kwargs)
            response.raise_for_status()
            value = response.json()
            record.append(
                {
                    "method": method,
                    "path": path,
                    "request": kwargs.get("json"),
                    "status": response.status_code,
                    "response": value,
                }
            )
            return value

        request("GET", "/health")
        job = request(
            "POST",
            "/jobs",
            json={
                "title": "Python Backend Developer",
                "company": "Sample Logistics GmbH",
                "location": "Berlin",
                "description": "Python FastAPI PostgreSQL Docker Git experience required",
            },
        )
        application = request(
            "POST",
            "/applications",
            json={"job_id": job["id"], "stage": "Applied", "notes": "Fictional demo application"},
        )
        match = request(
            "POST",
            "/resume/analyze",
            json={
                "job_id": job["id"],
                "text": "Sample candidate has Python FastAPI Docker Git project experience.",
            },
        )
        request("PATCH", f"/applications/{application['id']}", json={"stage": "Interview"})
        analytics = request("GET", "/analytics")
        assert match["score"] == 80.0
        assert analytics["average_match_score"] == 80.0
    (output / "demo.json").write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")
    fig, ax = plt.subplots(figsize=(9, 4.5))
    ax.bar(analytics["by_stage"].keys(), analytics["by_stage"].values(), color="#187c9a")
    ax.set(
        title=f"Sample application funnel | skill match {match['score']}%", ylabel="Applications"
    )
    ax.set_yticks(range(max(analytics["by_stage"].values()) + 1))
    fig.text(
        0.02,
        0.02,
        "Actual FastAPI response | fictional CV and job | missing skill: PostgreSQL",
        fontsize=9,
    )
    fig.tight_layout(rect=(0, 0.06, 1, 1))
    fig.savefig(images / "application-analytics.png", dpi=150)
    plt.close(fig)
    fig, ax = plt.subplots(figsize=(9, 4.5))
    skills = match["matched_skills"] + match["missing_skills"]
    values = [1] * len(match["matched_skills"]) + [0] * len(match["missing_skills"])
    ax.barh(skills, [1] * len(skills), color=["#187c9a" if v else "#dddddd" for v in values])
    for index, value in enumerate(values):
        ax.text(
            0.03,
            index,
            "Matched" if value else "Missing",
            va="center",
            color="white" if value else "black",
        )
    ax.set(title=f"Python Backend Developer | {match['score']}% skill overlap", xlim=(0, 1))
    ax.set_xticks([])
    ax.invert_yaxis()
    fig.text(
        0.02,
        0.02,
        "Actual /resume/analyze response | fictional CV and vacancy | not a hiring prediction",
        fontsize=9,
    )
    fig.tight_layout(rect=(0, 0.06, 1, 1))
    fig.savefig(images / "job-match-result.png", dpi=150)
    plt.close(fig)
    print(json.dumps({"match": match, "analytics": analytics}, indent=2))


if __name__ == "__main__":
    main()
