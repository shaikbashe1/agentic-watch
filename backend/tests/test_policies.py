import pytest
from fastapi.testclient import TestClient


def _create_policy(client: TestClient, action_type: str = "delete_database", decision: str = "block") -> dict:
    resp = client.post("/policies", json={
        "name": f"Test Policy {action_type}",
        "description": "Test",
        "action_type": action_type,
        "decision": decision,
        "is_active": True,
    })
    assert resp.status_code == 201, resp.text
    return resp.json()


class TestPolicyCRUD:
    def test_create_policy(self, client):
        data = _create_policy(client)
        assert data["decision"] == "block"
        assert data["action_type"] == "delete_database"
        assert data["is_active"] is True
        assert "id" in data

    def test_get_policies(self, client):
        _create_policy(client, "delete_file", "warn")
        resp = client.get("/policies")
        assert resp.status_code == 200
        assert len(resp.json()) >= 1

    def test_get_policy_by_id(self, client):
        created = _create_policy(client)
        resp = client.get(f"/policies/{created['id']}")
        assert resp.status_code == 200
        assert resp.json()["id"] == created["id"]

    def test_get_policy_not_found(self, client):
        resp = client.get("/policies/99999")
        assert resp.status_code == 404

    def test_update_policy(self, client):
        created = _create_policy(client)
        resp = client.put(f"/policies/{created['id']}", json={"decision": "warn", "is_active": False})
        assert resp.status_code == 200
        assert resp.json()["decision"] == "warn"
        assert resp.json()["is_active"] is False

    def test_delete_policy(self, client):
        created = _create_policy(client)
        resp = client.delete(f"/policies/{created['id']}")
        assert resp.status_code == 200
        resp2 = client.get(f"/policies/{created['id']}")
        assert resp2.status_code == 404

    def test_duplicate_name_rejected(self, client):
        _create_policy(client)
        resp = client.post("/policies", json={
            "name": "Test Policy delete_database",
            "action_type": "delete_database",
            "decision": "allow",
            "is_active": True,
        })
        assert resp.status_code == 400


class TestPolicyEvaluation:
    def test_evaluate_block(self, client):
        _create_policy(client, "delete_database", "block")
        resp = client.post("/policies/evaluate", json={"action_type": "delete_database"})
        assert resp.status_code == 200
        body = resp.json()
        assert body["decision"] == "block"
        assert "Test Policy" in body["matched_policy"]

    def test_evaluate_warn(self, client):
        _create_policy(client, "delete_file", "warn")
        resp = client.post("/policies/evaluate", json={"action_type": "delete_file"})
        assert resp.status_code == 200
        assert resp.json()["decision"] == "warn"

    def test_evaluate_no_match_defaults_allow(self, client):
        resp = client.post("/policies/evaluate", json={"action_type": "nonexistent_action"})
        assert resp.status_code == 200
        body = resp.json()
        assert body["decision"] == "allow"
        assert body["matched_policy"] is None

    def test_evaluate_inactive_policy_ignored(self, client):
        created = _create_policy(client, "create_file", "block")
        client.put(f"/policies/{created['id']}", json={"is_active": False})
        resp = client.post("/policies/evaluate", json={"action_type": "create_file"})
        assert resp.json()["decision"] == "allow"
