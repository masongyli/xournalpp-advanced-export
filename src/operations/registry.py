operation_registry = {}

def register_operation(name):
    def decorator(cls):
        operation_registry[name] = cls
        return cls
    return decorator

