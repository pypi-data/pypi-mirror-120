![image](https://raw.githubusercontent.com/seisbench/seisbench/main/docs/_static/seisbench_logo_subtitle_outlined.svg)
---
![PyPI - License](https://img.shields.io/pypi/l/seisbench)
![GitHub Workflow Status](https://img.shields.io/github/workflow/status/seisbench/seisbench/main_push_action)
![Read the Docs](https://img.shields.io/readthedocs/seisbench)
![PyPI](https://img.shields.io/pypi/v/seisbench)
[![Python 3.6](https://img.shields.io/badge/python-3.6+-blue.svg)](https://www.python.org/downloads/release/python-360/)

The Seismology Benchmark collection (*SeisBench*) is an open-source python toolbox for 
machine learning in seismology.
It provides a unified API for accessing seismic datasets and training and applying machine learning algorithms to seismic data.
SeisBench has been built to reduce the overhead when applying or developing machine learning techniques for seismic data.

## Getting started

SeisBench offers three core modules, `data`, `models`, and `generate`.
`data` provides access to benchmark datasets and offers functionality for loading datasets.
`models` offers a collection of machine learning models for seismology.
You can easily create models, load pretrained models or train models on any dataset.
`generate` contains tools for building data generation pipelines.
They bridge the gap between `data` and `models`.

The easiest way of getting started is through our colab notebooks.

Dataset basics: [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/seisbench/seisbench/blob/main/examples/01a_dataset_basics.ipynb)

Model API: [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/seisbench/seisbench/blob/main/examples/01b_model_api.ipynb)

Generator Pipelines: [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/seisbench/seisbench/blob/main/examples/01c_generator_pipelines.ipynb)

Training PhaseNet (advanced): [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/seisbench/seisbench/blob/main/examples/02_training_phasenet.ipynb)

Alternatively, you can clone the repository and run the same [examples](https://github.com/seisbench/seisbench/tree/main/examples) locally.

To get detailed information on Seisbench check out the [SeisBench documentation](https://seisbench.readthedocs.io/).

## Installation

SeisBench can be installed in two ways.
In both cases, you might consider installing SeisBench in a virtual environment, for example using [conda](https://docs.conda.io/en/latest/).

The recommended way is installation through pip.
Simply run:
```
pip install seisbench
```

Alternatively, you can install the latest version from source.
For this approach, clone the repository, switch to the repository root and run:
```
pip install .
```

## Contributing
There are many ways to contribute to SeisBench and we are always looking forward to your contributions.
Check out the [contribution guidelines](https://github.com/seisbench/seisbench/blob/main/CONTRIBUTING.md) for details on how to contribute.

## Citation
A reference publication for SeisBench is under publication.
Please check back later.