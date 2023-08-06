"""Enums about endpoints"""

from taktile_types.enums.common import ExtendedEnum


class EndpointKinds(ExtendedEnum):
    """EndpointKinds.
    Different kinds of endpoints taktile-components supports
    """

    GENERIC = "generic"
    TYPED = "typed"
    ARROW = "arrow"
    PROFILED = "profiled"


class ProfileKinds(ExtendedEnum):
    """ProfileKinds.
    Different profile kinds supported by taktile-profiling
    """

    BINARY = "binary"
    REGRESSION = "regression"
