from job_tracker.services import analyze_match, extract_skills


def test_matching_boundaries():
    assert extract_skills("git GitHub Pythonic python") == {"git", "python"}
    assert analyze_match("Python", "No recognised skills here")["score"] == 0


def test_saved_score_conflict_and_cascade(client):
    job = client.post(
        "/jobs",
        json={
            "title": "Backend developer",
            "company": "Sample GmbH",
            "description": "Python, Docker and PostgreSQL required",
        },
    ).json()
    payload = {"job_id": job["id"]}
    application = client.post("/applications", json=payload).json()
    assert client.post("/applications", json=payload).status_code == 409
    score = client.post(
        "/resume/analyze", json={"job_id": job["id"], "text": "Python and Docker sample experience"}
    ).json()["score"]
    assert client.get("/analytics").json()["average_match_score"] == score
    assert (
        client.patch(f"/applications/{application['id']}", json={"match_score": 101}).status_code
        == 422
    )
    assert (
        client.put(
            f"/jobs/{job['id']}",
            json={
                "title": "Updated backend role",
                "company": "Sample GmbH",
                "description": "Python and SQL project experience",
            },
        ).status_code
        == 200
    )
    assert client.delete(f"/jobs/{job['id']}").status_code == 204
    assert client.get("/analytics").json()["total_applications"] == 0
    assert client.delete(f"/jobs/{job['id']}").status_code == 404
