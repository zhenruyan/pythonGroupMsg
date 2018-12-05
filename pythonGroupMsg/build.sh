#!/usr/bin/env bash
cat ./nlib.py > lib.pyx
python ./setup.py build_ext  --inplace
mv ./pythonGroupMsg/lib.cpython-37m-x86_64-linux-gnu.so .
rm -rf ./pythonGroupMsg/
rm -rf ./build/