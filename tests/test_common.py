from pysubs3 import Color
import pytest

def test_color_argument_validation():
    Color(r=0, g=0, b=0) # does not raise

    with pytest.raises(ValueError):
        Color(r=0, g=0, b=256)

    with pytest.raises(ValueError):
        Color(r=0, g=0, b=-1)
