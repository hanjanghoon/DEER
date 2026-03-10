# DEER

DEER is a benchmark for evaluating deep research agents on expert report generation.

📄 Paper: [https://arxiv.org/abs/2512.17776](https://arxiv.org/abs/2512.17776)

<p align="center">
  <img src="img.png" width="100%"/>
</p>

DEER provides a systematic and interpretable evaluation framework for expert-level long-form research reports:

* Expert-defined hierarchical taxonomy (7 dimensions, 25 sub-dimensions)
* 101 fixed rubric items for structured LLM-based scoring
* Task-specific Expert Evaluation Guidance
* Report-wide claim verification with implicit citation back-tracking

DEER enables fine-grained, domain-aware diagnostics beyond aggregate scoring.

---

## Installation

```bash
git clone https://github.com/hanjanghoon/DEER.git
cd DEER
conda env create -f deer.yml
conda activate deer
```

---

## Environment Setup

Create a `.env` file in the root directory and add your API keys:

```
OPENAI_API_KEY=your_openai_key_here
JINA_API_KEY=your_jina_key_here
```

---

## Data

Each domain folder inside `data/` contains a `query.md`.

Generate a report that answers the query and place the report file in the same directory.

---

## Run

```bash
bash run_domain_all.sh
```

---

## Experimental Results

| Model | Req. Comp. | Evid. Valid. | Struct. Cons. | Narr. Style | Info. Int. | Info. Suff. | Ethics | Mean |
|------|------------|------------|------------|------------|------------|------------|------------|------|
| **General LLM** |||||||||
| qwen3-235b-fast | 6.10 | 6.59 | 9.04 | 8.66 | 3.30 | 4.40 | 8.58 | 6.67 |
| gemini-2.5-pro-fast | 6.08 | 7.02 | 9.29 | 8.87 | 2.92 | 4.43 | 8.89 | 6.79 |
| claude_opus4.1_fast | 6.04 | 6.47 | 8.96 | 8.95 | 4.76 | 4.81 | 8.78 | 6.97 |
| gpt5_fast | 5.61 | 6.63 | 8.80 | 8.46 | 2.18 | 3.45 | 8.82 | 6.28 |
| **LLM + Thinking** |||||||||
| qwen3-235b-think | 6.77 | 6.53 | 9.32 | 8.92 | 3.28 | 4.39 | 8.75 | 6.85 |
| gemini-2.5-pro-think | 6.41 | 7.66 | 9.55 | 9.20 | 3.86 | 4.97 | 9.37 | 7.20 |
| claude_opus4.1_think | 5.93 | 6.41 | 9.05 | 9.04 | 4.72 | 5.12 | 8.99 | 7.04 |
| gpt5_think | 7.69 | **8.37** | **9.57** | **9.32** | 4.19 | 5.42 | 9.37 | 7.70 |
| **LLM + Thinking + Search** |||||||||
| qwen3-235b-think_search | 6.43 | 6.31 | 9.07 | 8.82 | 3.60 | 4.49 | 8.44 | 6.74 |
| gemini-2.5-pro-think_search | 6.61 | 7.58 | 9.50 | 9.11 | 4.62 | 5.02 | 8.97 | 7.34 |
| claude_opus4.1_think_search | 6.03 | 6.62 | 9.04 | 9.03 | 5.17 | 4.80 | 8.85 | 7.08 |
| gpt5_think_search | **7.88** | 8.26 | 9.39 | 9.04 | 6.42 | 6.44 | **9.38** | **8.12** |
| **Deep Research** |||||||||
| webthinker | 5.27 | 5.76 | 8.48 | 8.62 | 7.57 | 6.92 | 8.68 | 7.33 |
| qwen3-235b-deep | 4.95 | 6.00 | 7.28 | 8.31 | 7.13 | **8.29** | 8.66 | 7.23 |
| gemini-2.5-pro-deep | 6.08 | 6.81 | 8.81 | 8.78 | 7.13 | 7.87 | 8.62 | 7.73 |
| claude_opus4.1_deep | 6.60 | 6.91 | 8.90 | 8.85 | 6.79 | 7.66 | 8.75 | 7.78 |
| gpt5_deep | 6.26 | 7.11 | 9.20 | 8.93 | **7.64** | 7.13 | 8.99 | 7.89 |

---

## License

* Code: MIT
* Data: CC BY-NC 4.0 (Non-commercial use only)
