#!/bin/bash

apt-get install python3-libnvinfer
echo "# Adding module mol_dqn into PYTHONPATH" >> ~/.bashrc
echo "export PYTHONPATH=\$PYTHONPATH:/workspace/molecule_generation:/workspace/molecule_generation/mol_dqn" >> ~/.bashrc
cd /workspace/molecule_generation/mol_dqn
git config --global user.email "peterzhilyaev@gmail.com"
git config --global user.name "Peter Zhilyaev"
poetry install --no-root 
cp optimizers.py $(poetry env info --path | head -1)/lib/python3.10/site-packages/tf_slim/layers/optimizers.py 
poetry shell
