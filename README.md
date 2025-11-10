# EDS_NER_CARDIOCCC

This repository contains the code used to train and benchmark a **Named Entity Recognition (NER)** model on the **CardioCCC** dataset.
CardioCCC is a collection of **cardiology clinical case reports** used for **domain adaptation**. Clinical case reports are a textual genre in medicine that describe a patient’s medical history, symptoms, diagnosis, and treatment in detail.

The model implementation is based on **[EDS-NLP](https://github.com/aphp/edsnlp)**, a library developed by the **data science team of the Greater Paris University Hospitals (AP-HP)** for clinical natural language processing.

---

## CardioCCC Dataset

The **CardioCCC** dataset consists of **508 cardiology clinical case reports**, split into:

* **258 documents** for development (training/validation)
* **250 documents** for testing

It has been **annotated with diseases, symptoms, medications, and procedures**.

## Requirements

All dependencies are managed with **[uv](https://docs.astral.sh/uv/)**, a fast Python package and environment manager.

1. **Install uv** (if not already available):

   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

2. **Clone the repository**:

   ```bash
   git clone https://github.com/Aremaki/eds_ner_cardioccc.git
   cd eds_ner_cardioccc
   ```

3. **Create and sync a virtual environment**:

   ```bash
   uv sync --no-install-project
   ```

4. **Activate the environment**:

   ```bash
   source .venv/bin/activate
   ```

## Quickstart

### 1. Download base models from Hugging Face

```bash
bash download_models.sh
```

### 2. Train and run inference on CardioCCC

```bash
sbatch scripts/run.slurm
```

The `scripts/run.slurm` file contains the SLURM submission commands for cluster execution.
You can modify the configuration path, GPU resources, or training parameters as needed.

## Project Structure

```
eds_ner_cardioccc/
├── configs/                # Example YAML config files
├── data/                   # Dataset root (not included)
├── models/                 # Saved and downloaded model checkpoints
├── scripts/                # SLURM and helper scripts
├── pyproject.toml          # Dependencies and metadata
└── README.md
```

## Citation

If you use this code, the **CardioCCC dataset**, or any **EDS-NLP** components in your work, please cite both:

* The **CardioCCC dataset**, developed by **Life science team** at the **Barcelona Supercomputing Center (BSC)**.
* The **EDS-NLP** library, developed by the **data science team of the Greater Paris University Hospitals (AP-HP)**.

Please ensure both teams are properly acknowledged in any publication or derivative work.

## License

This repository is released under the **MIT License**.
See the `LICENSE` file for details.