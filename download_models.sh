#!/bin/bash
set -e  # Exit immediately if a command fails

# ============================
# Configuration
# ============================

# Directory where models will be stored
MODEL_DIR="/data/scratch/cse200093/word-embedding"

# List of models to download (add as many as you want)
MODELS=(
  "dccuchile/bert-base-spanish-wwm-cased"
  "PlanTL-GOB-ES/bsc-bio-ehr-es"
  "DT4H/CardioBERTa.es"
  "FacebookAI/xlm-roberta-large"
  "almanach/camembertav2-base"
)

# ============================
# Setup
# ============================

# Create target directory if it doesn't exist
mkdir -p "$MODEL_DIR"

# ============================
# Download each model
# ============================

for model in "${MODELS[@]}"; do
  model_name=$(basename "$model")
  echo "⏬ Downloading model: $model"
  huggingface-cli download "$model" --local-dir "$MODEL_DIR/$model_name" --local-dir-use-symlinks False
  echo "✅ Saved to: $MODEL_DIR/$model_name"
  echo
done

echo "🎉 All models downloaded successfully!"
