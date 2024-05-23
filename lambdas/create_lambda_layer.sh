#!/bin/bash

# Get the Python version and shift the arguments
python_version=$1
shift

# Generate a random name for the virtual environment
venv_name=$(uuidgen)

# Create a new directory for the layer
mkdir lambda_layer
cd lambda_layer

# Create a Python virtual environment and activate it
python$python_version -m venv $venv_name
source $venv_name/bin/activate

# Install the packages
for pkg in "$@"
do
    pip install "$pkg"
done

# Deactivate the virtual environment
deactivate

# Prepare the layer for deployment
mkdir python
mv $venv_name/lib/python$python_version/site-packages/* python/
zip -r ../lambda_layer.zip python

# Delete the virtual environment and lambda_layer directory
rm -rf $venv_name
cd ..
rm -rf lambda_layer