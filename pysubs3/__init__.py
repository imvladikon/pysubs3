#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from pysubs3.ssafile import SSAFile
from pysubs3.ssaevent import SSAEvent
from pysubs3.ssastyle import SSAStyle
from pysubs3 import time, formats, cli, whisper
from pysubs3.common import Color, Alignment
from pysubs3.timestamps import Timestamps, TimeType
from pysubs3.version import __version__

#: Alias for :meth:`SSAFile.load()`.
load = SSAFile.load

#: Alias for :meth:`pysubs3.whisper.load_from_whisper()`.
load_from_whisper = whisper.load_from_whisper

#: Alias for :meth:`pysubs3.time.make_time()`.
make_time = time.make_time
