import os, sys, pickle
import numpy as np
import pandas as pd
import tensorflow as tf
from rdkit import Chem
from rdkit.Chem import AllChem, QED, RDConfig, Lipinski, Descriptors
from rdkit.DataStructs.cDataStructs import ConvertToNumpyArray
import statistics
from rdkit import DataStructs
from rdkit.Chem import AllChem
import lightgbm
import xgboost

sys.path.append(os.path.join(RDConfig.RDContribDir, 'SA_Score'))
import sascorer

from RAscore.RAscore import RAscore_XGB

FILENAME = sys.argv[1]

def get_fingerprint(mol):
  """ Converts SMILES into Morgan fingerprint """
  fp_array = np.zeros((0,), dtype=np.int8)
  fp = AllChem.GetMorganFingerprintAsBitVect(mol, 2, nBits=256)
  ConvertToNumpyArray(fp, fp_array)
  return fp_array

def check_bioactivity(mol):
  """ Calculates predicted MIC """
  model = pickle.load(open('lgbm_model.sav', 'rb'))
  fp = get_fingerprint(mol)
  mic = model.predict([fp])
  return mic[0]

def check_qed(mol):
  """ Calculates QED-score """
  return QED.qed(mol)

def check_sascore(mol):
  """ Calculates SAScore """
  return sascorer.calculateScore(mol)

def check_rascore(mol):
  """ Calculates RAScore """
  ra_scorer = RAscore_XGB.RAScorerXGB()
  smiles = Chem.MolToSmiles(mol)
  return ra_scorer.predict(smiles)

tox_df = pd.read_csv('tox_alerts.txt', sep='\t')
def check_toxicophore(mol):
  """ Returns the number of toxicophore groups in a molecule """
  count = 0
  for smarts in tox_df.SMARTS.to_list():
    pattern = Chem.MolFromSmarts(smarts)
    if mol.HasSubstructMatch(pattern)==True:
      count += 1
  return count

def check_lipinski_ro5(mol):
  """ Checks Lipinski's rule of five for drig-like molecules """
  counter = 0
  counter += 1 if Chem.Lipinski.NumHDonors(mol) <= 5 else 0
  counter += 1 if Chem.Lipinski.NumHAcceptors(mol) <= 10 else 0
  counter += 1 if Chem.Descriptors.MolWt(mol) <= 500 else 0
  counter += 1 if Chem.Descriptors.MolLogP(mol) <= 5 else 0

  return counter >= 3

def check_lipinski_ro3(mol):
  """ Checks Lipinski's rule of three for lead-like molecules """
  counter = 0
  counter += 1 if Chem.Lipinski.NumHDonors(mol) <= 3 else 0
  counter += 1 if Chem.Lipinski.NumHAcceptors(mol) <= 3 else 0
  counter += 1 if Chem.Descriptors.MolWt(mol) <= 300 else 0
  counter += 1 if Chem.Descriptors.MolLogP(mol) <= 3 else 0

  return counter >= 3

df = pd.read_csv(FILENAME)
list_smi = df['smiles'].tolist()
fpgen = AllChem.GetRDKitFPGenerator()
fps = [fpgen.GetFingerprint(Chem.MolFromSmiles(x)) for x in list_smi]

def check_diversity(mol):
    fp = fpgen.GetFingerprint(mol)
    scores = DataStructs.BulkTanimotoSimilarity(fp, fps)
    
    return statistics.mean(scores)

df['mol'] = df.smiles.apply(Chem.MolFromSmiles)
df['bioactivity'] = df.mol.apply(check_bioactivity)
df['QED'] = df.mol.apply(check_qed)
df['sascore'] = df.mol.apply(check_sascore)
df['rascore'] = df.mol.apply(check_rascore)
df['lipinski_ro5'] = df.mol.apply(check_lipinski_ro5)
df['lipinski_ro3'] = df.mol.apply(check_lipinski_ro3)
df['tox_groups'] = df.mol.apply(check_toxicophore)
df['diversity'] = df.mol.apply(check_diversity)

df.drop(columns='mol', inplace=True)

df.to_csv(f'{FILENAME[:-4]}_result.csv', index=False)

