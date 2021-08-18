from flask import jsonify

from services import tabnews as tabnews_service


def list_tabnews():
    return jsonify(tabnews_service.list_tabnews())


def create_tabnews(body, token_info=None):
    tabnews = tabnews_service.create_tabnews(
        body["title"],
        body.get("description"),
        token_info["email"],
    )
    return jsonify(tabnews), 201
