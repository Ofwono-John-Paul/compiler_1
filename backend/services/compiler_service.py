from backend.models.compiler_models import CompileRequest, CompileResponse
from compiler_pipeline import compile_source


class CompilerService:
    def compile(self, request: CompileRequest) -> CompileResponse:
        data = compile_source(request.source)
        return CompileResponse(
            success=data.get("success", False),
            stage=data.get("stage"),
            error=data.get("error"),
            data=data,
        )
