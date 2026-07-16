from collections.abc import Callable
from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class PromptDefinition:
    name: str
    version: str
    system_prompt: str
    build_user_prompt: Callable[..., str]