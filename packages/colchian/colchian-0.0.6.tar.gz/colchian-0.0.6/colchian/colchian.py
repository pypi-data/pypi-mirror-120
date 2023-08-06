from logging import getLogger
from typing import Union, List, Any
from copy import copy


class Colchian:
    logger = getLogger()

    type_factories = {}

    @staticmethod
    def format_keys(keys: List[str]):
        keys = "".join(
            f"[\"{key}\"]" if i == 0 else f"[\"{key}\"]"
            if isinstance(key, str) and len(key) > 0 and key[0] + key[-1] != "[]"
            else str(key) for i, key in enumerate(keys))
        return f'`{keys}`'

    @classmethod
    def text_bool(cls, x: Any, strict: bool, keys: List[str]) -> bool:
        if isinstance(x, bool):
            return x
        if isinstance(x, str):
            if x.lower() in ['f', 'false']:
                return False
            if not strict or x.lower() in ['t', 'true']:
                return True
        raise SyntaxError(f'Invalid text_bool value: {x} {cls.format_keys(keys)}')

    @classmethod
    def _execute_callable(cls, x, data_type, *args, strict, keys, **kwargs):
        try:
            return data_type(x, *args, strict=strict, keys=keys, **kwargs)
        except SyntaxError as e:
            raise e
        except Exception as e:
            if hasattr(data_type, '__name__'):
                name = data_type.__name__
            else:
                name = 'unnamed function {data_type}'
            raise SyntaxError(f'value at {cls.format_keys(keys)} passed to `{name}` raised {e}')

    @classmethod
    def validated(cls, x: Any, data_type: Any, strict: bool = True, _keys: Union[List, None] = None):
        if _keys is None:
            _keys = []
        if isinstance(data_type, dict):
            if not isinstance(x, dict):
                raise SyntaxError(f'expected {cls.format_keys(_keys)} to be a dict, not a {type(x)}')
            # if a constructor override was provided for type of x, call that with x, instead of the type constructor
            for t in cls.type_factories:
                if isinstance(x, t):
                    result = cls.type_factories[t](x)
                    # no check for multiple matches, first hit wins
                    break
            else:
                result = type(x)()
            wildcards = {
                key: dt for key, dt in data_type.items()
                if callable(key) or isinstance(key, tuple) or key.split(':')[0] == '*'
            }
            used_keys = []
            for key, type_value in data_type.items():
                if key not in wildcards:
                    new_keys = _keys + [key]
                    if not isinstance(key, str) and strict:
                        raise SyntaxError(f'non-string dictionary key {cls.format_keys(_keys)}')
                    # if the value is optional
                    if key not in x and (
                            (hasattr(type_value, '__origin__')
                             and type_value.__origin__ == Union
                             and type(None) in type_value.__args__) or
                            (isinstance(type_value, tuple)
                             and None in type_value)):
                        continue
                    if key not in x:
                        raise SyntaxError(f'missing required key {cls.format_keys(_keys)}')
                    result[key] = cls.validated(x[key], type_value, strict, new_keys)
                    used_keys.append(key)
            if wildcards:
                for key, value in x.items():
                    if key not in used_keys:
                        new_keys = _keys + [key]
                        for wildcard in wildcards:
                            try:
                                if isinstance(wildcard, type):
                                    if not isinstance(key, wildcard):
                                        raise SyntaxError(
                                            f'key {cls.format_keys(new_keys)} not of specified type {type}')
                                elif (
                                    (callable(wildcard) and wildcard(key, strict=strict, keys=new_keys) != key)
                                    or
                                    (isinstance(wildcard, tuple) and callable(wildcard[0]) and
                                     wildcard[0](key, *wildcard[1:], strict=strict, keys=new_keys) != key)
                                   ):
                                    raise SyntaxError(
                                        f'mismatch between key {cls.format_keys(new_keys)} and generated key')
                                elif isinstance(wildcard, tuple) and not callable(wildcard[0]) and key not in wildcard:
                                    raise SyntaxError(
                                        f'restricted key {cls.format_keys(new_keys)} not in {wildcard}')
                                y = cls.validated(value, data_type[wildcard], strict, new_keys)
                                break
                            except SyntaxError as e:
                                if len(wildcards) == 1:
                                    raise SyntaxError(f'could not match to only wildcard {wildcard}, raised "{e}"')
                                continue
                        else:
                            if strict:
                                raise SyntaxError(
                                    f'value of {cls.format_keys(new_keys)} could not be matched to wildcard')
                            result[key] = x[key]
                            continue
                        result[key] = y
            return result
        elif hasattr(data_type, '__origin__') and (data_type.__origin__ == Union):
            result = cls.validated(x, tuple(data_type.__args__), strict, _keys)
        elif isinstance(data_type, tuple):
            if data_type and not isinstance(data_type[0], type) and callable(data_type[0]):
                result = cls._execute_callable(x, data_type[0], *data_type[1:], strict=strict, keys=_keys)
            else:
                if isinstance(data_type[-1], str):
                    # TODO: generate help from final string
                    data_type = data_type[:-1]
                for type_value in data_type:
                    # tuple may contain None when checking optional values
                    if type_value is None:
                        continue
                    try:
                        result = cls.validated(x, type_value, strict, _keys)
                        break
                    except SyntaxError as e:
                        if len(data_type) == 1 or (len(data_type) and None in data_type):
                            raise e
                        continue
                else:
                    raise SyntaxError(f'value does not match any of the optional types at {cls.format_keys(_keys)}')
        elif hasattr(data_type, '__origin__') and (data_type.__origin__ == list):
            result = cls.validated(x, list(data_type.__args__), strict, _keys)
        elif isinstance(data_type, list):
            # read an empty list as a list of any type (any list can be empty)
            data_type = [Any] if not data_type else data_type
            if not isinstance(x, list):
                raise SyntaxError(f'expected a list at {cls.format_keys(_keys)}, got {type(x)}')
            if len(data_type) != 1:
                raise SyntaxError(
                    f'multiple types for list content unexpected at {cls.format_keys(_keys)}: {data_type}')
            result = [cls.validated(elem, data_type[0], strict, _keys + [f'[{n}]']) for n, elem in enumerate(x)]
        elif isinstance(data_type, type):
            if isinstance(x, data_type):
                result = x
            else:
                if strict:
                    raise SyntaxError(f'strict type mismatch (no casting) at {cls.format_keys(_keys)}, '
                                      f'expected `{data_type.__name__}`, found `{type(x).__name__}`')
                try:
                    result = data_type(x)
                except ValueError:
                    raise SyntaxError(f'type mismatch, casting failed at {cls.format_keys(_keys)}, '
                                      f'expected `{data_type.__name__}`, found `{type(x).__name__}`')
        elif data_type is Any:
            result = x
        elif callable(data_type):
            result = cls._execute_callable(x, data_type, strict=strict, keys=_keys)
        elif x != data_type:
            # remaining option is identity, the "data_type" is a value that's required
            raise SyntaxError(f'value "{x}" does not match expected "{data_type}" at {cls.format_keys(_keys)}')
        else:
            result = copy(data_type)
        return result
