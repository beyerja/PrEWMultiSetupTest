# PrEWMultiSetupTest - Testing a large number of setups with PrEW

Script to perform a `PrEW` fit using the `PrEWUtils` library.

## Installation

0. Make sure you installed `PrEW` and `PrEWUtils` (preferably in a directory next to this one).
1. Make sure your software is up-to-date (ROOT, gcc, cmake, ...) *or* load using macro (only on NAF):
 ```sh
 cd macros && source load_env.sh && cd ..
 ```
2. Compile the code:
 ```sh
 cd macros && chmod u+x compile.sh && ./compile.sh && cd ..
 ```
 
### After changing the source code

... simply recompile it using the `macros/compile.sh` macro.

## Running

The code can be easily run after compilation:
```sh
cd bin && ./PrEWMultiSetupTest && cd ..
```
This will produce output files in the `output` directory.
It is a plain text file that stores some information about the results of the fits


### Running it on the BIRD cluster

The executable can also be run on the BIRD cluster using the HTCondor scheduler.

```sh
cd macros && ./run_on_cluster.sh [--cpus=n_cpus] && cd ..
```
With the ```--cpus=n_cpus``` the number of cpus used on the BIRD cluster can be set.

### The source code

The main configuration and source code is in `source/main.cpp`.
Details on the configurations are in the `.h` files in the `source/Definitions` directory.

It uses the necessary `PrEW` classes and the interfaces provided by `PrEWUtils` to be as clear as manageable.
(This may not always have worked out.)

For open questions please consult the `PrEW` and `PrEWUtils` source code or open an issue on the GitHub page.

## Analysis

For the python code that interprets the output of the `PrEW` runs, please see the `analysis` folder and the readme therein.