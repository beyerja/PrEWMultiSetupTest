## Python-based analysis code

The Python code contained in `py` can be used to analyse the output from the multi-setup test.

Concrete tests to run are place in the `py/Results` directory.

### Framework basics

The `MultiResultReader` in the `IO` folder reads the different setups.
By default, it uses (all combinations of) the setups given in `Setups/DefaultSetups.py`.

The covariance matrix for a given setup is calculated from the result values that the fit lands on (see `Analysis/CovMatrixCalc.py`).

