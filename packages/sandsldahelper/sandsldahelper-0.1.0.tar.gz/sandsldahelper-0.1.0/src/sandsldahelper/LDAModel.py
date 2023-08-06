# --------------------------------------------------------------------------------------
# File: "topic_model_002_lda.py"
# Dir: "topic_model_scripts\topic_model_002_lda.py"
# Created: 2021-08-17
# --------------------------------------------------------------------------------------

"""
this file is meant to create a topic model using the HDP algorithm
I used  Normalized  Pointwise Mutual Information (NPMI) for model evaluation
"NPMI ranges from [-1,1] and it measures how much the top-10 words of a topic are related to each other, where higher positive NMPI is better."
BERT for Arabic Topic Modeling: An Experimental Study on BERTopic Technique by Abeer Abuzayed Hend Al-Khalifa
"""

from SandsPythonFunctions.TimerFunctions import function_timer as timer
from pathlib import Path
from tqdm import tqdm
import msgpack
import pretty_errors
import tomotopy as tp


def pre_lda_model_trianing(num_topics, corp_path):
    corpus = tp.utils.Corpus.load(corp_path)
    mdl = tp.LDAModel(k=num_topics, min_cf=10, min_df=5, corpus=corpus)
    mdl.train(0)
    min_cf_5_per = int(len(mdl.used_vocabs) * 0.05)
    min_df_5_per = int(len(mdl.docs) * 0.05)
    rm_top_5_per = int(20)
    return corpus, min_cf_5_per, min_df_5_per, rm_top_5_per


def make_hyperparameter_combos():
    term_weights = [tp.TermWeight.ONE, tp.TermWeight.IDF, tp.TermWeight.PMI]
    alphas = [0.01, 0.1, 0.5, 1.0]
    etas = [0.01, 0.1, 0.5, 1.0]
    hyperparameters_combos = []
    for alpha in alphas:
        for eta in etas:
            for term_weight in term_weights:
                hyperparameters_combos.append([term_weight, alpha, eta])
    return hyperparameters_combos


def train_lda_model(
    corpus,
    num_topics,
    min_cf_5_per,
    min_df_5_per,
    rm_top_5_per,
    hyperparameters=[tp.TermWeight.ONE, 0.1, 0.01],
):
    mdl = tp.LDAModel(
        min_cf=min_cf_5_per,
        min_df=min_df_5_per,
        corpus=corpus,
        rm_top=rm_top_5_per,
        k=num_topics,
        tw=hyperparameters[0],
        alpha=hyperparameters[1],
        eta=hyperparameters[2],
    )
    mdl.train(0)
    # print(
    #     f"Training LDA model with num_topics ({num_topics}), term_weight ({str(hyperparameters[0])}), alpha ({hyperparameters[1]}) and eta ({hyperparameters[2]})"
    # )
    # for i in range(0, 1000, 500):  # TESTCODE:
    #     mdl.train(500)  # TESTCODE:
    #     print(f"Iteration: {i}\tLog-likelihood: {mdl.ll_per_word}")  # TESTCODE:
    return mdl


def coherence_scores_file_manage(cohs_path, topics_coherence):
    import json

    all_coherence_scores = []
    if cohs_path.exists():
        with open(cohs_path, "r") as output_json:
            all_coherence_scores = json.load(output_json)
        # all_coherence_scores.append(old_topics_coherence)
    all_coherence_scores.append(topics_coherence)
    with open(cohs_path, "w") as output_json:
        json.dump(all_coherence_scores, output_json)


def calculate_coherence_scores(num_topics, hyperparameters, mdl):
    coh_u_mass = tp.coherence.Coherence(mdl, coherence="u_mass")
    coh_c_uci = tp.coherence.Coherence(mdl, coherence="c_uci")
    coh_c_v = tp.coherence.Coherence(mdl, coherence="c_v")
    coh_c_npmi = tp.coherence.Coherence(mdl, coherence="c_npmi")
    ave_coherence_u_mass = coh_u_mass.get_score()
    ave_coherence_c_uci = coh_c_uci.get_score()
    ave_coherence_c_v = coh_c_v.get_score()
    ave_coherence_c_npmi = coh_c_npmi.get_score()
    return [
        num_topics,
        str(hyperparameters[0]),
        hyperparameters[1],
        hyperparameters[2],
        ave_coherence_u_mass,
        ave_coherence_c_uci,
        ave_coherence_c_v,
        ave_coherence_c_npmi,
    ]


@timer
def test_lda_parameters(ldam_path, corp_path, cohs_path, num_topics, hyper_parameter_testing):
    if not ldam_path.exists():
        print(f"Training ldamodel for {str(num_topics).zfill(4)} topics")
        corpus, min_cf_5_per, min_df_5_per, rm_top_5_per = pre_lda_model_trianing(
            num_topics, corp_path
        )
        mdl = tp.LDAModel(k=num_topics, min_cf=10, min_df=5, corpus=corpus)
        if hyper_parameter_testing:
            hyperparameter_combos = make_hyperparameter_combos()
            for hyperparameters in tqdm(
                hyperparameter_combos, desc=f"Testing hyperparameters for {num_topics} topics"
            ):
                mdl = train_lda_model(
                    corpus, num_topics, min_cf_5_per, min_df_5_per, rm_top_5_per, hyperparameters
                )
                topics_coherence = calculate_coherence_scores(num_topics, hyperparameters, mdl)
                coherence_scores_file_manage(cohs_path, topics_coherence)
        else:
            hyperparameters = [tp.TermWeight.ONE, 0.1, 0.01]
            mdl = train_lda_model(
                corpus, num_topics, min_cf_5_per, min_df_5_per, rm_top_5_per, hyperparameters
            )
            topics_coherence = calculate_coherence_scores(num_topics, hyperparameters, mdl)
            coherence_scores_file_manage(cohs_path, topics_coherence)
        # mdl.summary()
        # print("Writing model file")
        # model_bytes = mdl.saves(full=True)
        # ldam_path.write_bytes(model_bytes)


def create_lda_model(
    ldam_path, corp_path, cohs_path, num_topics, hyperparameters=[tp.TermWeight.ONE, 0.1, 0.01]
):
    corpus, min_cf_5_per, min_df_5_per, rm_top_5_per = pre_lda_model_trianing(num_topics, corp_path)
    mdl = train_lda_model(
        corpus, num_topics, min_cf_5_per, min_df_5_per, rm_top_5_per, hyperparameters
    )
    topics_coherence = calculate_coherence_scores(num_topics, hyperparameters, mdl)
    coherence_scores_file_manage(cohs_path, topics_coherence)
    model_bytes = mdl.saves(full=True)
    ldam_path.write_bytes(model_bytes)


@timer
def get_coherence_model_score(num_topics, ldam_path, cohs_path):
    """There is a bug with the c_v method this issue has been reported here: https://github.com/bab2min/tomotopy/issues/126"""
    import json

    if not cohs_path.exists():
        print("Processing coherence score")
        model_bytes = ldam_path.read_bytes()
        mdl = tp.LDAModel.loads(model_bytes)
        coh_u_mass = tp.coherence.Coherence(mdl, coherence="u_mass")
        coh_c_uci = tp.coherence.Coherence(mdl, coherence="c_uci")
        coh_c_v = tp.coherence.Coherence(mdl, coherence="c_v")
        coh_c_npmi = tp.coherence.Coherence(mdl, coherence="c_npmi")
        ave_coherence_u_mass = coh_u_mass.get_score()
        ave_coherence_c_uci = coh_c_uci.get_score()
        ave_coherence_c_v = coh_c_v.get_score()
        ave_coherence_c_npmi = coh_c_npmi.get_score()
        topics_coherence = [
            num_topics,
            ave_coherence_u_mass,
            ave_coherence_c_uci,
            ave_coherence_c_v,
            ave_coherence_c_npmi,
        ]
        with open(cohs_path, "w") as output_json:
            json.dump(topics_coherence, output_json)
    else:
        with open(cohs_path, "r") as output_json:
            topics_coherence = json.load(output_json)
    print(
        f"The coherence for {str(topics_coherence[0]).zfill(4)} topics: {round(topics_coherence[1], 3)}"
    )
    return topics_coherence


def create_topic_model(
    target_label: str,
    topic_model_path: Path,
    num_topics: int,
    hyperparameter_testing=False,
    hyperparameter_override_list=False,
):
    topic_model_num_path = topic_model_path / f"{target_label}_{str(num_topics).zfill(4)}_topics"
    target_num_label = f"{target_label}_{str(num_topics).zfill(4)}"
    corp_path = topic_model_path / f"{target_label}_corpus.tomotopy"
    ldam_path = topic_model_num_path / f"{target_num_label}_lda_model.ldam"
    cohs_path = topic_model_path / f"{target_label}_lda_model_coherence.json"
    if hyperparameter_testing:
        test_lda_parameters(ldam_path, corp_path, cohs_path, num_topics, hyperparameter_testing)
    elif hyperparameter_override_list:
        topic_model_num_path.mkdir(parents=True, exist_ok=True)
        create_lda_model(ldam_path, corp_path, cohs_path, num_topics, hyperparameter_override_list)
    else:
        topic_model_num_path.mkdir(parents=True, exist_ok=True)
        create_lda_model(ldam_path, corp_path, num_topics)
