from fastapi import status


class TestViews:
    def test_health_checks_success(self, client, database):
        response = client.get("/health")

        assert response.status_code == status.HTTP_200_OK
        assert response.json() == {"status": "health"}
