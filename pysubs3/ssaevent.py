#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import dataclasses
import re
import warnings
from numbers import Real
from typing import Optional, Dict, Any, ClassVar, Union

from pysubs3.common import IntOrFloat
from pysubs3.time import ms_to_str, make_time
from pysubs3.timestamps import Timestamps, TimeType


@dataclasses.dataclass(repr=False, eq=False, order=False)
class SSAEvent:
    """
    A SubStation Event, ie. one subtitle.

    In SubStation, each subtitle consists of multiple "fields" like Start, End and Text.
    These are exposed as attributes (note that they are lowercase; see :attr:`SSAEvent.FIELDS` for a list).
    Additionaly, there are some convenience properties like :attr:`SSAEvent.plaintext` or :attr:`SSAEvent.duration`.

    This class defines an ordering with respect to (start, end) timestamps.

    .. tip :: Use :func:`pysubs3.make_time()` to get times in milliseconds.

    Example::

        >>> ev = SSAEvent(start=make_time(s=1), end=make_time(s=2.5), text="Hello World!")

    """
    OVERRIDE_SEQUENCE: ClassVar = re.compile(r"{[^}]*}")

    start: int = 0  #: Subtitle start time (in milliseconds)
    end: int = 10000  #: Subtitle end time (in milliseconds)
    text: str = ""  #: Text of subtitle (with SubStation override tags)
    marked: bool = False  #: (SSA only)
    layer: int = 0  #: Layer number, 0 is the lowest layer (ASS only)
    style: str = "Default"  #: Style name
    name: str = ""  #: Actor name
    marginl: int = 0  #: Left margin
    marginr: int = 0  #: Right margin
    marginv: int = 0  #: Vertical margin
    effect: str = ""  #: Line effect
    type: str = "Dialogue"  #: Line type (Dialogue/Comment)
    language: str = None

    @property
    def FIELDS(self):
        """All fields in SSAEvent."""
        warnings.warn("Deprecated in 1.2.0 - it's a dataclass now", DeprecationWarning)
        return frozenset(field.name for field in dataclasses.fields(self))

    @property
    def duration(self) -> IntOrFloat:
        """
        Subtitle duration in milliseconds (read/write property).

        Writing to this property adjusts :attr:`SSAEvent.end`.
        Setting negative durations raises :exc:`ValueError`.
        """
        return self.end - self.start

    @duration.setter
    def duration(self, ms: int):
        if ms >= 0:
            self.end = self.start + ms
        else:
            raise ValueError("Subtitle duration cannot be negative")

    @property
    def is_comment(self) -> bool:
        """
        When true, the subtitle is a comment, ie. not visible (read/write property).

        Setting this property is equivalent to changing
        :attr:`SSAEvent.type` to ``"Dialogue"`` or ``"Comment"``.
        """
        return self.type == "Comment"

    @is_comment.setter
    def is_comment(self, value: bool):
        if value:
            self.type = "Comment"
        else:
            self.type = "Dialogue"

    @property
    def is_drawing(self) -> bool:
        """Returns True if line is SSA drawing tag (ie. not text)"""
        from .substation import parse_tags
        return any(sty.drawing for _, sty in parse_tags(self.text))

    @property
    def plaintext(self) -> str:
        """
        Subtitle text as multi-line string with no tags (read/write property).

        Writing to this property replaces :attr:`SSAEvent.text` with given plain
        text. Newlines are converted to ``\\N`` tags.
        """
        text = self.text
        text = self.OVERRIDE_SEQUENCE.sub("", text)
        text = text.replace(r"\h", " ")
        text = text.replace(r"\n", "\n")
        # text = text.replace(r"\N", "\n")
        return text

    @plaintext.setter
    def plaintext(self, text: str):
        pass
        # self.text = text.replace("\n", r"\N")

    def shift(self, h: IntOrFloat=0, m: IntOrFloat=0, s: IntOrFloat=0, ms: IntOrFloat=0,
              frames: Optional[int]=None, fps: Optional[Union[Real,Timestamps]]=None):
        """
        Shift start and end times.

        See :meth:`SSAFile.shift()` for full description.

        """
        if frames is None and fps is None:
            delta = make_time(h=h, m=m, s=s, ms=ms)
            self.start += delta
            self.start = max(self.start, 0)
            self.end += delta
            self.end = max(self.end, 0)
        elif frames is None or fps is None:
            raise ValueError("Both fps and frames must be specified")
        else:
            if isinstance(fps, Real):
                timestamps = Timestamps.from_fps(fps)
            elif isinstance(fps, Timestamps):
                timestamps = fps
            else:
                raise TypeError("Unexpected type for fps")

            start_frame = timestamps.ms_to_frames(self.start, TimeType.START)
            end_frame = timestamps.ms_to_frames(self.end, TimeType.END)

            start_frame += frames
            end_frame += frames

            try:
                self.start = timestamps.frames_to_ms(start_frame, TimeType.START)
            except ValueError:
                self.start = 0
            
            try:
                self.end = timestamps.frames_to_ms(end_frame, TimeType.END)
            except ValueError:
                self.end = 0

    def copy(self) -> "SSAEvent":
        """Return a copy of the SSAEvent."""
        return SSAEvent(**self.as_dict())

    def as_dict(self) -> Dict[str, Any]:
        # dataclasses.asdict() would recursively dictify Color objects, which we don't want
        return {field.name: getattr(self, field.name) for field in dataclasses.fields(self)}

    def equals(self, other: "SSAEvent") -> bool:
        """Field-based equality for SSAEvents."""
        if isinstance(other, SSAEvent):
            return self.as_dict() == other.as_dict()
        else:
            raise TypeError("Cannot compare to non-SSAEvent object")

    def __eq__(self, other) -> bool:
        # XXX document this
        if not isinstance(other, SSAEvent):
            return NotImplemented
        return self.start == other.start and self.end == other.end

    def __ne__(self, other) -> bool:
        if not isinstance(other, SSAEvent):
            return NotImplemented
        return self.start != other.start or self.end != other.end

    def __lt__(self, other) -> bool:
        if not isinstance(other, SSAEvent):
            return NotImplemented
        return (self.start, self.end) < (other.start, other.end)

    def __le__(self, other) -> bool:
        if not isinstance(other, SSAEvent):
            return NotImplemented
        return (self.start, self.end) <= (other.start, other.end)

    def __gt__(self, other) -> bool:
        if not isinstance(other, SSAEvent):
            return NotImplemented
        return (self.start, self.end) > (other.start, other.end)

    def __ge__(self, other) -> bool:
        if not isinstance(other, SSAEvent):
            return NotImplemented
        return (self.start, self.end) >= (other.start, other.end)

    def __repr__(self):
        return f"<SSAEvent type={self.type} start={ms_to_str(self.start)} end={ms_to_str(self.end)} text={self.text!r}>"
