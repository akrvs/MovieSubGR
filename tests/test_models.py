from __future__ import annotations

import pytest
from pydantic import ValidationError

from subsmith.models import Segment


def test_duration_is_end_minus_start():
    segment = Segment(start=1.0, end=3.5, text="hi")
    assert segment.duration == pytest.approx(2.5)


def test_display_text_prefers_translation():
    segment = Segment(start=0, end=1, text="hello").with_translation("geia")
    assert segment.display_text == "geia"


def test_display_text_falls_back_to_source():
    assert Segment(start=0, end=1, text="hello").display_text == "hello"


def test_with_translation_does_not_mutate_original():
    original = Segment(start=0, end=1, text="hello")
    translated = original.with_translation("geia")
    assert original.translation is None
    assert translated.translation == "geia"


def test_end_before_start_is_rejected():
    with pytest.raises(ValidationError):
        Segment(start=2.0, end=1.0, text="bad")


def test_negative_start_is_rejected():
    with pytest.raises(ValidationError):
        Segment(start=-1.0, end=1.0, text="bad")
