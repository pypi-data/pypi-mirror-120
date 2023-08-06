import typing


def check_type(actual, definition):
    # Currently any type variable will be considered generic
    if type(definition) == typing.TypeVar:
        return True

    # Any allows any.
    if definition == typing.Any:
        return True

    try:
        actual_origin = actual.__origin__
    except AttributeError:
        actual_origin = actual
        actual_args = tuple()
    else:
        actual_args = typing.get_args(actual)

    try:
        definition_origin = definition.__origin__
    except AttributeError:
        definition_origin = definition
        definition_args = tuple()
    else:
        definition_args = typing.get_args(definition)

    try:
        # For the case where typing.Iterable is good for typing.List
        class_similarity = issubclass(actual_origin, definition_origin)
    except TypeError:
        class_similarity = actual_origin == definition_origin

    return (
        class_similarity
        and len(actual_args) >= len(definition_args)
        and all(
            check_type(actual_args[i], definition_args[i])
            for i in range(len(definition_args))
        )
    )
