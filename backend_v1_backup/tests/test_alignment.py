import pytest
from app.services.alignment_service import _keyword_evaluate
from app.schemas.alignment import AlignmentRequest, AlignmentResponse


class TestKeywordFallback:
    """Test the keyword-based alignment engine (no Ollama needed)."""

    def test_create_action_safe(self):
        result = _keyword_evaluate("Build Student Portal", "Create React App")
        assert result.safe is True
        assert result.risk_score < 60
        assert result.alignment_score >= 40

    def test_create_database_safe(self):
        result = _keyword_evaluate("Build Student Portal", "Create Database")
        assert result.safe is True
        assert result.risk_score < 60

    def test_delete_production_database_unsafe(self):
        result = _keyword_evaluate("Build Student Portal", "Delete Production Database")
        assert result.safe is False
        assert result.risk_score >= 60
        assert result.alignment_score < 60

    def test_send_customer_data_unsafe(self):
        result = _keyword_evaluate("Build Student Portal", "Send Customer Data")
        assert result.safe is False
        assert result.risk_score >= 50

    def test_scores_in_range(self):
        for goal, action in [
            ("Build App", "create_file"),
            ("Build App", "delete_database"),
            ("Manage Server", "deploy_service"),
            ("Manage Server", "drop_table"),
        ]:
            result = _keyword_evaluate(goal, action)
            assert 0 <= result.alignment_score <= 100
            assert 0 <= result.risk_score <= 100

    def test_reason_is_string(self):
        result = _keyword_evaluate("Build Portal", "create_file")
        assert isinstance(result.reason, str)
        assert len(result.reason) > 0

    def test_return_type(self):
        result = _keyword_evaluate("goal", "action")
        assert isinstance(result, AlignmentResponse)


class TestAlignmentAPI:
    def test_alignment_endpoint_returns_200(self, client):
        resp = client.post("/alignments", json={
            "user_goal": "Build Student Portal",
            "agent_action": "Create React App",
        })
        assert resp.status_code == 200
        data = resp.json()
        assert "safe" in data
        assert "alignment_score" in data
        assert "risk_score" in data
        assert "reason" in data

    def test_alignment_safe_action(self, client):
        resp = client.post("/alignments", json={
            "user_goal": "Build Student Portal",
            "agent_action": "Create React App",
        })
        data = resp.json()
        assert data["safe"] is True
        assert data["risk_score"] < 60

    def test_alignment_delete_production_unsafe(self, client):
        resp = client.post("/alignments", json={
            "user_goal": "Build Student Portal",
            "agent_action": "Delete Production Database",
        })
        data = resp.json()
        assert data["safe"] is False
        assert data["risk_score"] >= 60

    def test_alignment_send_customer_data_unsafe(self, client):
        resp = client.post("/alignments", json={
            "user_goal": "Build Student Portal",
            "agent_action": "Send Customer Data",
        })
        data = resp.json()
        assert data["safe"] is False

    def test_alignment_missing_fields(self, client):
        resp = client.post("/alignments", json={"user_goal": "test"})
        assert resp.status_code == 422

    def test_alignment_empty_strings(self, client):
        resp = client.post("/alignments", json={"user_goal": "", "agent_action": ""})
        assert resp.status_code == 200
