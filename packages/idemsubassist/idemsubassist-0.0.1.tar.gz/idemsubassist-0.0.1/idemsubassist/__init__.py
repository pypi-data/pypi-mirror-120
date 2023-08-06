from functools import wraps

def entry_exit_log(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        func_fqn = f'{func.__module__}.{func.__name__}'
        hub = args[0]
        hub.log.debug(f'Entering {func_fqn}')
        r = func(*args, **kwargs)
        hub.log.debug(f'Exiting {func_fqn}')
        return r
    return wrapper

def assert_kw_param(param_key):
    def the_decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if param_key not in kwargs:
                raise KeyError(f'{param_key}') # TODO: Make this error message better
            # setattr(func, param_key, kwargs[param_key])
            return func(*args, **kwargs)
        return wrapper
    return the_decorator

def assert_kw_param_in_ctx(param_key):
    def the_decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if len(args) < 2 or param_key not in args[1].kwargs:
                raise KeyError(f'{param_key}') # TODO: Make this error message better
            # setattr(func, param_key, args[1].kwargs[param_key])
            return func(*args, **kwargs)
        return wrapper
    return the_decorator