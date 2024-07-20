## Will the Real Linda Please Stand up...to Large Language Models? Examining the Representativeness Heuristic in LLMs

This repository contains the code and data for the paper "Will the Real Linda Please Stand up...to Large Language Models? Examining the Representativeness Heuristic in LLMs" by [Pengda Wang](https://wpengda.github.io/), [Zilin Xiao](https://zilin.me/), [Hanjie Chen](https://hanjiechen.github.io/) and [Frederick L. Oswald](https://profiles.rice.edu/faculty/fred-oswald).

[[arxiv]](https://arxiv.org/pdf/2404.01461)

### Data

We release the first version of data in `test_cases_0320.jsonl` with the following schema:

```
{"test_case": "Suppose we know that the number of graduate students...", "type": "Base Rate Fallacy", "ground_truth": "[2] Social science and social work > [4] Engineering"}
```

We also release the evaluation toolkit in `eval_kit/eval_0219.py`. 

### Code

Check all `run_heuristic_*.py` files for running the LLM queries on different endpoints. 

### BibTex

If you use this code or data, it would be great if you could cite our paper:

```bibtex
@article{wang2024real,
  title   = {Will the Real Linda Please Stand up...to Large Language Models? Examining the Representativeness Heuristic in LLMs},
  author  = {Pengda Wang and Zilin Xiao and Hanjie Chen and Frederick L. Oswald},
  year    = {2024},
  journal = {arXiv preprint arXiv: 2404.01461}
}
```
