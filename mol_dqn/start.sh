#!/bin/bash

cd ./workspace/molecule_generation/mol_dqn
poetry install
export PYTHONPATH=/workspace/molecule_generation:/workspace/molecule_generation/mol_dqn:$PYTHONPATH
poetry shell
cp optimizers.py $(poetry env info --path | head -1)/lib/python3.10/site-packages/tf_slim/layers/optimizers.py 
