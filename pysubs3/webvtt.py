#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import re
from typing import List

import pysubs3
from pysubs3.subrip import SubripFormat
from pysubs3.time import make_time


class WebVTTFormat(SubripFormat):
    """
    Web Video Text Tracks (WebVTT) subtitle format implementation

    Currently, this shares implementation with :class:`pysubs3.subrip.SubripFormat`.
    """
    TIMESTAMP = re.compile(r"(\d{0,4}:)?(\d{2}):(\d{2})\.(\d{2,3})")

    @staticmethod
    def ms_to_timestamp(ms: int) -> str:
        result = SubripFormat.ms_to_timestamp(ms)
        return result.replace(',', '.')

    @staticmethod
    def timestamp_to_ms(groups):
        _h, _m, _s, _ms = groups
        if not _h:
            h = 0
        else:
            h = int(_h.strip(":"))
        m, s, ms = map(int, (_m, _s, _ms))
        return make_time(h=h, m=m, s=s, ms=ms)

    @classmethod
    def guess_format(cls, text):
        """See :meth:`pysubs3.formats.FormatBase.guess_format()`"""
        if text.lstrip().startswith("WEBVTT"):
            return "vtt"

    @classmethod
    def to_file(cls, subs, fp, format_, **kwargs):
        """
        See :meth:`pysubs3.formats.FormatBase.to_file()`
        """
        print("WEBVTT\n", file=fp)
        return super(WebVTTFormat, cls).to_file(
            subs=subs, fp=fp, format_=format_, **kwargs)

    @classmethod
    def _get_visible_lines(cls, subs: "pysubs3.SSAFile") -> List["pysubs3.SSAEvent"]:
        visible_lines = [line for line in subs if not line.is_comment]
        visible_lines.sort(key=lambda e: e.start)
        return visible_lines
