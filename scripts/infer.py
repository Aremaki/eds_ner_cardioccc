import logging
import time
from collections import defaultdict
from datetime import datetime

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
    batch_size: str = "32 docs",
    show_progress: bool = True,
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
    print(nlp)
    logging.info("Model loading done")

    print(f"Job started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    tic = time.time()

    # Read BRAT input
    docs = edsnlp.data.read_standoff(input_path)  # type: ignore

    # Apply the model lazily
    docs = docs.map_pipeline(nlp)

    # Configure multiprocessing with automatic resource detection
    docs = docs.set_processing(
        backend="multiprocessing",
        batch_size=batch_size,
        show_progress=show_progress,
        # You can set num_cpu_workers and num_gpu_workers here,
        # otherwise they are auto-detected
    )

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
        out_path = f"{output_path}/results_tsv/{label}.tsv"
        pd.DataFrame(rows).to_csv(out_path, sep="\t", index=False)

    edsnlp.data.write_standoff(  # type: ignore
        docs,
        f"{output_path}/results_brat",
        overwrite=True,
        span_getter=["*"],
    )
    print(
        f"NER Prediction is saved in BRAT format in the following folder: {output_path}"
    )
    tac = time.time()
    print(f"Processed {len(list(docs))} docs in {tac - tic} secondes")


if __name__ == "__main__":
    app()
