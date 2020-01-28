import json

import pytest

from apps.constants.success import messages
from apps.sample.models import Sample

from ...factories import SampleFactory

api_version = "api/v1"


@pytest.mark.usefixtures("db")
class TestLocationsEndpoints:
    def test_get_all_samples(self, client, sample):
        response = client.get(f"{api_version}/samples")
        assert response.status_code == 200
        assert response.json["samples"][0]["name"] == sample.name

    def test_get_sample_succeeds(self, client, sample):
        response = client.get(f"{api_version}/samples")
        assert response.status_code == 200
        assert response.json["samples"][0]["name"] == sample.name

    def test_get_specific_sample_succeeds(self, client, sample):
        response = client.get(f"{api_version}/samples/{sample.id}")
        assert response.status_code == 200
        assert response.json["sample"]["name"] == sample.name

    def test_create_sample_succeeds(self, client):
        sample = SampleFactory.build()
        sample_data = json.dumps(
            {"name": sample.name}
        )
        response = client.post(f"{api_version}/samples/", data=sample_data)
        assert response.status_code == 201
        assert response.json["sample"]["name"] == sample.name

    def test_create_sample_with_missing_fields_fails(self, client):
        sample = SampleFactory.build()
        sample_data = json.dumps({})
        response = client.post(f"{api_version}/samples/", data=sample_data)
        assert response.status_code == 400

    def test_create_sample_with_no_fields_fails(self, client):
        sample = SampleFactory.build()
        sample_data = json.dumps({})
        response = client.post(f"{api_version}/samples/", data=sample_data)
        assert response.status_code == 400

    def test_update_existing_sample_succeeds(self, client, sample):
        new_sample = SampleFactory.build()

        update = json.dumps({"name": new_sample.name})

        response = client.put(
            f"{api_version}/samples/{sample.id}", data=update
        )
        assert response.status_code == 200
        assert response.json["sample"]["name"] == new_sample.name

    def test_update_non_existing_sample_with_fails(self, client):
        new_sample = SampleFactory.build()
        sample_id = 100
        update = json.dumps({"name": new_sample.name})
        response = client.put(
            f"{api_version}/samples/{sample_id}", data=update
        )
        assert response.status_code == 404
        assert response.json["msg"] == f"Sample with id {sample_id} not found"

    def test_delete_existing_sample_succeeds(self, client, sample):
        response = client.delete(f"{api_version}/samples/{sample.id}")
        assert response.status_code == 200
        assert response.json["msg"] == "OK"
        assert response.json["payload"] == "Sample successfully deleted"

    def test_delete_non_existing_sample_fails(self, client):
        sample_id = 100
        response = client.delete(f"{api_version}/samples/{sample_id}")
        assert response.status_code == 404
        assert response.json["msg"] == f"Sample with id {sample_id} not found"
