from __future__ import annotations

from pathlib import Path

from subsmith.models import Segment


class WhisperTranscriber:
    def __init__(
        self,
        model_size: str = "small",
        device: str = "cpu",
        compute_type: str = "int8",
    ) -> None:
        from faster_whisper import WhisperModel

        self._model = WhisperModel(model_size, device=device, compute_type=compute_type)

    def transcribe(self, audio: Path, language: str | None = None) -> list[Segment]:
        segments, _ = self._model.transcribe(str(audio), language=language)
        result: list[Segment] = []
        for segment in segments:
            text = segment.text.strip()
            if not text:
                continue
            result.append(Segment(start=segment.start, end=segment.end, text=text))
        return result
