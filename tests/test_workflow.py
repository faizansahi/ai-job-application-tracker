def test_job_resume_application_workflow(client):
    job = client.post(
        "/jobs",
        json={
            "title": "Python Werkstudent",
            "company": "Acme GmbH",
            "location": "Berlin",
            "description": "We need Python, FastAPI, PostgreSQL, Docker and Git experience.",
        },
    )
    assert job.status_code == 201
    job_id = job.json()["id"]
    analysis = client.post(
        "/resume/analyze",
        json={
            "job_id": job_id,
            "text": "Software developer with Python, FastAPI, Git and Docker project experience.",
        },
    )
    assert analysis.status_code == 200
    assert analysis.json()["score"] == 80.0
    assert analysis.json()["missing_skills"] == ["postgresql"]
    application = client.post(
        "/applications",
        json={"job_id": job_id, "stage": "Applied", "notes": "Applied through careers page"},
    )
    assert application.status_code == 201
    changed = client.patch(f"/applications/{application.json()['id']}", json={"stage": "Interview"})
    assert changed.json()["stage"] == "Interview"
    assert client.get("/analytics").json()["by_stage"]["Interview"] == 1
    assert len(client.get("/jobs?q=werk").json()) == 1


def test_validation_and_missing_resources(client):
    assert (
        client.post("/jobs", json={"title": "x", "company": "", "description": "short"}).status_code
        == 422
    )
    assert (
        client.post(
            "/resume/analyze",
            json={"job_id": 999, "text": "long enough resume content for validation"},
        ).status_code
        == 404
    )
    assert client.patch("/applications/999", json={"stage": "Offer"}).status_code == 404
