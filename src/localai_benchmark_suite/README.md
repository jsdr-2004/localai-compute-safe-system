# LocalAI Benchmark Suite

## Setup

Install requirements:

```bash
pip install -r requirements.txt
```

Install Ollama and pull models:

```bash
ollama pull llama3.2:1b
ollama pull llama3.2:3b
ollama pull qwen2.5:3b
ollama pull mistral:7b
```

Run benchmark:

```bash
python benchmark.py
```

Results will be saved to:

```text
data/templates/benchmark_results.csv
```

## Notes

The first version estimates tokens using text chunks. Later versions should use exact tokenizer metadata.
