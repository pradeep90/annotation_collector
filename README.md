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

# Stats

Computed for the following repositories. Click to see the raw stats and callables.

## Projects with well-typed callables

+ [typeshed](./data/typeshed-callables.txt)
+ [mypy](./data/mypy-non-typeshed-callables.txt) - well typed. **Note**: I'm excluding Mypy's internal copy of typeshed.
+ [spark](./data/spark-callables.txt) - pretty well typed. Very few `Callable`s with untyped parameters.
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
Callables with 0 parameters: 13 (1.73%)
Callables with 1 parameters: 62 (8.24%)
Callables with 2 parameters: 19 (2.53%)
Callables with 3 parameters: 9 (1.20%)
Callables with 4 parameters: 3 (0.40%)
Callables with 5 parameters: 0 (0.00%)
Callables with arbitrary parameters: 626 (83.24%)
Callback Protocols: 0 (0.00%)
```

Skipped:
+ scikit-learn - just 18 callable types.
+ sympathy - just 29 callable types.
+ pip - it has old-style comment hints, so my script doesn't work.
+ scipy - barely any callables.
+ black - same.

## Projects with No Types

Let's look at how callbacks are called in untyped Python code. (Click to see the individual functions.)

+ [django](./data/django-callback-parameters.txt): 75 functions with callback parameters (excluding calls to `cls` in `classmethod`s).
  + Callback is called with positional arguments: 44.0% (33/75)
  + Callback is called with `*args, **kwargs`: 37.3% (28/75)
  + Callback is called with `*args`: 2.7% (2/75)
  + Callback is called with `**kwargs`: 6.7% (5/75)
  + Callback is called with a named argument: 4.0% (3/75)
  + Miscellaneous: 1.3% (1/75)

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
  + Callback is called with positional arguments: 53.7% (58/108)
  + Callback is called with `*args, **kwargs`: 37.0% (40/108)
  + Callback is called with `*args`: 1.9% (2/108)
  + Callback is called with `**kwargs`: 2.8% (3/108)
  + Callback is called with a named argument: 0.9% (1/108)

    - `serialize` takes a class, not a real callback. The type would be `Type[Serializer]`, not a `Callable`.

		```
		def serialize(
				objects: Union[Any, Sequence[Any]],
				user: Optional[Any] = None,
				serializer: Optional[Any] = None,
				**kwargs: Any,
			) -> Any: ...
				serializer(o, attrs=attrs.get(o, {}), user=user, **kwargs)
		```

+ [tensorflow](./data/tensorflow-callback-parameters.txt): 1311 functions with callback parameters (excluding 113 calls to `cls` in `classmethod`s). I sampled around 113 functions.

  + Callback is called with positional arguments: 63.7% (72/113)
  + Callback is called with `*args, **kwargs`: 14.2% (16/113)
  + Callback is called with `*args`: 1.8% (2/113)
  + Callback is called with `**kwargs`: 10.6% (12/113)
  + Callback is called with a named argument: 8.0% (9/113)

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

## Callback parameters in Typed Projects

+ [mypy](./data/mypy-callback-parameters.txt): 66 functions with callback parameters (excluding 4 calls to `cls` in `classmethod`s).

  + Callback is called with positional arguments: 86.4% (57/66)
  + Callback is called with `*args, **kwargs`: 6.1% (4/66)
  + Callback is called with `*args`: 3.0% (2/66)
  + Callback is called with `**kwargs`: 0.0% (0/66)
  + Callback is called with a named argument: 4.5% (3/66)

    These were basically the same `fail` callback:

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
