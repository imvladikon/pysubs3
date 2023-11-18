#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from typing import Dict, Type

from pysubs3.formatbase import FormatBase
from pysubs3.microdvd import MicroDVDFormat
from pysubs3.subrip import SubripFormat
from pysubs3.jsonformat import JSONFormat
from pysubs3.substation import SubstationFormat
from pysubs3.mpl2 import MPL2Format
from pysubs3.tmp import TmpFormat
from pysubs3.webvtt import WebVTTFormat
from pysubs3.exceptions import *

#: Dict mapping file extensions to format identifiers.
FILE_EXTENSION_TO_FORMAT_IDENTIFIER: Dict[str, str] = {
    ".srt": "srt",
    ".ass": "ass",
    ".ssa": "ssa",
    ".sub": "microdvd",
    ".json": "json",
    ".txt": "tmp",
    ".vtt": "vtt",
}

#: Dict mapping format identifiers to implementations (FormatBase subclasses).
FORMAT_IDENTIFIER_TO_FORMAT_CLASS: Dict[str, Type[FormatBase]] = {
    "srt": SubripFormat,
    "ass": SubstationFormat,
    "ssa": SubstationFormat,
    "microdvd": MicroDVDFormat,
    "json": JSONFormat,
    "mpl2": MPL2Format,
    "tmp": TmpFormat,
    "vtt": WebVTTFormat,
}

FORMAT_IDENTIFIERS = list(FORMAT_IDENTIFIER_TO_FORMAT_CLASS.keys())


def get_format_class(format_: str) -> Type[FormatBase]:
    """Format identifier -> format class (ie. subclass of FormatBase)"""
    try:
        return FORMAT_IDENTIFIER_TO_FORMAT_CLASS[format_]
    except KeyError:
        raise UnknownFormatIdentifierError(format_)


def get_format_identifier(ext: str) -> str:
    """File extension -> format identifier"""
    try:
        return FILE_EXTENSION_TO_FORMAT_IDENTIFIER[ext]
    except KeyError:
        raise UnknownFileExtensionError(ext)


def get_file_extension(format_: str) -> str:
    """Format identifier -> file extension"""
    if format_ not in FORMAT_IDENTIFIER_TO_FORMAT_CLASS:
        raise UnknownFormatIdentifierError(format_)

    for ext, f in FILE_EXTENSION_TO_FORMAT_IDENTIFIER.items():
        if f == format_:
            return ext

    raise RuntimeError(f"No file extension for format {format_!r}")


def autodetect_format(content: str) -> str:
    """Return format identifier for given fragment or raise FormatAutodetectionError."""
    formats = set()
    for impl in FORMAT_IDENTIFIER_TO_FORMAT_CLASS.values():
        guess = impl.guess_format(content)
        if guess is not None:
            formats.add(guess)

    if len(formats) == 1:
        return formats.pop()
    elif not formats:
        raise FormatAutodetectionError("No suitable formats")
    else:
        raise FormatAutodetectionError(f"Multiple suitable formats ({formats!r})")
