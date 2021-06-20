# Annotation Collector

To get stats on `Callable` annotations, run:

```bash
./callable_annotations.py <directory>

```

To see the actual `Callable` annotations, run:

```bash
./callable_annotations.py <directory> --show-callables
```

For example:

```bash
$ ./callable_annotations.py ~/Programs/typeshed/stdlib/xmlrpc/
Callables of arity 0: 2
Callables of arity 1: 15
Callables of arity 2: 5
Callables of arity 3: 1
Callables of arity 4: 0
Callables of arity 5: 0
Callables with arbitrary parameters: 2
Callback Protocols: 6

$ ./callable_annotations.py ~/Programs/typeshed/stdlib/concurrent/ --show-callables
Callables of arity 0: 2
    Callable[[], None]
    Callable[[], None]
Callables of arity 1: 15
    Callable[[Any], None]
    Callable[[str], Any]
    Callable[[str], Any]
    Callable[[str], Any]
    Callable[[str], Any]
    Callable[[str], Any]
    Callable[[str], Any]
    Callable[[str], Any]
    Callable[[str], Any]
    Callable[[str], Any]
    Callable[[str], Any]
    Callable[[str], Any]
    Callable[[str], Any]
    Callable[[str], str]
    Callable[[str], str]
Callables of arity 2: 5
    Callable[[Optional[str], Tuple[_Marshallable, ...]], Union[Fault, Tuple[_Marshallable, ...]]]
    Callable[[Optional[str], Tuple[_Marshallable, ...]], Union[Fault, Tuple[_Marshallable, ...]]]
    Callable[[Unmarshaller, str], None]
    Callable[[str, Tuple[_Marshallable, ...]], _Marshallable]
    Callable[[str, Tuple[_Marshallable, ...]], _Marshallable]
Callables of arity 3: 1
    Callable[[Marshaller, Any, Callable[[str], Any]], None]
Callables of arity 4: 0
Callables of arity 5: 0
Callables with arbitrary parameters: 2
    Callable[..., Any]
    Callable[..., Any]
Callback Protocols: 6
    _DispatchArity0 - def __call__(self) -> _Marshallable: pass
    _DispatchArity1 - def __call__(self, __arg1: _Marshallable) -> _Marshallable: pass
    _DispatchArity2 - def __call__(self, __arg1: _Marshallable, __arg2: _Marshallable) -> _Marshallable: pass
    _DispatchArity3 - def __call__(self, __arg1: _Marshallable, __arg2: _Marshallable, __arg3: _Marshallable) -> _Marshallable: pass
    _DispatchArity4 - def __call__(
        self, __arg1: _Marshallable, __arg2: _Marshallable, __arg3: _Marshallable, __arg4: _Marshallable
    ) -> _Marshallable: pass
    _DispatchArityN - def __call__(self, *args: _Marshallable) -> _Marshallable: pass
```

# Stats

Computed for the following repositories. Click to see the raw stats and callables.

## Projects with well-typed callables

+ [typeshed](./typeshed-callables.txt)
+ [mypy](./mypy-callables.txt) - well typed.
+ [spark](./spark-callables.txt) - pretty well typed. Very few `Callable`s with untyped parameters.
+ [tornado](./tornado-callables.txt) - 50-50 well-typed and loosely-typed Callables.

Combined stats:

```
Callables of arity 0: 459 (16.19%)
Callables of arity 1: 1124 (39.65%)
Callables of arity 2: 321 (11.32%)
Callables of arity 3: 81 (2.86%)
Callables of arity 4: 27 (0.95%)
Callables of arity 5: 16 (0.56%)
Callables with arbitrary parameters: 731 (25.78%)
Callback Protocols: 76 (2.68%)
```

## Projects with loosely-typed callables (mostly `f: Callable`)

+ [sphinx](./sphinx-callables.txt) - mostly `Callable`.
+ [jax](./jax-callables.txt) - mostly `Callable`.
+ [pytorch/ignite](./pytorch-ignite-callables.txt) - almost all just `Callable`.
+ [pytorch/vision](./vision-callables.txt) - mostly `Callable` or `Callable[..., nn.Module]`.
+ [pandas](./pandas-callables.txt)

Combined stats:

```
Callables of arity 0: 13 (1.73%)
Callables of arity 1: 62 (8.24%)
Callables of arity 2: 19 (2.53%)
Callables of arity 3: 9 (1.20%)
Callables of arity 4: 3 (0.40%)
Callables of arity 5: 0 (0.00%)
Callables with arbitrary parameters: 626 (83.24%)
Callback Protocols: 0 (0.00%)
```

Skipped:
+ scikit-learn - just 18 callable types.
+ sympathy - just 29 callable types.
+ pip - it has old-style comment hints, so my script doesn't work.
+ scipy - barely any callables.
+ black - same.

# How does it work?

This includes annotations from parameter types, return types, attribute types, etc.

It extracts `Callable[[int], str]` from within `List[Callable[[int], str]]`.

# Limitations

It doesn't:

+ Extract nested callables: `Callable[[Callable[[int], str]], str]`. We will only get the outer callable.

+ Extract types from `TypeVar` bounds.

+ Extract types from type aliases.

+ Recognize ParamSpec. It treats `Callable[P, R]` as a callable with undefined parameters.
