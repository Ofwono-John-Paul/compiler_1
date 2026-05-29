from flask import Blueprint, jsonify, request

from backend.models.compiler_models import CompileRequest
from backend.services.compiler_service import CompilerService


compiler_bp = Blueprint("compiler", __name__, url_prefix="/api")
service = CompilerService()


@compiler_bp.get("/health")
def health():
    return jsonify({"status": "ok"})


@compiler_bp.post("/compile")
def compile_code():
    payload = request.get_json(silent=True) or {}
    source = payload.get("source", "")

    compile_request = CompileRequest(source=source)
    response = service.compile(compile_request)

    status_code = 200 if response.success else 400
    return jsonify(
        {
            "success": response.success,
            "stage": response.stage,
            "error": response.error,
            "result": response.data,
        }
    ), status_code
