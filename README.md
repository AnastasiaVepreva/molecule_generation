# molecule_generation
Run this command:
python main.py --exp_root ../experiments --alert_collections ../alert_collections.csv --fragments ../zinc_crem.json --receptor ../4j1r.pdbqt --vina_program ./env/qvina02 --starting_smile "c1([*:1])c([*:2])ccc([*:3])c1" --fragmentation crem --num_sub_proc 12 --n_conf 1 --exhaustiveness 1 --save_freq 50 --epochs 200 --commands "train,sample" --reward_version soft --box_center "37.36,32.49,30.85" --box_size "10.186,11.792,8.916" --seed 150 --name freedpp --objectives "DockingScore" --weights "1.0"
