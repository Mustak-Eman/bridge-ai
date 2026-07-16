from app.ai.prompts.base import PromptDefinition


class PromptNotFoundError(LookupError):
    pass


class PromptRegistry:
    def __init__(
        self,
        prompts: list[PromptDefinition],
    ) -> None:
        self._prompts: dict[str, PromptDefinition] = {}

        for prompt in prompts:
            if prompt.name in self._prompts:
                raise ValueError(
                    f"Prompt '{prompt.name}' is already registered."
                )

            self._prompts[prompt.name] = prompt

    def get(self, name: str) -> PromptDefinition:
        try:
            return self._prompts[name]
        except KeyError as exc:
            raise PromptNotFoundError(
                f"Prompt '{name}' is not registered."
            ) from exc