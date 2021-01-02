from functools import wraps
from inspect import signature


def partializable(fn):
    @wraps(fn)
    def arg_partializer(*fixable_parameters):
        def partialized_fn(dynamic_arg):
            return fn(dynamic_arg, *fixable_parameters)

        return partialized_fn

    # Override signature
    sig = signature(fn)
    sig = sig.replace(parameters=tuple(sig.parameters.values())[1:])
    arg_partializer.__signature__ = sig

    return arg_partializer
