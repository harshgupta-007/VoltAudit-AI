"""Structured logging and observability tracing for Antigravity Skills."""

import json
import logging
import time
from collections.abc import Callable
from functools import wraps
from typing import Any, TypeVar, cast

# Setup structured logger
logger = logging.getLogger("voltaudit_skills")
logger.setLevel(logging.INFO)

# Avoid adding multiple handlers if already configured
if not logger.handlers:
    handler = logging.StreamHandler()
    formatter = logging.Formatter(
        '{"timestamp": "%(asctime)s", "level": "%(levelname)s", "message": %(message)s}'
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)

F = TypeVar("F", bound=Callable[..., Any])


def trace_skill(skill_id: str, skill_name: str) -> Callable[[F], F]:
    """Decorator to trace execution time, log inputs/outputs, and catch errors for a skill.

    Args:
        skill_id: Stable identifier of the skill (e.g. SPK-001-SK-001).
        skill_name: Human readable name of the skill.

    Returns:
        Decorated function.
    """

    def decorator(func: F) -> F:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            start_time = time.perf_counter()
            log_payload: dict[str, Any] = {
                "skill_id": skill_id,
                "skill_name": skill_name,
                "event": "execution_start",
                "args": [str(a) for a in args],
                "kwargs": {k: str(v) for k, v in kwargs.items()},
            }
            logger.info(json.dumps(log_payload))

            try:
                result = func(*args, **kwargs)
                duration = time.perf_counter() - start_time
                success_payload = {
                    "skill_id": skill_id,
                    "skill_name": skill_name,
                    "event": "execution_success",
                    "duration_seconds": round(duration, 4),
                    "result_summary": str(result)[:200],
                }
                logger.info(json.dumps(success_payload))
                return result
            except Exception as exc:
                duration = time.perf_counter() - start_time
                error_payload = {
                    "skill_id": skill_id,
                    "skill_name": skill_name,
                    "event": "execution_failure",
                    "duration_seconds": round(duration, 4),
                    "error_class": exc.__class__.__name__,
                    "error_message": str(exc),
                }
                logger.error(json.dumps(error_payload))
                raise exc

        return cast(F, wrapper)

    return decorator
