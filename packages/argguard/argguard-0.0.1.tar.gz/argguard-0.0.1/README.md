# ArgGuard [![Tests Actions Status](https://github.com/gcascio/arg-guard/workflows/Tests/badge.svg)](https://github.com/gcascio/arg-guard/actions)

ArgGuard is a simple abstract utility class to remove some boilerplate code when asserting class arguments.

## Usage

The `ArgGuard` class provides the protected abstract `_argGuard` method. This is the method where all assertions, checks and validations of the class arguments should take place. Every class that extends the `ArgGuard` class needs to implement this method.

A second central method is `_assert_args` which stores the provided arguments and calls `_argGuard`. This method should be called as soon as possible in the constructor of the class to be guarded.

## API

| Method               | Args                       | Description                                                      |
|----------------------|----------------------------|------------------------------------------------------------------|
| `_arg_guard`         | `self`                     | Abstract method where all assertions should take pace            |
| `_assert_args`       | `self`, `args`             | Stores the provided arguments and calls `_argGuard`              |
| `_get_args`          | `self`, `*requested_args`  | Retrieves all requested arguments                                |
| `_get_required_args` | `self`, `*requested_args`  | Retrieves all requested arguments and fails if they are missing  |

## Example

```python
# Without ArgGuard
class A:
    def __init__(self, a, b, c=0):
        assert (
            'a' in self.__args
        ), 'Required argument "a" is missing'

        assert (
            'b' in self.__args
        ), 'Required argument "b" is missing'

        assert (
            a % b == 0
        ), 'a ({}) must be divisible by b ({})'.format(a, b)

        self.state = a // b + c

# With ArgGuard
class A(ArgGuard):
    def __init__(self, a, b, c=0):
        self._assert_args(locals())
        self.state = a // b + c

    def _arg_guard(self):
        # If a required argument is missing, an error is thrown
        a, b = self._get_required_args('a', 'b')

        assert (
            a % b == 0
        ), 'a ({}) must be divisible by b ({})'.format(a, b)
```