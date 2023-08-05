## FlexNeuART (flex-noo-art)
Flexible classic and NeurAl Retrieval Toolkit, or shortly `FlexNeuART` (**intended pronunciation** flex-noo-art) 
is a substantially reworked [`knn4qa` package](knn4qa.md).  The overview can be found in our EMNLP OSS workshop paper: 
[Flexible retrieval with NMSLIB and FlexNeuART, 2020. Leonid Boytsov, Eric Nyberg](https://arxiv.org/abs/2010.14848).


In Aug-Dec 2020, we used this framework to generate best traditional and/or neural runs 
in the [MSMARCO Document ranking task](https://microsoft.github.io/msmarco/#docranking).
In fact, our best traditional (non-neural) run slightly outperformed a couple of neural submissions.
The code for the best-performing neural model will be published within 2-3 months. This model is described in our ECIR 2021 paper:
[Boytsov, Leonid, and Zico Kolter. "Exploring Classic and Neural Lexical Translation Models for Information Retrieval: Interpretability, Effectiveness, and Efficiency Benefits." ECIR 2021](https://arxiv.org/abs/2102.06815).


`FlexNeuART` is under active development. More detailed description and documentaion is to appear. Currently we have:

* [The installation instructions](INSTALL.md)
* [Usage notebooks covering most functionality (including Python API demo)](scripts/demo/README.md)
* [Former life (as a knn4qa package), including acknowledgements and publications](knn4qa.md)
* Collection-specific (**older version the library**):
   * [MS MARCO](scripts/data_convert/msmarco/README.md)
   * [Yahoo Answers](scripts/data_convert/yahoo_answers/README.md)

The framework supports data in generic JSONL format. We provide conversion (and in some cases download) scripts for the following collections:
* MS MARCO data v1 and v2 (documents and passages)
* Wikipedia DPR (Natural Questions, SQuAD)
* Yahoo Answers collections
* Cranfield (a small toy collection)


For neural network training FlexNeuART incorporates
a re-worked variant of CEDR ([MacAvaney et al' 2019](https://github.com/Georgetown-IR-Lab/cedr)).



