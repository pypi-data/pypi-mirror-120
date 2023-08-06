# [MIIDL](https://chunribu.github.io/miidl)

[![chunribu logo](https://img.shields.io/badge/chunribu-🚀-black?logo=github)](https://github.com/chunribu/) [![Anaconda-Server Badge](https://anaconda.org/bioconda/miidl/badges/version.svg)](https://anaconda.org/bioconda/miidl) [![Anaconda-Server Badge](https://anaconda.org/bioconda/miidl/badges/downloads.svg)](https://anaconda.org/bioconda/miidl) [![Anaconda-Server Badge](https://anaconda.org/bioconda/miidl/badges/platforms.svg)](https://anaconda.org/bioconda/miidl) [![Anaconda-Server Badge](https://anaconda.org/bioconda/miidl/badges/license.svg)](https://anaconda.org/bioconda/miidl) 

**MIIDL** `/ˈmaɪdəl/` is a Python package for biomarker identification based on interpretable deep learning.

---
### [Getting Started](https://github.com/chunribu/miidl/blob/main/Tutorials.ipynb)

👋Welcome! 

[🔗This guide](https://github.com/chunribu/miidl/blob/main/Tutorials.ipynb) will provide you with a specific example that using `miidl` to detect microbial biomarkers for the diagnosis of colorectal cancer. 

After that, you will learn how to use this tool properly.

---
### Installation

```bash
pip install miidl
```
or
```bash
conda install miidl captum -c pytorch -c conda-forge -c bioconda
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
### Contact

If you have further thoughts or queries, please feel free to email at chunribu@mail.sdu.edu.cn or open an issue!

---
### Licence

MIIDL is released under the [MIT licence](https://github.com/chunribu/miidl/blob/main/LICENSE).
<!-- ---
### Citation

doi: -->
