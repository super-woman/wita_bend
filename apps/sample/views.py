# -*- coding: utf-8 -*-
"""Rating views."""
from flask import Blueprint, jsonify, make_response, request
from flask.views import MethodView

from ..utils.view_utils import delete_by_id
from .models import Sample
from .schema import SampleSchema

blueprint = Blueprint("sample", __name__, url_prefix="/api/v1/samples")


class SamplesView(MethodView):
    def get(self):
        all_samples = Sample.query.all()
        schema = SampleSchema(many=True)
        return {"samples": schema.dump(all_samples)}, 200

    def post(self):
        request_data = request.get_json()
        schema = SampleSchema()
        obj = schema.load(request_data)
        obj.save()
        return make_response(jsonify({"sample": schema.dump(obj)}), 201)


class SampleView(MethodView):
    def get(self, id):
        sample = Sample.get_or_404(id)
        schema = SampleSchema()
        return make_response(jsonify({"sample": schema.dump(sample)}), 200)

    def put(self, id):
        sample = Sample.get_or_404(id)
        request_data = request.get_json()
        schema = SampleSchema()
        sample = schema.load(request_data, instance=sample, partial=True)
        return make_response(jsonify({"sample": schema.dump(sample)}), 200)

    def delete(self, id):
        return delete_by_id(Sample, id, "Sample")


blueprint.add_url_rule("/", view_func=SamplesView.as_view("samples"))
blueprint.add_url_rule("/<id>", view_func=SampleView.as_view("sample"))
