"""Test main."""
from celltest.cli import main


def test_main():
  """Test main."""
  assert main([]) == 0
