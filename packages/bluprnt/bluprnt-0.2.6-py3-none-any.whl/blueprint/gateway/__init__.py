import logging
import json
from base64 import b64decode
from functools import wraps
from flask import jsonify, Request, request, g
from requests.exceptions import HTTPError
from ..service import call
from ..models import AssetReference


class User:
    def __init__(self, encoded_user_info):
        user_info = json.loads(b64decode(encoded_user_info + "==="))
        self.id = user_info["user_id"]
        self.path = "users/" + self.id
        self.email = user_info["email"]
        self.email_verified = user_info["email_verified"]


def response(message, **data):
    return jsonify(message=message, **data)


def get_user():
    encoded_user_info = request.headers.get("X-Endpoint-Api-Userinfo")
    if encoded_user_info:
        return User(encoded_user_info)
    return None


def authorize(permission=None):
    def wrap(func):
        @wraps(func)
        def wrapper():
            try:
                user = get_user()
                if not user:
                    return response("Missing authentication information."), 401
                if permission:
                    if not "asset" in request.json:
                        return (
                            response("Missing 'asset' parameter."),
                            400,
                        )
                    asset = AssetReference(request.json["asset"])
                    r = call(
                        "db",
                        "authorize",
                        asset=asset.path,
                        uid=user.id,
                        permission=permission,
                    )
                    r.raise_for_status()
                    if not r.json()["granted"]:
                        return response("Access denied."), 403
                    g.asset = asset
                g.user = user
            except Exception as e:
                logging.exception(e)
                return response("An unexpected error occurred in authorization."), 500
            return func()

        return wrapper

    return wrap


def validate(**kwargs):
    def wrap(func):
        @wraps(func)
        def wrapper():
            try:
                for key in kwargs:
                    valid = kwargs[key](request.json.get(key))
                    if not valid:
                        return response(f"Invalid value for '{key}'"), 400
            except Exception as e:
                logging.exception(e)
                return response("An unexpected error occurred in validation."), 500
            return func()

        return wrapper

    return wrap
