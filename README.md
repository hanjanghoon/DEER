# DEER

DEER is a benchmark for evaluating deep research agents on expert report generation.

📄 Paper: [https://arxiv.org/abs/2512.17776](https://arxiv.org/abs/2512.17776)

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

Create a `.env` file in the root directory and add your API key:

```
OPENAI_API_KEY=your_api_key_here
```

---

## Data

For each query inside the `data/` folder, place the report you want to evaluate in the same directory.

---

## Run

```bash
bash run_domain_all.sh
```

---

## License

* Code: MIT
* Data: CC BY-NC 4.0 (Non-commercial use only)
