<p  align="center">
  <img src='logo.png' width='200'>
</p>

# Diversity Over Size: On the Effect of Sample and Topic Sizes for Topic-Dependent Argument Mining Datasets
[![Arxiv](https://img.shields.io/badge/Arxiv-2205.11472-red?style=flat&logo=arxiv&logoColor=white)](https://arxiv.org/abs/2205.11472)
[![License](https://img.shields.io/github/license/UKPLab/ukp-project-template)](https://opensource.org/licenses/Apache-2.0)
[![Python Versions](https://img.shields.io/badge/Python-3.12-blue.svg?style=flat&logo=python&logoColor=white)](https://www.python.org/)

This repository provides the means to download the newly created **Few-Shot-150T Corpus (FS150T-Corpus)**, introduced in the 
paper ["Diversity Over Size: On the Effect of Sample and Topic Sizes for Topic-Dependent Argument Mining Datasets"](https://arxiv.org/abs/2205.11472). 

> **Abstract:** Topic-Dependent Argument Mining (TDAM), that is extracting and classifying argument components for a specific topic from large document sources, is an inherently difficult task for machine learning models and humans alike, as large TDAM datasets are rare and recognition of argument components requires expert knowledge. The task becomes even more difficult if it also involves stance detection of retrieved arguments. In this work, we investigate the effect of TDAM dataset composition in few- and zero-shot settings. Our findings show that, while fine-tuning is mandatory to achieve acceptable model performance, using carefully composed training samples and reducing the training sample size by up to almost 90% can still yield 95% of the maximum performance. This gain is consistent across three TDAM tasks on three different datasets.

Contact person: [Benjamin Schiller](mailto:schiller@summetix.com) 

[UKP Lab](https://www.ukp.tu-darmstadt.de/) | [TU Darmstadt](https://www.tu-darmstadt.de/) | [summetix](https://www.summetix.com/)

Don't hesitate to send us an e-mail or report an issue, if something is broken (and it shouldn't be) or if you have further questions.

## Getting started
Due to license reasons, we cannot provide the download to the full dataset files directly. Instead, all the sentences
have to be retrieved from [Common Crawl](https://commoncrawl.org) WARC files and are missing in the dataset files in this 
repository. To download the sentences, follow these instructions:

First, create a virtual environment and install the requirements:

    python3.12 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt

Next, use _src/main.py_ to complete the datasets:

    python src/main.py -i dataset/test_full_no_sents.tsv -o dataset/test_full.tsv
    python src/main.py -i dataset/dev_full_no_sents.tsv -o dataset/dev_full.tsv
    python src/main.py -i dataset/train_full_no_sents.tsv -o dataset/train_full.tsv

The code checks via hashes if the retrieved sentences are correct and prints out a message if not. The code also
checks if all sentences were retrieved at the end.

Retrieving all sentences can take up to 4 hours and the retrieval process may get interrupted. Hence, every 500 rows,
a checkpoint file will be saved (e.g. test_full.chkpt500.tsv). In case of an interruption, this file can be used as
in-file (-i) to start the process from the checkpoint.

The code was tested with Python 3.12. 
In case you cannot retrieve the dataset, please request it from us at https://tudatalib.ulb.tu-darmstadt.de/handle/tudatalib/4353.

Download the other corpora used in the paper at:

- [UKP Sentential Argument Mining Corpus (UKP-Corpus)](https://tudatalib.ulb.tu-darmstadt.de/handle/tudatalib/2345)
- [IAM-Corpus](https://github.com/LiyingCheng95/IAM/tree/main/claims)
- [IBM-Corpus](https://research.ibm.com/haifa/dept/vst/debating_data.shtml)



## Cite

Please use the following citation:

```
@inproceedings{
  anonymous2024diversityoversize,
  title={Diversity Over Size: On the Effect of Sample and Topic Sizes for Topic-Dependent Argument Mining Datasets},
  author={Anonymous},
  booktitle={The 2024 Conference on Empirical Methods in Natural Language Processing},
  year={2024},
  url={https://openreview.net/forum?id=ZV4HC5Ifuk}
}
```

## Disclaimer

> This repository contains experimental software and is published for the sole purpose of giving additional background details on the respective publication. 
