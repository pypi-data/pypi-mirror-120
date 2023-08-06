pyftdc
==============

[![Gitter][gitter-badge]][gitter-link]

|      CI              | status |
|----------------------|--------|
| conda.recipe         | [![Conda Actions Status][actions-conda-badge]][actions-conda-link] |
| pip builds           | [![Pip Actions Status][actions-pip-badge]][actions-pip-link] |



A MongoDB FTDC files parser written in C++ that provides Python bindings using [pybind11](https://github.com/pybind/pybind11) and scikit-build.



[gitter-badge]:            https://badges.gitter.im/pybind/Lobby.svg
[gitter-link]:             https://gitter.im/pybind/Lobby
[actions-badge]:           https://github.com/pybind/pyftdc/workflows/Tests/badge.svg
[actions-conda-link]:      https://github.com/pybind/pyftdc/actions?query=workflow%3AConda
[actions-conda-badge]:     https://github.com/pybind/pyftdc/workflows/Conda/badge.svg
[actions-pip-link]:        https://github.com/pybind/pyftdc/actions?query=workflow%3APip
[actions-pip-badge]:       https://github.com/pybind/pyftdc/workflows/Pip/badge.svg
[actions-wheels-link]:     https://github.com/pybind/pyftdc/actions?query=workflow%3AWheels
[actions-wheels-badge]:    https://github.com/pybind/pyftdc/workflows/Wheels/badge.svg

Installation
------------

**Building on Unix (Linux, macOS)**

 You will need to install packages. Please see https://github.com/jorge-imperial/mongo_ftdc/blob/main/docs/build.md
 
  
 1. clone this repository and change to the top level directory.
      ```
      git clone git@github.com:jorge-imperial/mongo_ftdc.git 
      cd mongo_ftdc
      ```
      
 2. Install Python libraries to build binaries. Create a virtual environment to make your life easier.
      ```
      python3 -m venv venv
      source venv/bin/activate
      pip install pybind11 cmake ninja wheel scikit-build
      ```
 3. Build local wheel 
      ```
       python setup.py bdist_wheel
      ```
 4. Install locally using one of the following lines, depending on your target environment: 
     ```
      pip install dist/pyftdc-0.0.1-cp39-cp39-macosx_11_0_x86_64.whl
      
      pip install dist/pyftdc-0.0.1-cp38-cp38-linux_x86_64.whl
      
      pip install dist/pyftdc-0.0.1-cp39-cp39-macosx_11_0_arm64.whl
     ```

**Building on Windows**
  
  Not tested yet.

**Building C++ tests**

NB: To build and run C++ tests you might need to explicitly define the path to `pybind11Config.cmake`. This can be done running 

```
cd mongo_ftdc
PYBINDCMAKE=$(find `pwd` -name pybind11Config.cmake)
PYBIND11PATH=$(dirname $PYBINDCMAKE)
mkdir BUILD  ; cd BUILD
source ../venv/bin/activate
cmake -D pybind11_DIR=$PYBIND11PATH ..
make -j8
```

Remember to install all packages, as described here:  https://github.com/jorge-imperial/mongo_ftdc/blob/main/docs/build.md


License
-------

Apache V2

Test call
---------

```python
import pyftdc
# Create a parser object
p = pyftdc.FTDCParser()

# Parse a test directory
status = p.parse_dir('./tests/diagnostic.data_40')
if status == 0:
    print(f"Parsed sample data dir")
else:
    print(f"foo: status is {status}")

meta = p.metadata
print(meta[0])
print(f"metadata has {len(meta)} elements")

ts = p.timestamps
print(f"There are {len(ts)} timestamps")

metrics = p.metric_names
print(f"There are {len(metrics)} metrics")

# serverStatus.locks.Database.acquireCount.w
m = p.get_metric('serverStatus.metrics.document.deleted')
print(f"ChunkMetric values {m}")
n = p.get_metric('serverStatus.locks.Database.acquireCount.w')
print(f"Another metric  {n}")
```

[`cibuildwheel`]:          https://cibuildwheel.readthedocs.io
