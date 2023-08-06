def curry(function):
    def decorated(*args, **kwargs):
        return lambda: function(*args, **kwargs)

    return decorated
