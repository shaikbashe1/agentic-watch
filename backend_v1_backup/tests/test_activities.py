import pytest


def _create_activity(client, agent_name="CoderAgent", action_type="create_file", status="success", user_goal=None):
    payload = {
        "agent_name": agent_name,
        "action_type": action_type,
        "action_description": f"{action_type} description",
        "target_resource": "resource.txt",
        "status": status,
    }
    if user_goal:
        payload["user_goal"] = user_goal
    resp = client.post("/activities", json=payload)
    assert resp.status_code == 201, resp.text
    return resp.json()


class TestActivityCRUD:
    def test_create_activity(self, client):
        data = _create_activity(client)
        assert data["agent_name"] == "CoderAgent"
        assert data["action_type"] == "create_file"
        assert "id" in data
        assert "timestamp" in data

    def test_get_activities(self, client):
        _create_activity(client)
        resp = client.get("/activities")
        assert resp.status_code == 200
        assert len(resp.json()) >= 1

    def test_get_activity_by_id(self, client):
        created = _create_activity(client)
        resp = client.get(f"/activities/{created['id']}")
        assert resp.status_code == 200
        assert resp.json()["id"] == created["id"]

    def test_get_activity_not_found(self, client):
        resp = client.get("/activities/99999")
        assert resp.status_code == 404

    def test_delete_activity(self, client):
        created = _create_activity(client)
        resp = client.delete(f"/activities/{created['id']}")
        assert resp.status_code == 200
        resp2 = client.get(f"/activities/{created['id']}")
        assert resp2.status_code == 404

    def test_metadata_field(self, client):
        resp = client.post("/activities", json={
            "agent_name": "Agent1",
            "action_type": "test",
            "action_description": "test",
            "target_resource": "res",
            "status": "success",
            "metadata": {"key": "value"},
        })
        assert resp.status_code == 201
        data = resp.json()
        assert data.get("metadata") == {"key": "value"}


class TestActivityStats:
    def test_stats_counts(self, client):
        _create_activity(client, status="success")
        _create_activity(client, status="warning")
        _create_activity(client, status="blocked")
        resp = client.get("/stats")
        assert resp.status_code == 200
        data = resp.json()
        assert data["total"] >= 3
        assert data["success"] >= 1
        assert data["warning"] >= 1
        assert data["blocked"] >= 1

    def test_agent_stats(self, client):
        _create_activity(client, agent_name="CoderAgent")
        _create_activity(client, agent_name="PlannerAgent")
        _create_activity(client, agent_name="CoderAgent")
        resp = client.get("/activities/stats/agents")
        assert resp.status_code == 200
        data = resp.json()
        agents = {r["agent_name"]: r["total"] for r in data}
        assert agents.get("CoderAgent", 0) >= 2
        assert agents.get("PlannerAgent", 0) >= 1


class TestAlignmentIntegration:
    def test_activity_with_user_goal_gets_scores(self, client):
        data = _create_activity(client, action_type="create_file", user_goal="Build Student Portal")
        assert data["risk_score"] is not None
        assert data["alignment_score"] is not None
        assert 0 <= data["risk_score"] <= 100
        assert 0 <= data["alignment_score"] <= 100

    def test_destructive_action_high_risk(self, client):
        data = _create_activity(client, action_type="delete_production_database",
                                user_goal="Build Student Portal")
        assert data["risk_score"] is not None
        assert data["risk_score"] >= 40

    def test_create_action_low_risk(self, client):
        data = _create_activity(client, action_type="create_react_app",
                                user_goal="Build Student Portal")
        assert data["risk_score"] is not None
        assert data["risk_score"] < 60

    def test_policy_decision_stored(self, client):
        # Create a block policy first
        client.post("/policies", json={
            "name": "Block Delete DB",
            "action_type": "delete_database",
            "decision": "block",
            "is_active": True,
        })
        data = _create_activity(client, action_type="delete_database")
        assert data["policy_decision"] == "block"
