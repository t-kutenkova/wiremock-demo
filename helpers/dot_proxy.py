from functools import reduce
from typing import Any, Tuple, Union

SequenceTypes = (list, tuple, set)


class DotProxy:
    """Implementation of proxy with access (read/write) to elements on path by delimiter.

    >>> a = {"a": {"b": 1}, "c": 3, "d": [{"e": 1}, {"e": 2}]}
    >>> dot_proxy_a = DotProxy(a)
    >>> assert dot_proxy_a['a.b'] == 1
    >>> assert dot_proxy_a['c'] == 3
    >>> assert dot_proxy_a['d.[].e'] == [1, 2]

    # dot_proxy_a['a.d'] KeyError: "Can't get value by keys=['a', 'd']: error in key 'd'"
    >>> dot_proxy_a['a.d'] = '4'
    >>> assert dot_proxy_a['a.d'] == '4'
    """

    def __init__(
        self, data: Union[dict, list, tuple, set], delimiter=".", strict=False
    ):
        self._data = data
        self._delimiter = delimiter
        self._strict = strict

    def __setitem__(self, key, value) -> None:
        key_list = key.split(self._delimiter)
        *keys, last_key = key_list

        last_structure_value = self.__get_value(keys)

        if isinstance(last_structure_value, dict):
            last_structure_value[last_key] = value
            return
        elif isinstance(last_structure_value, SequenceTypes):
            if last_key == "[]":
                for index, _ in enumerate(last_structure_value):
                    last_structure_value[index] = value
                return
            for last_value in last_structure_value:
                if not isinstance(last_value, dict):
                    raise KeyError(
                        f"Can't change last values for key={key}. [last values are not equal dict]"
                    )
                last_value[last_key] = value
            return

        raise KeyError(f"Can't change last value for key={key}")

    def __getitem__(self, k):
        return self.__get_value(k.split(self._delimiter))

    def __get_value(self, keys: Tuple["str"]):
        """Recursive get value."""
        try:
            return reduce(self._get_item, keys, self._data)
        except KeyError as e:
            raise KeyError(f"Can't get value by {keys=}: error in key {e}")

    def __str__(self):
        return f"DotProxy: delimiter={self._delimiter} data={self._data}"

    @property
    def data(self):
        return self._data

    def _get_item(
        self, data: Union[list, tuple, set, dict], key: str
    ) -> Union[dict, list, tuple, set, Any]:
        if isinstance(data, dict):
            return data[key]
        elif key == "[]":
            if not isinstance(data, SequenceTypes):
                raise KeyError("Can't get list")
            return data
        elif isinstance(data, SequenceTypes):
            result_data = []
            for index, d in enumerate(data):
                try:
                    result = self._get_item(d, key)
                except KeyError:
                    if self._strict:
                        raise
                    continue

                if isinstance(result, list):
                    result_data.extend(result)
                else:
                    result_data.append(result)
            return result_data
        raise KeyError(f"Can't get {key=} from value with type={type(data)}")
