from __future__ import annotations

from pydantic import BaseModel, Field, model_validator


class Segment(BaseModel):
    start: float = Field(ge=0)
    end: float = Field(ge=0)
    text: str
    translation: str | None = None

    @model_validator(mode="after")
    def _check_bounds(self) -> Segment:
        if self.end < self.start:
            raise ValueError("Segment end must not precede start")
        return self

    @property
    def duration(self) -> float:
        return self.end - self.start

    def with_translation(self, translation: str) -> Segment:
        return self.model_copy(update={"translation": translation})

    @property
    def display_text(self) -> str:
        return self.translation if self.translation is not None else self.text
