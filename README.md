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
$ ./callable_annotations.py ~/Programs/typeshed/stdlib/concurrent/
Callables of arity 0: 2
Callables of arity 1: 15
Callables of arity 2: 5
Callables of arity 3: 1
Callables of arity 4: 0
Callables of arity 5: 0
Callables with arbitrary parameters: 2

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
```

## Details

This includes annotations from parameter types, return types, attribute types, etc.

It extracts `Callable[[int], str]` from within `List[Callable[[int], str]]`.

## Limitations

It doesn't:

+ Extract nested callables: `Callable[[Callable[[int], str]], str]`. We will only get the outer callable.

+ Extract types from `TypeVar` bounds.

+ Extract types from type aliases.

+ Recognize ParamSpec. It treats `Callable[P, R]` as a callable with undefined parameters.
