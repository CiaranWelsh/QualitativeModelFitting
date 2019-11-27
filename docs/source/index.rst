.. QualitativeModelFitting documentation master file, created by
   sphinx-quickstart on Wed Nov 27 10:35:33 2019.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

QualitativeModelFitting
=======================

`QualitativeModelFitting` (`qmf`) is a package designed for validating a model
against arbitrary observations. The concept stems from that of unit testing in
software development. Using `qmf`, each part of a model
is tested by statements derived from literature or in house data. These statements
are encoded as a `qmf` input string which is used together with an
`antimony string <https://tellurium.readthedocs.io/en/latest/antimony.html>`_
as input to the :py:class:`qualitative_model_fitting.Runner` class.

Click below for more information on usage.

.. toctree::
   :maxdepth: 1

   qmf_string.rst
   runner.rst


This is the first version of `qmf` and there are a number of planned features
that are not yet supported. In no particular order, these are:

.. todo::

   - Build in full profile type analysis using a machine learning classification model. This would allow for profiles to be compared agaist (e.g.) a hyperbolic, transient or sigmoidal curve.
   - Implement a cache system for performance improvements
   - Implement the 'between' operator for implementing a rule that a component should be between x and y.
   - Implement the 'almost' operator for floating point comparisons
   - Implement the 'start' and 'end' operators for time intervals to abstract the need to always remember the end point of a simulation
   - Allow for assigning variables to collections so we can list species that have the same rules
   - Build in loops so we can do bulk validations
   - Build the steady state block
   - Build a dose response block
   - Build the sensitivity block
   - Build a plot block
