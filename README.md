#PythonSigma

The goal of this project is to be a Discrete Event Simulation engine that uses Sigma .mod files as input

##Using
An example of a simulation is included in `example.py`. 

Initial parameters are passed as a list of values.

Data files are passed as a dictionary with the file name as the key and a list of values from the file as the value.

The constructor for a `Simulation` object takes the mod file name, runtime, initial values, and dictionary of data files as parameters. The random seed is passed to `run_simulation`.

The output is returned as an `Output` object by `run_simulation`.

##Limitations

This project currently implements a subset of Sigma functions (RND, sequential DISK, PUT, GET, CLK). Other functions will be added over time.
