#### 1. Overview
This tool loads text from an Excel golden dataset and a CSV of user search queries, generates embeddings, exports TensorFlow Projector-compatible TSV files, and produces a local 2D scatter plot preview.

#### 2. Setup
```bash
pip install -r requirements.txt
# For local embeddings:
pip install sentence-transformers
# For UMAP (optional):
pip install umap-learn
```

#### 3. Configuration
All configuration is in `config.py`.

- Change `EMBEDDER` via environment variable `EMBEDDER`:
  - `mock` (default)
  - `sentence_transformer`
  - `azure_openai`

- Azure OpenAI environment variables:
```bash
export AZURE_OPENAI_ENDPOINT="https://your-resource.openai.azure.com/"
export AZURE_OPENAI_API_KEY="your-key"
export AZURE_OPENAI_DEPLOYMENT="text-embedding-ada-002"
```

- Switch `REDUCTION_METHOD` between PCA and UMAP:
  - `REDUCTION_METHOD=pca` (default)
  - `REDUCTION_METHOD=umap` (requires `pip install umap-learn`)

#### 4. Running the script
```bash
python main.py
```

#### 5. Loading into TensorFlow Projector (step-by-step with screenshots placeholders)
```
Step 1: Open https://projector.tensorflow.org/ in Chrome or Firefox
Step 2: Click the "Load" button in the top-left panel
Step 3: Under "Load a TSV file of vectors", click "Choose file"
        → Select output/vectors.tsv
Step 4: Under "Load a TSV file of metadata", click "Choose file"
        → Select output/metadata.tsv
Step 5: Click the "Color by" dropdown and choose:
        - "category"  → see HR vs Travel vs IT clusters
        - "use_case"  → see UC-01 through UC-08 clusters
        - "type"      → see document vs keyword separation
Step 6: Use T-SNE or UMAP in the left panel for better cluster separation than PCA
```

#### 6. Switching to real embeddings later
Change `EMBEDDER = "mock"` to `"sentence_transformer"` in config.py and re-run.

#### 7. Adding new data sources
Create a new file in `loaders/`, implement a `load()` function that returns `list[dict]` with the same keys as the existing loaders, and add a call in `main.py`.

