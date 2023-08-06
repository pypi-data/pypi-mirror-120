from abc import ABC, abstractmethod
from collections.abc import Mapping


class ArgGuard(ABC):
    def _assert_args(self, args: Mapping):
        self.__args = args
        self._arg_guard()

    def _get_args(self, *requested_args: str):
        values = [self.__args.get(key) for key in requested_args]
        return values

    def _get_required_args(self, *requested_args: str):
        for key in requested_args:
            assert (
                key in self.__args
            ), 'Required argument "%r" is missing' % key

        values = [self.__args.get(key) for key in requested_args]
        return values

    @abstractmethod
    def _arg_guard(self):
        pass
