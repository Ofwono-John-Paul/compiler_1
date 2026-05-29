from dataclasses import dataclass


@dataclass
class CompileRequest:
    source: str


@dataclass
class CompileResponse:
    success: bool
    stage: str | None
    error: str | None
    data: dict
