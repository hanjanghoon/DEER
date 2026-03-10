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

| Model | Request Fulfillment | Analytic Soundness | Structural Coherence | Format & Style | Information Integrity | Information Sufficiency | Ethics | Mean |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| **`General LLMs`** |||||||||
| `Qwen3-235B Fast` | 4.51 | 5.02 | 6.09 | 7.49 | 1.24 | 4.20 | 7.19 | 5.11 |
| `Gemini 2.5 Flash Fast` | 4.64 | 5.33 | 6.55 | 7.85 | 1.30 | 3.99 | 7.52 | 5.31 |
| `Claude Opus 4.5 Fast` | 4.94 | 5.48 | 6.54 | 7.99 | 2.29 | 4.50 | 7.78 | 5.65 |
| `GPT-5 Fast` | 4.11 | 4.75 | 5.84 | 7.21 | 1.05 | 3.13 | 7.30 | 4.77 |
| **`LLMs + Reasoning`** |||||||||
| `Qwen3-235B + Reasoning` | 5.00 | 5.33 | 6.64 | 7.88 | 1.12 | 3.90 | 7.38 | 5.32 |
| `Gemini 2.5 Pro + Reasoning` | 4.88 | 5.81 | 6.99 | 8.09 | 2.23 | 4.40 | 7.73 | 5.73 |
| `Claude Opus 4.5 + Reasoning` | 4.96 | 5.48 | 6.68 | 8.10 | 2.27 | 4.22 | 7.73 | 5.63 |
| `GPT-5 + Reasoning` | **5.57** | **6.18** | **7.00** | 8.06 | 2.11 | 4.16 | _8.08_ | 5.88 |
| **`LLMs + Reasoning + WebSearch`** |||||||||
| `Qwen3-235B + Reasoning + WebSearch` | 4.05 | 4.34 | 5.68 | 6.83 | 5.22 | 5.45 | 7.06 | 5.52 |
| `Claude Opus 4.5 + Reasoning + WebSearch` | 4.52 | 5.13 | 5.99 | 7.41 | _7.03_ | _7.62_ | 7.37 | 6.44 |
| `GPT-5 + Reasoning + WebSearch` | **5.57** | _6.08_ | 6.97 | **8.15** | 5.63 | 6.17 | **8.11** | **6.67** |
| **`Deep Research`** |||||||||
| `WebThinker (Li et al., 2025b)` | 4.11 | 4.64 | 5.51 | 7.35 | 6.21 | 6.40 | 7.13 | 5.91 |
| `Qwen3-235B Deep Research` | 4.13 | 4.69 | 4.85 | 7.06 | 6.55 | **7.90** | 7.43 | 6.09 |
| `Gemini 2.5 Pro Deep Research` | 4.71 | 5.37 | 6.25 | 7.59 | 6.01 | 7.61 | 7.39 | 6.42 |
| `Claude Opus 4.5 Deep Research` | 4.53 | 5.22 | 5.69 | 7.22 | 6.04 | 5.66 | 7.57 | 5.99 |
| `OpenAI Deep Research` | 4.67 | 5.29 | 6.28 | 7.66 | **7.14** | 6.89 | 7.48 | 6.49 |

---

## License

* Code: MIT
* Data: CC BY-NC 4.0 (Non-commercial use only)
