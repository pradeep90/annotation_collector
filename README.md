# Annotation Collector

# Overall Stats in Typeshed

See [here](./generic_annotations/data/typeshed-generic-annotations.txt) for the raw types.

| Annotation name | Frequency in Typeshed |
| -               | -:                    |
| Optional        | 10237                 |
| Tuple           | 2296                  |
| Union           | 2162                  |
| List            | 1937                  |
| Callable        | 1314                  |
| Dict            | 1286                  |
| Iterable        | 1261                  |
| Set             | 159                   |

As of October 2021, `Callable` is the most frequently used special form that still requires an import. Others like `List` have a builtin equivalent like `list`. `Optional[int]` is very frequently used but is technically expressible as `int | None`. That may still be cumbersome, though.

# Callable Annotations

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
Callables with 0 parameters: 2
Callables with 1 parameters: 15
Callables with 2 parameters: 5
Callables with 3 parameters: 1
Callables with 4 parameters: 0
Callables with 5 parameters: 0
Callables with arbitrary parameters: 2
Callback Protocols: 6

$ ./callable_annotations.py ~/Programs/typeshed/stdlib/concurrent/ --show-callables
Callables with 0 parameters: 2
    Callable[[], None]
    Callable[[], None]
Callables with 1 parameters: 15
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
Callables with 2 parameters: 5
    Callable[[Optional[str], Tuple[_Marshallable, ...]], Union[Fault, Tuple[_Marshallable, ...]]]
    Callable[[Optional[str], Tuple[_Marshallable, ...]], Union[Fault, Tuple[_Marshallable, ...]]]
    Callable[[Unmarshaller, str], None]
    Callable[[str, Tuple[_Marshallable, ...]], _Marshallable]
    Callable[[str, Tuple[_Marshallable, ...]], _Marshallable]
Callables with 3 parameters: 1
    Callable[[Marshaller, Any, Callable[[str], Any]], None]
Callables with 4 parameters: 0
Callables with 5 parameters: 0
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

## Calls to Callback Parameters

To see functions that call one of their parameters, use `--show-callback-parameters`:

```
$ ./callable_annotations.py --show-callback-parameters /Users/pradeepkumars/Programs/github-clones/django/django/views/decorators/http.py
Callables with 0 parameters: 0
Callables with 1 parameters: 0
Callables with 2 parameters: 0
Callables with 3 parameters: 0
Callables with 4 parameters: 0
Callables with 5 parameters: 0
Callables with arbitrary parameters: 0
Callback Protocols: 0
Functions with callback parameters: 3
    def condition(etag_func=None, last_modified_func=None): ...
    	etag_func(request, *args, **kwargs)
    	last_modified_func(request, *args, **kwargs)

    def decorator(func): ...
    	func(request, *args, **kwargs)

    def decorator(func): ...
    	func(request, *args, **kwargs)
```

# Stats

Computed for the following repositories. Click to see the raw stats and callables.

## Projects with well-typed callables

+ [typeshed](./data/typeshed-callables.txt)

	```
	Callables with 0 parameters: 223 (16.56%)
	Callables with 1 parameters: 521 (38.68%)
	Callables with 2 parameters: 137 (10.17%)
	Callables with 3 parameters: 43 (3.19%)
	Callables with 4 parameters: 13 (0.97%)
	Callables with 5 parameters: 9 (0.67%)
	Callables with arbitrary parameters: 364 (27.02%)
	Callback Protocols: 37 (2.75%)
	```

+ [mypy](./data/mypy-non-typeshed-callables.txt) - well typed. **Note**: I'm excluding Mypy's internal copy of typeshed.
+ [spark](./data/spark-callables.txt) - pretty well typed. Very few `Callable`s with untyped parameters.

	```
	Callables with 0 parameters: 4 (2.04%)
	Callables with 1 parameters: 107 (54.59%)
	Callables with 2 parameters: 49 (25.00%)
	Callables with 3 parameters: 6 (3.06%)
	Callables with 4 parameters: 0 (0.00%)
	Callables with 5 parameters: 0 (0.00%)
	Callables with arbitrary parameters: 26 (13.27%)
	Callback Protocols: 4 (2.04%)
	```

+ [tornado](./data/tornado-callables.txt) - 50-50 well-typed and loosely-typed Callables.

Combined stats:

```
Callables with 0 parameters: 258 (14.86%)
Callables with 1 parameters: 712 (41.01%)
Callables with 2 parameters: 210 (12.10%)
Callables with 3 parameters: 49 (2.82%)
Callables with 4 parameters: 15 (0.86%)
Callables with 5 parameters: 8 (0.46%)
Callables with arbitrary parameters: 443 (25.52%)
Callback Protocols: 41 (2.36%)
```

## Projects with loosely-typed callables (mostly `f: Callable`)

+ [sphinx](./data/sphinx-callables.txt) - mostly `Callable`.
+ [jax](./data/jax-callables.txt) - mostly `Callable`.
+ [pytorch/ignite](./data/pytorch-ignite-callables.txt) - almost all just `Callable`.
+ [pytorch/vision](./data/vision-callables.txt) - mostly `Callable` or `Callable[..., nn.Module]`.
+ [pandas](./data/pandas-callables.txt)

Combined stats:

```
Callables with 0 parameters: 13 (1.76%)
Callables with 1 parameters: 62 (8.39%)
Callables with 2 parameters: 19 (2.57%)
Callables with 3 parameters: 9 (1.22%)
Callables with 4 parameters: 3 (0.41%)
Callables with 5 parameters: 0 (0.00%)
Callables with arbitrary parameters: 633 (85.66%)
Callback Protocols: 0 (0.00%)
```

Skipped:
+ scikit-learn - just 18 callable types.
+ sympathy - just 29 callable types.
+ pip - it has old-style comment hints, so my script doesn't work.
+ scipy - barely any callables.
+ black - same.

## Typed Projects - overall stats

+ Callables with 0 parameters: 286 (11.32%)
+ Callables with 1 parameters: 796 (31.51%)
+ Callables with 2 parameters: 235 (9.30%)
+ Callables with 3 parameters: 59 (2.34%)
+ Callables with 4 parameters: 18 (0.71%)
+ Callables with 5 parameters: 9 (0.36%)
+ Callables with arbitrary parameters: 1082 (42.83%)
+ Callback Protocols: 41 (1.62%)

## Projects with No Types

Let's look at how callbacks are called in untyped Python code. (Click to see the individual functions.)

+ [django](./data/django-callback-parameters.txt): 88 functions with callback parameters.

  + Callback is called with positional arguments: 36.4% (32/88)
  + Callback is called with `*args, **kwargs`: 35.2% (31/88)
  + Callback is called with `*args`: 2.3% (2/88)
  + Callback is called with `**kwargs`: 5.7% (5/88)
  + Callback is called with a named argument or default value: 1.1% (1/88)
  + Class type: 19.3% (17/88)

    - `_generate_altered_foo_together` - this is called with a class. Not a real "callback" as such. The type would just be `operation: Type[AlterUniqueTogether] | Type[AlterIndexTogether]`.

		```
		./db/migrations/autodetector.py:1145:        self._generate_altered_foo_together(operations.AlterUniqueTogether)
		./db/migrations/autodetector.py:1148:        self._generate_altered_foo_together(operations.AlterIndexTogether)
		```

	- `_path`

		```
		./urls/conf.py:
		path = partial(_path, Pattern=RoutePattern)
		re_path = partial(_path, Pattern=RegexPattern)
		```

	- `method_set_order` - same.

		```
		./db/models/base.py:2133:def method_set_order(self, ordered_obj, id_list, using=None):
				  ordered_obj(pk=pk, _order=order)
		```

+ [sentry](./data/sentry-callback-parameters.txt): 108 functions with callback parameters (excluding calls to `cls` in `classmethod`s).

  + Callback is called with positional arguments: 39.6% (57/144)
  + Callback is called with `*args, **kwargs`: 29.9% (43/144)
  + Callback is called with `*args`: 4.2% (6/144)
  + Callback is called with `**kwargs`: 5.6% (8/144)
  + Callback is called with a named argument or default value: 0.7% (1/144)
  + Class type: 20.1% (29/144)

+ [tensorflow](./data/tensorflow-callback-parameters.txt): 1011 functions with callback parameters. I filtered out test functions.

  + Callback is called with positional arguments: 55.7% (519/932)
  + Callback is called with `*args, **kwargs`: 15.2% (142/932)
  + Callback is called with `*args`: 7.7% (72/932)
  + Callback is called with `**kwargs`: 13.7% (128/932)
  + Callback is called with a named argument or default value: 5.5% (51/932)
  + Class type: 5.9% (55/932)

    - Most of these were just calls to classes, like in the previous projects.
	- Tests did some dynamic things.
	- There were a few legitimate uses of named arguments.

		```python
		def _tf_gradients_forward_over_back_hvp(model, images, labels, vector): ...
			model(images, training=True)


		./debug/cli/analyzer_cli.py:1365:
		def _dfs_from_node(self,
						   lines,
						   attr_segs,
						   node_name,
						   tracker,
						   max_depth,
						   depth,
						   unfinished,
						   include_control=False,
						   show_op_type=False,
						   command_template=None): ...
			tracker(node_name, is_control=False)
			tracker(node_name, is_control=True)


		def _convert_sparse_segment(pfor_input, _, op_func): ...
			op_func(data, indices, segment_ids, num_segments=num_segments)
		```

+ Summary for django, sentry, and tensorflow:

Weighted by function counts (biased towards tensorflow, which is very large):

  + Callback is called with positional arguments: 50.7% (608/1199)
  + Callback is called with `*args, **kwargs`: 18.0% (216/1199)
  + Callback is called with `*args`: 6.7% (80/1199)
  + Callback is called with `**kwargs`: 11.8% (141/1199)
  + Callback is called with a named argument or default value: 4.4% (53/1199)
  + Class type: 8.4% (101/1199)

Average of percentages:

  + Callback is called with positional arguments: 43.9%
  + Callback is called with `*args, **kwargs`: 26.6%
  + Callback is called with `*args`: 4.7%
  + Callback is called with `**kwargs`: 8.3%
  + Callback is called with a named argument or default value: 2.4%
  + Class type: 15.1%

## Callback parameters in Typed Projects

+ [mypy](./data/mypy-non-typeshed-callables.txt): 77 functions with callback parameters.

  + Callback is called with positional arguments: 80.5% (62/77)
  + Callback is called with `*args, **kwargs`: 5.2% (4/77)
  + Callback is called with `*args`: 1.3% (1/77)
  + Callback is called with `**kwargs`: 0.0% (0/77)
  + Callback is called with a named argument or default value: 5.2% (4/77)
  + Class type: 3.9% (3/77)

    The named arguments were basically for the same `fail` callback:

		```python
		# Mypyc doesn't support callback protocols yet.
		MsgCallback = Callable[[str, Context, DefaultNamedArg(Optional[ErrorCode], 'code')], None]

		def get_omitted_any(disallow_any: bool, fail: MsgCallback, note: MsgCallback,
							orig_type: Type, python_version: Tuple[int, int],
							fullname: Optional[str] = None,
							unexpanded_type: Optional[Type] = None) -> AnyType:
			fail(message_registry.IMPLICIT_GENERIC_ANY_BUILTIN.format(alternative), typ,
				 code=codes.TYPE_ARG)
		```

+ [spark](./data/spark-callables.txt): 115 functions with callback parameters.

  + Callback is called with positional arguments: 56.5% (65/115)
  + Callback is called with `*args, **kwargs`: 7.8% (9/115)
  + Callback is called with `*args`: 11.3% (13/115)
  + Callback is called with `**kwargs`: 7.0% (8/115)
  + Callback is called with a named argument or default value: 2.6% (3/115)
  + Class type: 13.9% (16/115)
  + Too dynamic: 0.9% (1/115)

+ [sphinx](./data/sphinx-callables.txt): 169 functions with callback parameters. (This may be a bit unrepresentative because one file - sphinx/domains/cpp.py - has a lot of similar-looking positional callables.)

  + Callback is called with positional arguments: 83.4% (141/169)
  + Callback is called with `*args, **kwargs`: 8.9% (15/169)
  + Callback is called with `*args`: 1.8% (3/169)
  + Callback is called with `**kwargs`: 0.0% (0/169)
  + Callback is called with a named argument or default value: 2.4% (4/169)
  + Class type: 3.6% (6/169)
  + Too dynamic: 0.0% (0/169)

+ [jax](./data/jax-callables.txt): 275 functions with callback parameters. I'm ignoring test functions.

  + Callback is called with positional arguments: 63.3% (174/275)
  + Callback is called with `*args, **kwargs`: 10.5% (29/275)
  + Callback is called with `*args`: 18.2% (50/275)
  + Callback is called with `**kwargs`: 1.8% (5/275)
  + Callback is called with a named argument or default value: 2.5% (7/275)
  + Class type: 3.6% (10/275)

+ Summary for mypy, spark, sphinx, and jax:

  + Callback is called with positional arguments: 69.9% (442/632)
  + Callback is called with `*args, **kwargs`: 9.0% (57/632)
  + Callback is called with `*args`: 10.6% (67/632)
  + Callback is called with `**kwargs`: 2.1% (13/632)
  + Callback is called with a named argument or default value: 2.8% (18/632)
  + Class type: 5.5% (35/632)

# Function Calls

## Calls to PyTorch `register_buffer`

To see the initial argument passed to the Pytorch method `self.register_buffer`:

```
$ python3 function_call.py /Users/pradeepkumars/Programs/github-clones/pytorch/torch/utils/ --verbose
PROGRESS: Parsed 20/103 files...
PROGRESS: Parsed 40/103 files...
PROGRESS: Parsed 60/103 files...
PROGRESS: Parsed 80/103 files...
PROGRESS: Parsed 100/103 files...
Register buffer calls: 12
dense_module.weight.to_mkldnn(dtype)
dense_module.bias.to_mkldnn()
torch.zeros([dense_module.weight.size(0)], dtype=torch.float).to_mkldnn()
dense_module.bias.to_mkldnn()
torch.zeros([dense_module.weight.size(0)], dtype=torch.float).to_mkldnn()
dense_module.weight.to_mkldnn(dtype)
torch._C._nn.mkldnn_reorder_conv2d_weight(
    dense_module.weight.to_mkldnn(dtype),
    self.padding,
    self.stride,
    self.dilation,
    self.groups)
torch._C._nn.mkldnn_reorder_conv3d_weight(
    dense_module.weight.to_mkldnn(dtype),
    self.padding,
    self.stride,
    self.dilation,
    self.groups)
dense_module.weight.to_mkldnn()
dense_module.bias.to_mkldnn()
dense_module.running_mean.to_mkldnn()
dense_module.running_var.to_mkldnn()
```

## Calls that have a Literal Argument

```
./function_call.py /Users/pradeepkumars/Programs/github-clones/pytorch/torch/utils/mkldnn.py --verbose
...

Calls with literals: 12
self.register_buffer('weight', dense_module.weight.to_mkldnn(dtype))
self.register_buffer('bias', dense_module.bias.to_mkldnn())
self.register_buffer(
    'bias',
    torch.zeros([dense_module.weight.size(0)], dtype=torch.float).to_mkldnn())
self.register_buffer('bias', dense_module.bias.to_mkldnn())
self.register_buffer(
    'bias',
    torch.zeros([dense_module.weight.size(0)], dtype=torch.float).to_mkldnn())
self.register_buffer('weight', dense_module.weight.to_mkldnn(dtype))
self.register_buffer('weight', torch._C._nn.mkldnn_reorder_conv2d_weight(
    dense_module.weight.to_mkldnn(dtype),
    self.padding,
    self.stride,
    self.dilation,
    self.groups))
self.register_buffer('weight', torch._C._nn.mkldnn_reorder_conv3d_weight(
    dense_module.weight.to_mkldnn(dtype),
    self.padding,
    self.stride,
    self.dilation,
    self.groups))
self.register_buffer('weight', dense_module.weight.to_mkldnn())
self.register_buffer('bias', dense_module.bias.to_mkldnn())
self.register_buffer('running_mean', dense_module.running_mean.to_mkldnn())
self.register_buffer('running_var', dense_module.running_var.to_mkldnn())
```

# Methods returning `self` or `cls`

If you have a method that returns an object of the same type, the way to write type annotations is as below:

```python
T = TypeVar("T", bound="Base")

class Base:
    @classmethod
    def from_config(cls: Type[T], config: Dict[str, str]) -> T:
        return cls(**config)

class Child(Base):
    def child_method(self) -> None:
	    print("Child!")
```

Note that we have to use `Type[T]` as the type of `cls` and have a return type `T`. Otherwise, someone constructing a `Child` object using `from_config` will get an object of type `Base`, not `Child`.

```python
# If we used `Base` as the return type of `from_config`.

class Base:
    @classmethod
    def from_config(cls: Type[T], config: Dict[str, str]) -> Base:
        return cls(**config)

class Child(Base):
    def child_method(self) -> None:
	    print("Child!")

def main() -> None:
	child = Child.from_config(config) # => actually of type Base
	child.child_method() # error: No method `child_method` in class Base.
```

For more details, see [my presentation](https://www.youtube.com/watch?v=ld9rwCvGdhc&t=3260s) from the Typing Summit at PyCon 2021 ([slides](https://drive.google.com/file/d/1x-qoDVY_OvLpIV1EwT7m3vm4HrgubHPG/view)).

## Methods where the `self` or `cls` parameter is annotated

Run the script as below:

```
python self_annotation.py /Users/pradeepkumars/Programs/typeshed/stdlib/distutils/version.pyi /Users/pradeepkumars/Programs/typeshed/stdlib/ctypes/__init__.pyi --verbose

Methods with `self` or `cls` annotations: 17
    def __lt__(self: _T, other: Union[_T, str]) -> bool: ...

    def __le__(self: _T, other: Union[_T, str]) -> bool: ...

    def __gt__(self: _T, other: Union[_T, str]) -> bool: ...

    def __ge__(self: _T, other: Union[_T, str]) -> bool: ...

    @abstractmethod
    def parse(self: _T, vstring: str) -> _T: ...

    @abstractmethod
    def _cmp(self: _T, other: Union[_T, str]) -> bool: ...

    def parse(self: _T, vstring: str) -> _T: ...

    def _cmp(self: _T, other: Union[_T, str]) -> bool: ...

    def parse(self: _T, vstring: str) -> _T: ...

    def _cmp(self: _T, other: Union[_T, str]) -> bool: ...

    # By default mypy complains about the following two methods, because strictly speaking cls
    # might not be a Type[_CT]. However this can never actually happen, because the only class that
    # uses _CDataMeta as its metaclass is _CData. So it's safe to ignore the errors here.
    def __mul__(cls: Type[_CT], other: int) -> Type[Array[_CT]]: ...  # type: ignore

    def __rmul__(cls: Type[_CT], other: int) -> Type[Array[_CT]]: ...  # type: ignore

    @classmethod
    def from_buffer(cls: Type[_CT], source: _WritableBuffer, offset: int = ...) -> _CT: ...

    @classmethod
    def from_buffer_copy(cls: Type[_CT], source: _ReadOnlyBuffer, offset: int = ...) -> _CT: ...

    @classmethod
    def from_address(cls: Type[_CT], address: int) -> _CT: ...

    @classmethod
    def from_param(cls: Type[_CT], obj: Any) -> _UnionT[_CT, _CArgObject]: ...

    @classmethod
    def in_dll(cls: Type[_CT], library: CDLL, name: str) -> _CT: ...
```

## Methods that return `self` or `cls(...)` in their body

Run the script as below:

```
python self_annotation.py /Users/pradeepkumars/Programs/github-clones/tensorflow/tensorflow/python/autograph/operators/variables.py /Users/pradeepkumars/Programs/github-clones/tensorflow/tensorflow/python/keras/layers/recurrent.py --verbose

Methods returning `self` or `cls(...)`: 5
    def __getitem__(self, i):
        return self

    @classmethod
    def from_config(cls, config, custom_objects=None):
        from tensorflow.python.keras.layers import deserialize as deserialize_layer  # pylint: disable=g-import-not-at-top
        cells = []
        for cell_config in config.pop('cells'):
            cells.append(
                deserialize_layer(cell_config, custom_objects=custom_objects))
        return cls(cells, **config)

    @classmethod
    def from_config(cls, config):
        if 'implementation' in config:
            config.pop('implementation')
        return cls(**config)

    @classmethod
    def from_config(cls, config):
        if 'implementation' in config and config['implementation'] == 0:
            config['implementation'] = 1
        return cls(**config)

    @classmethod
    def from_config(cls, config):
        if 'implementation' in config and config['implementation'] == 0:
            config['implementation'] = 1
        return cls(**config)
```

## Stats

### Typed Projects

Here are stats for common OSS projects. Click the project name to see the raw methods. There are two columns:

+ Method signatures with `self` or `cls` annotation: These are methods that have signatures like `def foo(cls: Type[T]) -> T: ...`.
+ Method bodies returning `self` or `cls(...)`: These are usually methods that return `self` or `cls(<some arguments>)` in their body. See the previous section for examples.

| Project                                                       | Method signatures with `self` or `cls` annotation | Method bodies returning `self` or `cls(...)` | Notes                                                                                   |
| -                                                             | -:                                                | -:                                           | -                                                                                       |
| [typeshed](./data/typeshed-methods-with-self-annotations.txt) | 523                                               | 0                                            |                                                                                         |
| [mypy](./data/mypy-non-typeshed-methods-returning-self.txt)   | 2                                                 | 8                                            |                                                                                         |
| [tornado](./data/tornado-methods-returning-self.txt)          | 1                                                 | 4                                            | Filtered out methods with `self: Any`.                                                  |
| [spark](./data/spark-methods-returning-self.txt)              | 57                                                | 127                                          | Filtered out methods that needed the exact generic parameters `self: RDD[Tuple[K, V]]`. |
| [sphinx](./data/sphinx-methods-returning-self.txt)            | 0                                                 | 11                                           |                                                                                         |
| [jax](./data/jax-methods-returning-self.txt)                  | 0                                                 | 28                                           |                                                                                         |
| [ignite](./data/ignite-methods-returning-self.txt)            | 0                                                 | 9                                            |                                                                                         |
| [vision](./data/vision-methods-returning-self.txt)            | 0                                                 | 2                                            |                                                                                         |
| [pandas](./data/pandas-methods-returning-self.txt)            | 228                                               | 126                                          |                                                                                         |
| [scipy](./data/scipy-methods-returning-self.txt)              | 0                                                 | 33                                           |                                                                                         |
| [black](./data/black-methods-returning-self.txt)              | 3                                                 | 2                                            |                                                                                         |
| [tensorflow](./data/tensorflow-methods-returning-self.txt)    | 2                                                 | 200                                          |                                                                                         |
| Total                                                         | 816                                               | 550                                          |                                                                                         |

### Script commands

```
# Ignore Mypy's copy of typeshed.
time python self_annotation.py /Users/pradeepkumars/Programs/mypy/misc /Users/pradeepkumars/Programs/mypy/mypyc /Users/pradeepkumars/Programs/mypy/scripts /Users/pradeepkumars/Programs/mypy/mypy/dmypy /Users/pradeepkumars/Programs/mypy/mypy/plugins /Users/pradeepkumars/Programs/mypy/mypy/server /Users/pradeepkumars/Programs/mypy/mypy/test /Users/pradeepkumars/Programs/mypy/mypy/xml /Users/pradeepkumars/Programs/mypy/mypy/*.py --verbose > data/mypy-non-typeshed-methods-returning-self.txt

time python self_annotation.py /Users/pradeepkumars/Programs/tornado/ --verbose > data/tornado-methods-returning-self.txt

for project in spark sphinx jax ignite vision pandas scipy black; do echo $project; time python self_annotation.py /Users/pradeepkumars/Programs/$project --verbose > data/$project-methods-returning-self.txt; echo ''; done
```

# How does it work?

This includes annotations from parameter types, return types, attribute types, etc.

It extracts `Callable[[int], str]` from within `List[Callable[[int], str]]`.

# Limitations

It doesn't:

+ Extract nested callables: `Callable[[Callable[[int], str]], str]`. We will only get the outer callable.

+ Extract types from `TypeVar` bounds.

+ Extract types from type aliases.

+ Recognize ParamSpec. It treats `Callable[P, R]` as a callable with undefined parameters.

+ Get callback parameters that have been assigned to a local variable or a class attribute before being called.

# Wish list of features

+ Save the state after analyzing all files. That will let us investigate the data some more and get other stats of interest without rerunning the whole analysis.
