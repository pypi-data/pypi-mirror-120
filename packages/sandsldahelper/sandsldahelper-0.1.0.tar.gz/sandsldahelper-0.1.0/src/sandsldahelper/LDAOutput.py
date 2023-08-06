# --------------------------------------------------------------------------------------
# File: "topic_model_003_output.py"
# Dir: "topic_model_scripts\topic_model_003_output.py"
# Created: 2021-08-17
# --------------------------------------------------------------------------------------

"""
this file is meant to create output files for the topic model created from the data provided

this page was very useful here:
https://stackoverflow.com/questions/43357247/get-document-topics-and-get-term-topics-in-gensim
"""

from SandsPythonFunctions.TimerFunctions import function_timer as timer
from pathlib import Path
from tqdm import tqdm
import SandsPythonFunctions.ParquetFunctions as pf
import msgpack
import numpy as np
import pandas as pd
import pretty_errors
import tomotopy as tp


def create_pyLDAVis(mdl, pyvs_path):
    import pyLDAvis
    import numpy as np

    if not pyvs_path.exists():
        topic_term_dists = np.stack([mdl.get_topic_word_dist(k) for k in range(mdl.k)])
        doc_topic_dists = np.stack([doc.get_topic_dist() for doc in mdl.docs])
        doc_topic_dists /= doc_topic_dists.sum(axis=1, keepdims=True)
        doc_lengths = np.array([len(doc.words) for doc in mdl.docs])
        vocab = list(mdl.used_vocabs)
        term_frequency = mdl.used_vocab_freq
        vis = pyLDAvis.prepare(
            topic_term_dists,
            doc_topic_dists,
            doc_lengths,
            vocab,
            term_frequency,
            start_index=0,  # tomotopy starts topic ids with 0, pyLDAvis with 1
            sort_topics=False,  # IMPORTANT: otherwise topic_ids between pyLDAvis and tomotopy will not match
        )
        pyLDAvis.save_html(vis, open(str(pyvs_path.resolve()), "w"))


def create_topic_summery_text_page(mdl, topt_path):
    if not topt_path.exists():
        extractor = tp.label.PMIExtractor(
            min_cf=10, min_df=5, max_len=5, max_cand=10000, normalized=True
        )
        cands = extractor.extract(mdl)
        labeler = tp.label.FoRelevance(mdl, cands, min_df=5, smoothing=1e-2, mu=0.25)
        output_string = ""
        for k in range(mdl.k):
            output_string = f"{output_string}== Topic #{k} ==\n"
            output_string = f"{output_string}\nLabels: {', '.join(label for label, score in labeler.get_topic_labels(k, top_n=5))}\n"
            for word, prob in mdl.get_topic_words(k, top_n=30):
                if len(word) < 4:
                    output_string = f"{output_string}\n{word}\t\t\t{prob}"
                elif len(word) > 7:
                    output_string = f"{output_string}\n{word}\t{prob}"
                else:
                    output_string = f"{output_string}\n{word}\t\t{prob}"
            output_string = f"{output_string}\n\n"
        topt_path.write_text(output_string)


@timer
def extract_dominant_topic(mdl, ltxp_path, dtdx_path, corp_path, dtdp_path, dtcx_path):
    if not (dtdp_path.exists() and dtdx_path.exists() and dtcx_path.exists()):
        dta = pf.read_parquet_by_path(ltxp_path)
        # print(f"len dta: {len(dta)}; len mdl.docs: {len(mdl.docs)}")  # TESTCODE:
        if len(mdl.docs) == len(dta):
            corpus = tp.utils.Corpus.load(str(corp_path))
            inferred_corpus, ll = mdl.infer(corpus)
            dom_dist = []
            for doc in tqdm(inferred_corpus, desc="creating individual post dominant topic output"):
                dom_dist.append(doc.get_topic_dist().tolist())
            # print(f"type(dom_dist[0]: {type(dom_dist[0])}")  # TESTCODE:
            dta["dom_dist"] = dom_dist
        else:
            lemmatized_texts = dta["lemmatized_texts"].tolist()
            dom_dist = []
            for lemmatized_text in tqdm(lemmatized_texts, desc="Processing dominant topic by post"):
                doc = lemmatized_text.split()
                try:
                    doc = mdl.make_doc(doc)
                    topic_dist, ll = mdl.infer(doc)
                    dom_dist.append(topic_dist.tolist())
                except:
                    dom_dist.append(np.nan)
            dta["dom_dist"] = dom_dist
            dta = dta.dropna()
            dom_dist = dta["dom_dist"].tolist()
        dta["dom_topic"] = [(dist.index(max(dist)) + 1) for dist in dom_dist]
        dta["dom_topic_score"] = [max(dist) for dist in dom_dist]
        dta = dta[["id", "text", "dom_dist", "dom_topic", "dom_topic_score"]]
        pf.save_dataframe_as_parquet(dta, dtdp_path)
        print(dta.columns)
        dta.to_excel(dtdx_path)
        dta = dta.groupby("dom_topic")["id"].count()
        dta.to_excel(dtcx_path)


def create_dominant_topic_dta(domt_path, dta, text_dom_topics, percents_dom_topic):
    dta["dominant_topic"] = text_dom_topics
    dta["percent_dominant_topic"] = percents_dom_topic
    pf.save_dataframe_as_parquet(dta[["id", "dominant_topic", "percent_dominant_topic"]], domt_path)
    dta["percent_dominant_topic_string"] = [
        str(round(per, 3)).ljust(5, "0") for per in percents_dom_topic
    ]
    dta["dominant_topic_string"] = [str(dom).zfill(3) for dom in text_dom_topics]
    return dta


def create_dominant_topic_text_file(dta, dtxt_path, tpex_path, tgex_path):
    dta["text_no_newline"] = dta["text"].str.replace("\n", " |NEWLINE_CHAR| ")
    dta.to_excel(tpex_path, sheet_name="dominant_topics")
    dta = dta.sort_values(
        ["dominant_topic_string", "percent_dominant_topic_string"], ascending=[True, False]
    )
    dta["output_string"] = (
        dta["dominant_topic_string"]
        + " - "
        + dta["percent_dominant_topic_string"]
        + " - "
        + dta["id"]
        + " - "
        + dta["text_no_newline"]
    )
    output_string = dta.output_string.str.cat(sep="\n\n")
    dtxt_path.write_text(output_string)


def create_top_sample_dominant_topic_text_file(dta, dtst_path):
    dta["text_no_newline"] = dta["text"].str.replace("\n", " |NEWLINE_CHAR| ")
    dta = dta.sort_values(
        ["dominant_topic_string", "percent_dominant_topic_string"], ascending=[True, False]
    )
    dta = dta.groupby("dominant_topic_string").head(4).reset_index(drop=True)
    dta["output_string"] = (
        dta["dominant_topic_string"]
        + " - "
        + dta["percent_dominant_topic_string"]
        + " - "
        + dta["id"]
        + " - "
        + dta["text_no_newline"]
    )
    output_string = dta.output_string.str.cat(sep="\n\n")
    dtst_path.write_text(output_string)


def create_output_string(dta):
    dta["output_string"] = (
        dta["id"]
        + " - "
        + dta["year_month"]
        + " - "
        + dta["comment"]
        + " - "
        + dta["text_combined"]
    )
    return dta.output_string.str.cat(sep="\n")


@timer
def load_lda_model(ldam_path):
    model_bytes = ldam_path.read_bytes()
    return tp.LDAModel.loads(model_bytes)


def create_lda_output_files(
    target_label: str, topic_model_path: Path, dta: pd.DataFrame, num_topics: int
):
    topic_model_num_path = topic_model_path / f"{target_label}_{str(num_topics).zfill(4)}_topics"
    topic_model_num_path.mkdir(parents=True, exist_ok=True)
    target_num_label = f"{target_label}_{str(num_topics).zfill(4)}"
    ldam_path = topic_model_num_path / f"{target_num_label}_lda_model.ldam"
    mdl = load_lda_model(ldam_path)
    pyvs_path = topic_model_num_path / f"{target_num_label}_pyLDAvis.html"
    create_pyLDAVis(mdl, pyvs_path)
    topt_path = topic_model_num_path / f"{target_num_label}_topics_terms.txt"
    create_topic_summery_text_page(mdl, topt_path)

    # domt_path = topic_model_num_path / f"{target_num_label}_dominate_topics.parquet"
    # domt_path = topic_model_num_path / f"{target_num_label}_dominate_topics.parquet"
    # dtxt_path = topic_model_num_path / f"{target_num_label}_dominate_topics.txt"
    # dtst_path = topic_model_num_path / f"{target_num_label}_dominate_topics_sample.txt"
    # tpex_path = topic_model_num_path / f"{target_num_label}_dominant_topics_terms.xlsx"
    # tgex_path = topic_model_num_path / f"{target_num_label}_pub_count_by_year.xlsx"
    ltxp_path = topic_model_path / f"{target_label}_tomotopy_lemmatized_texts.parquet"
    dtdx_path = topic_model_num_path / f"{target_num_label}_dominant_topic_by_doc.xlsx"
    dtcx_path = topic_model_num_path / f"{target_num_label}_dominant_topic_count.xlsx"
    dtdp_path = topic_model_num_path / f"{target_num_label}_dominant_topic_by_doc.parquet"
    corp_path = topic_model_path / f"{target_label}_corpus.tomotopy"
    extract_dominant_topic(mdl, ltxp_path, dtdx_path, corp_path, dtdp_path, dtcx_path)
    # dta = create_dominant_topic_dta(domt_path, dta, text_dom_topics, percents_dom_topic)
    # create_dominant_topic_text_file(dta, dtxt_path, tpex_path, tgex_path)
    # create_top_sample_dominant_topic_text_file(dta, dtst_path)
