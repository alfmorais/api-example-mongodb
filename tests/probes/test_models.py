from src.app.probes.models import HealthCheck


class TestModels:
    def test_health_checks_success(self):
        _model = HealthCheck(status="ready")

        response = _model.model_dump()

        assert isinstance(response, dict)
        assert response == {"status": "ready"}
