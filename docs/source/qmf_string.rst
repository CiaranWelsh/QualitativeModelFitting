====================
The qmf input string
====================

`qmf` defines its own syntax for retrieving user input. In `qmf` this
is known as an `input` or `observation` string. An input string is
divided into blocks and each block has a type. For now, there are only
`timeseries` blocks and an `observation` block. You can have as many
`timeseries` blocks as you like, but there must only be one `observation`
block.

The timeseries block
======================

This is where you define the timeseries that you can use in later comparisons. Each
timeseries block you specify requires a separate time series simulation with its own
independent variables (i.e. starting conditions) and therefore the more you have,
the longer the programs execurion time.

The syntax of a `timeseries` block looks like this:

    .. code-block:: C
        :linenos:

        timeseries name {component1=amount1, component2=amount2, ...} 0, 100, 101

Spaces are ignored, so:

    .. code-block:: C
        :linenos:

     timeseries name {
        component1=amount1,
        component2=amount2,
        ...} start, stop, num


is syntactically equivalent and sometimes preferred, when a `timeseries` has lots of
independent variables. The `name` argument is a handle for this timeseries and is used later
within the observation block to refer to it. The final three arguments are `start`, `stop` and `num` which are
the `start` and `stop` points of numerical integration and `num` how many equally spaced time points
to have between them.

Examples
--------

    .. code-block:: C
        :linenos:

        timeseries SInactive {S=0} 0, 50, 51
        timeseries SActive {S=1} 0, 50, 51

These two timeseries encode the two situations where a hypothetical stimulus `S` is on in `SActive`
or off in `SInactive`. Both timeseries will be integrated from `0` to `50` using a wrapper
around `tellurium <https://tellurium.readthedocs.io/en/latest/>`_ and `roadrunner <https://sys-bio.github.io/roadrunner/python_docs/index.html>`_
packages.

The Observation Block
=====================

As the name suggests, this is where we define our observations. Observations can be one of several types.
The simplest look like the following:

    .. code-block:: C
        :linenos:

        name: statement

where

    - `name`: The name of your observation. Arbitrary.
    - `statement`: A binary comparison instruction

The `statement` has the following form:

    - `clause operator clause`

Where:

    - `operator`: One of the comparison operators (`>`, `<`, `>=`, `<=`, `==`, `!=`).
    - `clause`: an entity for comparison (see below)

Clause
======

Constants and expressions
-------------------------
A `clause`, in analogy to part of a sentence, can have one of several forms. At its simplest,
a clause can be a constant value or a numerical expression.

    .. code-block:: C
        :linenos:

        0
        5*10
        4 + 4*9

The usual precedent rules in math are applied correctly.

Model variables
---------------

More often, we want a particular model variable at a particular time:

    .. code-block:: C
        :linenos:

        model_component[timeseries_name]@t=x

Which will resolve to a single number representing the amount of `model_component`
in condition `timeseries_name` at time `x`. For example we could do:

    .. code-block:: C
        :linenos:

        A[SActive]@t=0

Which returns that scalar number. Sometimes we do not want a scalar but the amount
of a variable between two time points.

    .. code-block:: C
        :linenos:

        model_component[timeseries_name]@t=(x, y)

Which be resolved to a vector of numbers representing the amount of `model_component`
in condition `timeseries_name` between the time ranges of `x` and `y`. Since
a vector cannot directly be compared with a scalar, to use a range of values in a comparison
we need to use a function (see below).

Functions
=========

Functions can take two forms:

    - `Type1`: Those which tell the `Runner` how to make a comparison between scalar and vector
    - `Type2`: Those which convert vectors to scalars prior to making the comparison.

These two function types have a slightly different syntax:

Type1:

    .. code-block:: C
        :linenos:

        name: function(clause operator clause)

Type2:

    .. code-block:: C
        :linenos:

        name: function(clause) operator clause

.. note::

    The `Type1` function type takes as argument the whole `clause operator clause` statement
    while the `Type2` function takes only a clause as argument.

.. note::

    Point 2 here assumes that the first `clause` is the time interval clause and the
    second is a scalar.

.. note::

    Comparing a vector with another vector (i.e. element wise) is not yet supported.

Type1 functions
---------------

There are two `Type1` functions: `any` and `all` which are analogous to Python's and `numpy`
`any` and `all` functions. If you use the `all` function when comparing a vector and
scalar, the function will return `True` if all of the elements in the vector meet the condition
set by the operator and the other clause. The `any` function on the other hand will
return True if any of the elements in the vector meet the conditions set by the operator and the other
clause.

Type1 Function Examples
-----------------------

All of `A` in the `SActive` timeseries between `0` and `50` are `greater than`
the amount of `A` in the `SInactive` timeseries at time 25.

    .. code-block:: C
        :linenos:

        all(A[SActive]@t=(0, 50) >  A[SInactive]@t=25)

If `A` in the `SActive` timeseries at time `0` are `greater then` any of
`B` between the bounaries of `13` and `19`, return `True` else `False`

    .. code-block:: C
        :linenos:

        any(A[SActive]@t=0 >  B[SActive]@t=(13, 19))

Type2 functions
---------------

Type 2 functions currently include:

    - mean
    - min
    - max

Which are self explainatory in what they do.

Type 2 function examples
------------------------

The **mean**, **maximum** or **minimum** (respectively) of `A` in the `SActive` time series between time `0` and `50` is `greater than`
the amount of `A` in the `SInactive` time series at time `0`

    .. code-block:: C
        :linenos:

        mean(A[SActive]@t=(0, 50)) > A[SInactive]@t=0
        max(A[SActive]@t=(0, 50)) > A[SInactive]@t=0
        min(A[SActive]@t=(0, 50)) > A[SInactive]@t=0













