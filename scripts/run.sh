#!/bin/bash
#SBATCH --job-name=ner
#SBATCH -t 48:00:00
#SBATCH --gres=gpu:v100:1
#SBATCH --cpus-per-task=2
#SBATCH --mem=40000
#SBATCH --partition gpuV100
#SBATCH --output=logs/slurm-%j-stdout.log
#SBATCH --error=logs/slurm-%j-stderr.log
#SBATCH --container-image /scratch/images/sparkhadoop.sqsh  --container-mounts=/export/home/$USER:/export/home/$USER,/data/scratch/$USER:/data/scratch/$USER --container-mount-home --container-writable
source $HOME/.user_conda/miniconda/etc/profile.d/conda.sh # appel de ce script
cd "/export/home/cse200093/Adam/eds_ner_cardioccc"
source "/export/home/cse200093/Adam/eds_ner_cardioccc/.venv/bin/activate"
conda deactivate

echo -----------------
echo TRAINING
echo -----------------
start_time="$(date -u +%s)"

python -m edsnlp.train --config configs/config_v1.yml

end_time="$(date -u +%s)"
elapsed="$(($end_time-$start_time))"
echo -----------------
echo "Total of $elapsed seconds elapsed for TRAINING"
echo -----------------

echo -----------------
echo INFERENCE
echo -----------------
start_time="$(date -u +%s)"

python -u scripts/infer.py \
  --input_path "data/cardioccc/test" \
  --output_path "data/cardioccc/pred" \
  --model_path "models/ner_cardioccc_run1" \
  --batch_size "10000 words" \
  --show_progress

end_time="$(date -u +%s)"
elapsed="$(($end_time-$start_time))"
echo -----------------
echo "Total of $elapsed seconds elapsed for INFERENCE"
echo -----------------

# echo --NER_FINISHED---

# echo ---------------
