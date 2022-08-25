Template for create de Docker with Ubuntu image.

## Install
conda create -V ./venv/ python==3.5
conda activate ./venv/
pip install -r requirements.txt

## Execute


Este con el modelo pequeño para que veas que funciona:

./falsefriends.py -v classify  resources/sepulveda2011_training.txt resources/sepulveda2011_testing.txt resources/pre_process_sample_es_vectors.bin resources/pre_process_sample_pt_vectors.bin resources/big/trans_es_100_pt_100.npz

curl -X POST http://0.0.0.0:8866/class_falsefriends -H 'Content-Type: application/json' -d '{"type":"structuredText", "texts":[{"content":"barata"},{"content":"barata"}]}'



## Use

## Known Issues:
