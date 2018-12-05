#!/usr/bin/env bash
rm ./build/ -rf
rm ./dist/* -rf
python setup.py sdist build
python setup.py bdist_wheel --universal

