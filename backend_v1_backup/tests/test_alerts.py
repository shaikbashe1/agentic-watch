import pytest
from fastapi.testclient import TestClient


def _create_alert(client: TestClient, severity: str = "high") -> dict:
    resp = client.post("/alerts", json={
        "title": "Test Alert",
        "description": "Something happened",
        "severity": severity,
        "source": "policy_engine",
        "status": "open",
    })
    assert resp.status_code == 201, resp.text
    return resp.json()


class TestAlertCRUD:
    def test_create_alert(self, client):
        data = _create_alert(client)
        assert data["severity"] == "high"
        assert data["status"] == "open"
        assert "id" in data

    def test_get_alerts(self, client):
        _create_alert(client)
        resp = client.get("/alerts")
        assert resp.status_code == 200
        assert len(resp.json()) >= 1

    def test_get_alert_by_id(self, client):
        created = _create_alert(client)
        resp = client.get(f"/alerts/{created['id']}")
        assert resp.status_code == 200
        assert resp.json()["id"] == created["id"]

    def test_get_alert_not_found(self, client):
        resp = client.get("/alerts/99999")
        assert resp.status_code == 404

    def test_update_alert_status(self, client):
        created = _create_alert(client)
        resp = client.put(f"/alerts/{created['id']}", json={"status": "acknowledged"})
        assert resp.status_code == 200
        assert resp.json()["status"] == "acknowledged"

    def test_delete_alert(self, client):
        created = _create_alert(client)
        resp = client.delete(f"/alerts/{created['id']}")
        assert resp.status_code == 200
        resp2 = client.get(f"/alerts/{created['id']}")
        assert resp2.status_code == 404

    def test_severity_levels(self, client):
        for sev in ["low", "medium", "high", "critical"]:
            data = _create_alert(client, severity=sev)
            assert data["severity"] == sev


class TestAlertIntegration:
    def test_activity_with_block_policy_creates_alert(self, client):
        # Create a blocking policy
        client.post("/policies", json={
            "name": "Block DB Delete",
            "action_type": "delete_database",
            "decision": "block",
            "is_active": True,
        })
        # Create an activity that triggers the policy
        client.post("/activities", json={
            "agent_name": "test-agent",
            "action_type": "delete_database",
            "action_description": "Attempted deletion",
            "target_resource": "prod-db",
            "status": "pending",
        })
        # Verify alert was generated
        alerts = client.get("/alerts").json()
        assert any(a["source"] == "policy_engine" for a in alerts)
        block_alerts = [a for a in alerts if "block" in a["title"].lower() or "BLOCK" in a["title"]]
        assert len(block_alerts) >= 1

    def test_activity_with_allow_policy_no_alert(self, client):
        client.post("/policies", json={
            "name": "Allow Create",
            "action_type": "create_file",
            "decision": "allow",
            "is_active": True,
        })
        client.post("/activities", json={
            "agent_name": "test-agent",
            "action_type": "create_file",
            "action_description": "Created file",
            "target_resource": "file.txt",
            "status": "success",
        })
        alerts = client.get("/alerts").json()
        policy_alerts = [a for a in alerts if a["source"] == "policy_engine"]
        assert len(policy_alerts) == 0
