# Few-Shot-150T Corpus v1.1 (FS150T-Corpus)
The FS150T-Corpus consists of three files train_full.tsv (17,280 samples, 120 topics), dev_full.tsv 
(1,440 samples, 10 topics), and test_full.tsv (2,880 samples, 20 topics) in TSV format. Each topic has exactly 144 
samples. The topics do not overlap, i.e. this dataset is split for cross-topic experiments.

Each file has the following columns:

* **topic**: The topic of the sentence.
* **url**: The URL of the document from where the sentence was extracted
* **source**: The domain name from where the document originates
* **timestamp**: The timestamp of the document
* **id**: An id of the document
* **warc_file/warc_offset/warc_length/sentence_offset/sentence_length**: Metadata needed to recover the sentence from CommonCrawl
* **sentence_hash**: Hash to check if the sentence was correctly recovered
* **annotation**: Labels indicating whether this sentence is no argument towards the topic (NoArgument), a contra
argument (Argument_against), or a pro argument (Argument_for)