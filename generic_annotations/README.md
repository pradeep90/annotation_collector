# Generic Types

To collect stats on generic types like `List`, `Dict`, etc., run the following outside the `annotation_collector` directory:

```
$ python -m annotation_collector.generic_annotations.generic_annotation /Users/pradeepkumars/Programs/spark/python/pyspark/context.pyi

`Union` annotations: 0


`Callable` annotations: 1
    Callable[[Iterable[T]], Iterable[U]]

`Optional` annotations: 40
    Optional[AccumulatorParam[T]]
    Optional[BaseException]
    Optional[Dict[str, str]]
    Optional[Dict[str, str]]
    Optional[Dict[str, str]]
    Optional[Dict[str, str]]
    Optional[Dict[str, str]]
    Optional[JavaGateway]
    Optional[JavaObject]
    Optional[List[int]]
    Optional[List[str]]
    Optional[SparkConf]
    Optional[SparkConf]
    Optional[TracebackType]
    Optional[Type[BaseException]]
    Optional[int]
    Optional[int]
    Optional[int]
    Optional[int]
    Optional[int]
    Optional[int]
    Optional[int]
    Optional[int]
    Optional[str]
    Optional[str]
    Optional[str]
    Optional[str]
    Optional[str]
    Optional[str]
    Optional[str]
    Optional[str]
    Optional[str]
    Optional[str]
    Optional[str]
    Optional[str]
    Optional[str]
    Optional[str]
    Optional[str]
    Optional[str]
    Optional[str]

`List` annotations: 3
    List[U]
    List[int]
    List[str]

`Dict` annotations: 6
    Dict[str, ResourceInformation]
    Dict[str, str]
    Dict[str, str]
    Dict[str, str]
    Dict[str, str]
    Dict[str, str]

`Set` annotations: 0


`Tuple` annotations: 7
    Tuple[T, U]
    Tuple[T, U]
    Tuple[T, U]
    Tuple[T, U]
    Tuple[T, U]
    Tuple[str, bytes]
    Tuple[str, str]

`Iterable` annotations: 4
    Iterable[RDD[T]]
    Iterable[T]
    Iterable[U]
    Iterable[str]
```
