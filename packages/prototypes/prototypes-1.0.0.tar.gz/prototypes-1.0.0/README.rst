Prototypes
----------

|py3.6| |py3.7| |py3.8| |py3.9| |py3.10|

.. |py3.6| image:: https://img.shields.io/badge/python-3.6-blue.svg
.. |py3.7| image:: https://img.shields.io/badge/python-3.7-blue.svg
.. |py3.8| image:: https://img.shields.io/badge/python-3.8-blue.svg
.. |py3.9| image:: https://img.shields.io/badge/python-3.9-blue.svg
.. |py3.10| image:: https://img.shields.io/badge/python-3.10-blue.svg

Summary
=======

Prototypes allow you to define signatures for your functions and
verify those signatures during both static type checking and runtime.

Installation
============

::

    $ pip install prototypes

Requirements
============

- `typing-extensions`_ >= 3.10 when using Python < 3.10

.. _`typing-extensions`: https://pypi.org/project/typing-extensions

Basic usage
===========

To validate your function against prototype, decorate your function with
the ``prototype`` decorator and pass the prototype function as a parameter.

.. code-block:: python

    from prototypes import prototype

    def add(x: int, y: int) -> int:
        ...

    @prototype(add)
    def custom_add(x: int, y: int) -> int:
        return x + y

Static type checking is fully supported thanks to usage of both ``typing.TypeVar``
(`PEP 484`_) and ``typing.ParamSpec`` (`PEP 612`_) under the hood.

.. code-block:: python

    from prototypes import prototype

    def add(x: int, y: int) -> int:
        ...

    # This will report type error by static type checkers like `mypy` in the future
    @prototype(add)
    def compute() -> None:
        pass

.. _`PEP 484`: https://www.python.org/dev/peps/pep-0484
.. _`PEP 612`: https://www.python.org/dev/peps/pep-0612

Advanced usage
==============

Prototype functions does not have to be empty. They can be regular functions
that already contain specific implementation. The prototype function act
more like a signature template for the function, rather than an empty shell
to be filled with the implementation.

.. code-block:: python

    from prototypes import prototype

    def add(x: int, y: int) -> int:
        return x + y

    @prototype(add)
    def custom_add(x: int, y: int) -> int:
        ...
        return add(x, y)

By default, the ``prototype`` decorator verifies the signatures during runtime. Since
decorators are executed during the function definition, this validation is performed
right away, even if function is never called.

.. code-block:: python

    >>> from prototypes import prototype
    >>>
    >>> def add(x: int, y: int) -> int: ...
    ...
    >>> @prototype(add)
    ... def compute() -> None:
    ...     pass
    ...
    Traceback (most recent call last):
        ...
    prototypes.PrototypeError: Incompatible function implementation for given prototype

    Function:
    def compute() -> None @ compute

    Prototype:
    def add(x: int, y: int) -> int @ add

However, since closures (inner functions) are defined on function execution,
using ``prototype`` decorator in the closure will have no effect until the outer
function is called.

.. code-block:: python

    >>> from prototypes import prototype
    >>>
    >>> def add(x: int, y: int) -> int: ...
    ...
    >>> def func() -> None:
    ...     @prototype(add)
    ...     def compute() -> None:
    ...         ...
    ...
    >>> # No exception is raised at that point
    >>> func()
    Traceback (most recent call last):
        ...
    prototypes.PrototypeError: Incompatible function implementation for given prototype

    Function:
    def compute() -> None @ func.<locals>.compute

    Prototype:
    def add(x: int, y: int) -> int @ add

The runtime validation can be turned off when static type checking is performed
to increase the code performance during runtime.

.. code-block:: python

    >>> from prototypes import prototype
    >>>
    >>> def add(x: int, y: int) -> int: ...
    ...
    >>> @prototype(add, runtime=False)
    ... def compute() -> None:
    ...     pass
    ...
    >>> # No exception is raised during runtime

Bugs/Requests
-------------

Please use the `GitHub issue tracker`_ to submit bugs or request features.

.. _`GitHub issue tracker`: https://github.com/kprzybyla/prototypes/issues

License
-------

Copyright Krzysztof Przybyła, 2021.

Distributed under the terms of the `MIT`_ license.

.. _`MIT`: https://github.com/kprzybyla/prototypes/blob/master/LICENSE
