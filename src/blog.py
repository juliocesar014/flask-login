from flask import Blueprint, jsonify

blog = Blueprint("blog", __name__)


@blog.get("/")
def status():
    return jsonify({"status":"Up and Running"}), 200