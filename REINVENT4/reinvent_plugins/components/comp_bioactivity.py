"""Compute bioactivity score with LGBM"""

__all__ = ["MIC"]

from .component_results import ComponentResults
from .add_tag import add_tag
from typing import List

import pickle
import numpy as np
import pandas as pd
import lightgbm
from rdkit import Chem
from rdkit.DataStructs.cDataStructs import ConvertToNumpyArray

@add_tag("__parameters")
@dataclass
class Parameters:

    smiles_list: List[str]

@add_tag("__component")
class MIC:
    def check_bioactivity(mol):
        model = pickle.load(open('lgbm_model.sav', 'rb'))
        fp = get_fingerprint(mol)
        mic = model.predict([fp])
        
        return mic[0]