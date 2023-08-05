# [MIIDL](https://chunribu.github.io/miidl)

**MIIDL** `/ˈmaɪdəl/` is a Python package for biomarker identification based on interpretable deep learning.

---
### [Getting Started](https://github.com/chunribu/miidl/blob/main/Tutorials.ipynb)

👋Welcome! [🔗This guide](https://github.com/chunribu/miidl/blob/main/Tutorials.ipynb) will provide you with a specific example that using `miidl` to detect microbial biomarkers for the diagnosis of colorectal cancer. After that, you will konw how to use this tool properly.

---
### Installation

```bash
pip install miidl
```
or
```bash
conda install miidl -c bioconda
```

---
### Features

+ One-stop profiling
+ Multiple strategies for biological data
+ More interpretable, not a "black box"

---
### Workflow

#### 1) Quality Control

The very first procedure is filtering features according to a threshold of observation (non-missing) rate (0.3 by default).

#### 2) Normalization

`miidl` offers plenty of normalization methods to transform data and make samples more comparable. 

#### 3) Imputation

By default, this step is unactivated, as `miidl` is designed to solve problems including sparseness. But imputation can be useful in some cases. Commonly used methods are available if needed. 

#### 4) Reshape

The pre-processed data also need to be zero-completed to a certain length, so that a CNN model can be applied.

#### 5) Modeling

A CNN classifier is trained for discrimination. [PyTorch](https://pytorch.org) is needed.

#### 6) Interpretation

[Captum](https://captum.ai/) is dedicated to model interpretability for PyTorch. This step relies heavily on captum.

---
<!-- ---
### Citation

doi: -->