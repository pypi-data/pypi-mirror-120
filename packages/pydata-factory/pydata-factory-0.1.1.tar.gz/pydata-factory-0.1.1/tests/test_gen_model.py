"""Tests for `pydata_factory` package."""
from pathlib import Path

from pydata_factory.class_model import create_model
from pydata_factory.schema import load_schema


def test_create_model():
    """Test the creation of a new model from a parquet file."""
    path = Path(__file__).parent / "data" / "schemas" / "fb2021.json"
    schema = load_schema(path)
    result = create_model(schema)
    assert "class" in result
