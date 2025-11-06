# BSC_CardioCCC_NER

This repository contains the code used to train and benchmark a Named Entity Recognition (NER) model on the CardioCCC dataset. CardioCCC is a collection of cardiology clinical case reports used for domain adaptation. Clinical case reports are a type of textual genre in the field of medicine that describe a patient’s medical history, symptoms, diagnosis, and treatment in detail. The model implementation is based on EDS-NLP, a library developed by the data science team of the Greater Paris University Hospitals (AP‑HP).

## CardioCCC Dataset

A collection of cardiology clinical case reports (CardioCCC) is used for the domain adaptation part of the task. The dataset contains 508 documents, split in 258 for development and 250 for testing. It has been annotated with diseases and medications using the guidelines as the DisTEMIST and DrugTEMIST corpora. The medications part is released in three languages: Spanish, English and Italian.

## Key points
- Task: Clinical NER (BILOU supported).
- Language: Spanish, with medication data also in English and Italian.
- Data: CardioCCC — A collection of 508 cardiology clinical case reports (258 for development, 250 for testing). Annotated for diseases and medications.
- Model: implementations and model components adapted from EDS-NLP (AP‑HP data science team).

## Features
- Training and evaluation scripts.
- Preprocessing and dataset converters.
- Support for Hugging Face transformers and custom BiLSTM-CRF backends (EDS-NLP inspired components).
- Logging, checkpoints, and reproducible training configs.

## Requirements

The project dependencies are listed in the `pyproject.toml` file.

- Python >3.7.1
- EDS-NLP
- PyTorch

Install all dependencies with:
```
pip install .
```

## Quickstart

1. Prepare dataset
- Place CardioCCC files (tokenized + BIO labels or original notes) under `data/cardioccc/`.

2. Train
Example using a transformer backbone:
```
python scripts/train.py \
    --model_name_or_path bert-base-multilingual-cased \
    --dataset_path data/cardioccc \
    --output_dir outputs/run1 \
    --epochs 5 \
    --batch_size 16 \
    --lr 3e-5
```

3. Evaluate
```
python scripts/evaluate.py --model_path outputs/run1 --dataset_path data/cardioccc --split test
```

4. Inference
```
python scripts/infer.py --model_path outputs/run1 --input_file examples/sample_notes.txt --output_file predictions.json
```

## Data format
Preferred format: token-per-line with BIO labels and sentence separators (empty line). Example:
```
Paciente O
con O
insuficiencia B-DX
cardiaca I-DX
. O
```

Scripts in `src/preprocess/` convert between common formats (CoNLL, JSON, HF datasets).

## Project structure
- eds_ner_cardioccc/ — training, evaluation, inference, preprocessing code
- configs/ — example YAML config files
- data/ — dataset root (not included)
- outputs/ — training outputs and checkpoints
- requirements.txt
- README.md

## Reproducibility
- Seed is fixed by default; set `--seed` to change.
- Save best checkpoint by validation F1.

## Citation
If you use this code, the CardioCCC dataset, or EDS-NLP components in publications, please cite the CardioCCC dataset and the EDS-NLP library (credit to the AP‑HP data science team).

## License
This repository is provided under the MIT License. See LICENSE for details.

## Contributing
Open issues or submit pull requests. For major changes, open an issue first to discuss.
