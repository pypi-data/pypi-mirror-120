__all__ = [
    "PrototypeError",
]

from types import (
    FunctionType,
)

from inspect import (
    Signature,
)


class PrototypeError(RuntimeError):

    """
    Prototype runtime error.
    Indicates incompatible function signature for given prototype.
    """

    __slots__ = (
        "function",
        "function_parameters",
        "prototype",
        "prototype_parameters",
    )

    __module__ = "prototypes"

    def __init__(
        self,
        function: FunctionType,
        function_signature: Signature,
        prototype: FunctionType,
        prototype_signature: Signature,
    ) -> None:
        self.function = function
        self.function_signature = function_signature
        self.prototype = prototype
        self.prototype_signature = prototype_signature

        message = [
            "Incompatible function implementation for given prototype",
            "",
            "Function:",
            f"def {function.__name__}{function_signature!s} @ {function.__qualname__}",
            "",
            "Prototype:",
            f"def {prototype.__name__}{prototype_signature!s} @ {prototype.__qualname__}",
        ]

        super().__init__("\n".join(message))
