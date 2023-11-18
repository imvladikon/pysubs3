import pytest
import pysubs3

def test_identifier_to_class():
    with pytest.raises(pysubs3.UnknownFormatIdentifierError):
        pysubs3.formats.get_format_class("unknown-format-identifier")

def test_ext_to_identifier():
    with pytest.raises(pysubs3.UnknownFileExtensionError):
        pysubs3.formats.get_format_identifier(".xyz")

def test_identifier_to_ext():
    with pytest.raises(pysubs3.UnknownFormatIdentifierError):
        pysubs3.formats.get_file_extension("unknown-format-identifier")

def test_format_detection_fail():
    with pytest.raises(pysubs3.FormatAutodetectionError):
        pysubs3.formats.autodetect_format("")
