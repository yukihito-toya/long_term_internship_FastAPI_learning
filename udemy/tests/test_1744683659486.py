import pytest

def add(a: int, b: int) -> int:
    """
    Add two numbers.
    """
    return a + b

def test_add():
    assert add(1, 2) == 3
    assert add(-1, 1) == 0
    assert add(0, 0) == 0
    assert add(-1, -1) == -2
    assert add(1000000, 2000000) == 3000000