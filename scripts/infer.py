import logging
import time
from datetime import datetime

import confit
import edsnlp

app = confit.Cli()


@app.command("inference")
def infer(
    *,
    input_path: str,
    output_path: str,
    model_path: str,
    batch_size: str = "32 docs",
    show_progress: bool = False,
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
    nlp = edsnlp.load(model_path)
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

    edsnlp.data.write_standoff(  # type: ignore
        docs,
        output_path,
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
