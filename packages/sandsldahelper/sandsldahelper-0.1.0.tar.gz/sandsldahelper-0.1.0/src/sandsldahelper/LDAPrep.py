# --------------------------------------------------------------------------------------
# File: "0420_topic_modeling_prep.py"
# Dir: "scripts"
# Created: 2021-01-27
# --------------------------------------------------------------------------------------

"""
this file is create a gensim topic model based on factors with the highest coherence value

the file that cleans the text is required before this script is run

KEY: this file requires the installation of message pack which is a compacted version of json

you can install message pack by using this line to install the package

`pip install msgpack`
"""

from SandsPythonFunctions.TimerFunctions import function_timer as timer
from pathlib import Path
from tqdm import tqdm
import SandsPythonFunctions.ParquetFunctions as pf
import SandsPythonFunctions.TextFunctions as tf
import msgpack
import numpy as np
import pandas as pd
import pretty_errors
import tomotopy as tp


def get_files(topic_model_path, target_label: str):
    """
    gets the path for the script location and returns the parquet files located in the
    local folder
    """
    topic_model_path.mkdir(parents=True, exist_ok=True)
    return topic_model_path


def get_stopwords():
    """
    this will test to see if the stopwords from the nltk module have already been
    downloaded if they have not they will be download this function is needed for both
    word embedding and topic modeling and is just overall useful
    """
    from nltk.downloader import download
    from nltk.corpus import stopwords

    try:
        return stopwords.words("english")
    except:
        print(f"NLTK needs to download the stopwords. This will take a while.")
        download("stopwords")
        print(f"NLTK has finished downloading stopwords.")
        return stopwords.words("english")


@timer
def remove_stopwords_function(dta):
    """
    this function removes all of the stopwords from every item in a column in this case
    in the cleaned column
    this function is needed for both word embedding and topic modeling and is just
    overall useful
    """
    stop_words = get_stopwords()
    dta["text"] = dta["text"].apply(
        lambda x: " ".join([word for word in x.split() if word not in (stop_words)])
    )
    return dta


@timer
def lemm_text_prep(dta):
    """this will clean the text of the column name given"""
    import vaex

    print("Dropping missing values using pandas")  # TESTCODE:
    dta = dta.dropna(subset=["text"])
    # dta["text"] = dta["text"].str.replace({"nan": "", "NaN": "", "None": "", "none": "", None: ""})
    dta["text"] = dta["text"].str.replace(
        r"http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+",
        " ",
        regex=True,
    )
    print("Processing removal of non-alpha characters")  # TESTCODE:
    dta["text"] = dta["text"].apply(
        lambda x: " ".join([word for word in x.split() if word.isalpha()])
    )
    print("Done processing removal of non-alpha characters")  # TESTCODE:
    print("Converting to Vaex Dataframe")  # TESTCODE:
    dta = vaex.from_pandas(dta)
    print("Done converting to Vaex Dataframe")  # TESTCODE:
    print("Now processing using vaex")  # TESTCODE:
    dta["text"] = dta["text"].str.lower()
    dta["text"] = dta["text"].str.replace("[^\w\s]", "", regex=True)  # punctuation
    dta["text"] = dta["text"].str.replace(r"'", " ", regex=True)  # apostrophe
    dta["text"] = dta["text"].str.replace(r"<[^<>]+(>|$)", " ", regex=True)
    dta["text"] = dta["text"].str.replace(r"<img[^<>]+(>|$)", " ", regex=True)
    dta["text"] = dta["text"].str.replace(r"\[img_assist[^]]*?\]", " ", regex=True)
    dta["text"] = dta["text"].str.replace(r"\W+", " ", regex=True)
    dta["text"] = dta["text"].str.replace(r" +", " ", regex=True)
    # dta = tf.clean_text_columns(
    #     dta,
    #     target_column="text",
    #     remove_punctuation=True,
    #     make_lower=False,
    #     remove_stopwords=True,
    #     stem_strings=False,
    #     remove_urls=True,
    #     get_number_of_words=False,
    #     remove_empty_body_posts=True,
    #     remove_non_alpha=True,
    #     print_timings=False,
    # )
    print("Converting back to pandas (and processing the 8 regex string functions)")  # TESTCODE:
    dta = dta.to_pandas_df()
    print("Done converting back to pandas")  # TESTCODE:
    print("Processing the decoding of ascii characters (using pandas)")  # TESTCODE:
    dta["text"] = dta["text"].str.encode("ascii", "ignore").str.decode("ascii")
    print("Done processing the decoding of ascii characters (using pandas)")  # TESTCODE:
    return dta


@timer
def lemmatization_spacy_joblib(texts):
    """this lemmatizes the text
    Make sure to install joblib by using this command `pip install joblib`
    """
    import sys
    import spacy
    from joblib import Parallel, delayed

    try:
        # nlp = spacy.load("en_core_web_sm", disable=["parser", "ner"], n_threads=6)
        # nlp = spacy.load("en_core_web_sm", disable=["tagger", "parser", "ner"])
        nlp = spacy.load("en_core_web_sm", disable=["parser", "ner"])
        # nlp.add_pipe(nlp.create_pipe("sentencizer"))
        nlp.add_pipe("sentencizer")
    except OSError:
        sys.exit(
            "You must run `python -m spacy download en_core_web_sm` to download data required to run spacy"
        )

    def lemmatize_pipe(doc):
        allowed_postags = ["NOUN", "ADJ", "VERB", "ADV"]
        return [
            str(token.lemma_).lower()
            for token in doc
            if token.is_alpha and token.text.lower() and token.pos_ in allowed_postags
        ]

    def chunker(iterable, total_length, chunksize):
        return (iterable[pos : pos + chunksize] for pos in range(0, total_length, chunksize))

    def flatten(list_of_lists):
        "Flatten a list of lists to a combined list"
        return [item for sublist in list_of_lists for item in sublist]

    def process_chunk(texts):
        return [lemmatize_pipe(doc) for doc in nlp.pipe(texts, batch_size=20)]

    def preprocess_parallel(texts, chunksize=100):

        executor = Parallel(n_jobs=10)
        do = delayed(process_chunk)
        tasks = (do(chunk) for chunk in chunker(texts, len(texts), chunksize=chunksize))
        result = executor(tasks)
        return flatten(result)

    return preprocess_parallel(texts, chunksize=3500)


@timer
def lemmatize_text(dta):
    dta = lemm_text_prep(dta)
    dta = remove_stopwords_function(dta)
    texts = dta["text"].tolist()
    lemmatized_texts = lemmatization_spacy_joblib(texts)
    dta["lemmatized_texts"] = lemmatized_texts
    dta[["id", "text", "lemmatized_texts"]]
    return dta


@timer
def load_lemmatized_texts(dta, ltxp_path):
    dta = lemmatize_text(dta)
    dta["lemmatized_texts"] = [" ".join(text) for text in dta["lemmatized_texts"].values.tolist()]
    dta = dta[dta["lemmatized_texts"] != ""]
    dta = tf.remove_words_below_freq(dta, "lemmatized_texts", min_num_word_freq=5)
    dta = dta[dta["num_words"] > 4]
    pf.save_dataframe_as_parquet(dta, ltxp_path)
    return dta["lemmatized_texts"].values.tolist()


@timer
def prepare_lemmatized_texts(topic_model_path, target_label, dta, lmtx_path, ltxp_path):
    """TODO: Docstring"""
    import SandsPythonFunctions.ParquetFunctions as pf

    if lmtx_path.exists():
        return msgpack.unpackb(lmtx_path.read_bytes())
        # return msgpack.load(open(lmtx_path, "rb"))
    else:
        lemmatized_texts = load_lemmatized_texts(dta, ltxp_path)
        lmtx_path.write_bytes(msgpack.packb(lemmatized_texts))
        # msgpack.dump(lemmatized_texts, open(lmtx_path, "wb"))
        return lemmatized_texts


@timer
def extract_ngrams(corpus: tp.utils.Corpus, lemmatized_texts: list, ngrm_path: Path):
    """takes the corpus and finds the most common ngrams more information can be found at the two sites below:
    https://bab2min.github.io/tomotopy/v0.12.2/en/utils.html#tomotopy.utils.Corpus.extract_ngrams
    https://bab2min.github.io/tomotopy/v0.12.2/en/utils.html#tomotopy.utils.Corpus.concat_ngrams
    TODO: figure out how you should use the length of the lemmatized_texts to influance the ngram variables
    """
    num_docs_5_per = int(len(lemmatized_texts) * 0.05)
    cands = corpus.extract_ngrams(
        min_cf=20,
        min_df=10,
        max_len=5,
        max_cand=5000,
        normalized=True,
        min_score=0.5,
    )
    print(f"There are {len(cands)} ngram found")  # TESTCODE:
    # for cand in cands: print(cand)  # TESTCODE:
    output_string = ""
    for cand in cands:
        output_string = f"{output_string}cand\n\n"
    ngrm_path.write_text(output_string)
    corpus.concat_ngrams(cands, delimiter="_")
    return corpus


@timer
def create_corpus(lemmatized_texts: list, corp_path: Path, ltxp_path: Path, ngrm_path: Path):
    """this takes the list of lemmatized texts and tokenizes, extracts ngrams, creates saves a tomotopy corpus

    Args:
        lemmatized_texts (list): a list of strings which are the lemmatized texts
        corp_path (Path): corpus pathlib.Path
    """
    if not corp_path.exists():
        corpus = tp.utils.Corpus(tokenizer=tp.utils.SimpleTokenizer(stemmer=None))
        corpus.process(lemmatized_texts)
        corpus = extract_ngrams(corpus, lemmatized_texts, ngrm_path)
        corpus.save(corp_path)


@timer
def prep_topic_model_files(target_label: str, topic_model_path: Path, dta: pd.DataFrame):
    lmtx_path = topic_model_path / f"{target_label}_tomotopy_lemmatized_texts.msgpack"
    ltxp_path = topic_model_path / f"{target_label}_tomotopy_lemmatized_texts.parquet"
    corp_path = topic_model_path / f"{target_label}_corpus.tomotopy"
    ngrm_path = topic_model_path / f"{target_label}_ngram.txt"
    topic_model_path = get_files(topic_model_path, target_label)
    lemmatized_texts = prepare_lemmatized_texts(
        topic_model_path, target_label, dta, lmtx_path, ltxp_path
    )
    create_corpus(lemmatized_texts, corp_path, ltxp_path, ngrm_path)
