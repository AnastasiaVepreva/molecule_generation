#!/bin/bash
conda create --name reinvent4
pip install -r requirements-linux-64.lock
pip install --no-deps . 
