import pytest

from dataclasses import dataclass
from argguard import ArgGuard


def test_arg_guard_argument_retrieval():
    """
    Description
    """
    ArgGuard.__abstractmethods__ = set()

    # Arrange
    @dataclass
    class Dummy(ArgGuard):
        pass

    test_args = {'a': 'a', 'b': 'b', 'c': 'c'}
    dummy = Dummy()

    # Act
    dummy._assert_args(test_args)
    a, b, c = dummy._get_args('a', 'b', 'c')

    # Assert
    assert (
        a == test_args.get('a') and
        b == test_args.get('b') and
        c == test_args.get('c')
    ), 'Arguments can not be correctly retrieved'

    with pytest.raises(
        AssertionError,
        match=r"Required argument .* is missing",
    ):
        dummy._get_required_args('d')
