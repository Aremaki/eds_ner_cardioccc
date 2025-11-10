import logging
import time
from collections import defaultdict
from datetime import datetime
from pathlib import Path

import confit
import edsnlp
import pandas as pd
from edsnlp.core.registries import registry

app = confit.Cli()


@app.command("infer", registry=registry)
def infer(
    *,
    input_path: str,
    output_path: str,
    model_path: str,
):
    """
    Run inference on a corpus of notes stored in BRAT format.

    Parameters
    ----------
    input_path : str
        Input BRAT path (e.g. s3://bucket/notes/ or hdfs path)
    output_path : str
        Output Parquet path (e.g. s3://bucket/note_nlp/ or hdfs path)
    model_path : str
        Model to load: local path, installed model package or EDS-NLP
        compatible Hub repo (e.g. 'AP-HP/eds-pseudo-public')
    batch_size : str
        Batch size expression (e.g. '32 docs', '8000 words')
    show_progress : bool
        Show progress bars
    """

    logging.info("Model loading started")
    nlp = edsnlp.load(f"{model_path}/model-last")
    # Do anything to the model here
    logging.info("Model loading done")

    print(f"Job started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    tic = time.time()

    # Read BRAT input
    docs = list(edsnlp.data.read_standoff(input_path))  # type: ignore

    # Apply the model
    docs = [nlp(doc) for doc in docs]

    def convert_ents_to_rows(doc):
        return [
            {
                "filename": doc._.note_id,
                "label": ent.label_,
                "start_span": ent.start_char,
                "end_span": ent.end_char,
                "text": ent.text,
            }
            for ent in doc.ents
        ]

    # Collect and convert after processing
    rows_by_label = defaultdict(list)

    for doc in docs:  # iterate over processed docs
        for ent in doc.ents:
            rows_by_label[ent.label_].append({
                "filename": doc._.note_id,
                "label": ent.label_,
                "start_span": ent.start_char,
                "end_span": ent.end_char,
                "text": ent.text,
            })

    # Write one CSV per label
    for label, rows in rows_by_label.items():
        out_dir = Path(output_path) / "results_tsv"
        out_dir.mkdir(parents=True, exist_ok=True)  # <-- ensure folder exists
        pd.DataFrame(rows).to_csv(out_dir / f"{label}.tsv", sep="\t", index=False)

    edsnlp.data.write_standoff(  # type: ignore
        docs,
        Path(output_path) / "results_brat",
        overwrite=True,
        span_getter=["*"],
    )
    print(
        f"NER Prediction is saved in BRAT format in the following folder: {output_path}"
    )
    tac = time.time()
    print(f"Processed {len(docs)} docs in {tac - tic} secondes")


if __name__ == "__main__":
    app()
