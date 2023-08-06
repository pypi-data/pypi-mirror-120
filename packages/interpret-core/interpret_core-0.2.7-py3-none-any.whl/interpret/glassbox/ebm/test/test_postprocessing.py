# Copyright (c) 2019 Microsoft Corporation
# Distributed under the MIT software license

from ..postprocessing import multiclass_postprocess

from ....test.utils import (
    synthetic_multiclass,
    synthetic_classification,
    adult_classification,
    iris_classification,
)

from sklearn.model_selection import (
    cross_validate,
    StratifiedShuffleSplit,
    train_test_split,
)
from ..ebm import ExplainableBoostingRegressor, ExplainableBoostingClassifier
from ..utils import EBMUtils

import numpy as np


def test_multiclass_postprocess_smoke():
    n = 1000
    d = 2
    k = 3
    b = 10

    X_binned = np.random.randint(b, size=(d, n))
    feature_graphs = []
    for _ in range(d):
        feature_graphs.append(np.random.rand(b, k))

    def binned_predict_proba(X_binned, k=3):
        n = X_binned.shape[1]
        return 1 / k * np.ones((n, k))

    feature_types = ["numeric"] * d
    results = multiclass_postprocess(
        X_binned, feature_graphs, binned_predict_proba, feature_types
    )

    assert "intercepts" in results
    assert "feature_graphs" in results

def valid_ebm(ebm):
    assert ebm.feature_groups_[0] == [0]

    for _, model_feature_group in enumerate(ebm.additive_terms_):
        all_finite = np.isfinite(model_feature_group).all()
        assert all_finite

def _smoke_test_explanations(global_exp, local_exp, port):
    from .... import preserve, show, shutdown_show_server, set_show_addr

    set_show_addr(("127.0.0.1", port))

    # Smoke test: should run without crashing.
    preserve(global_exp)
    preserve(local_exp)
    show(global_exp)
    show(local_exp)

    # Check all features for global (including interactions).
    for selector_key in global_exp.selector[global_exp.selector.columns[0]]:
        preserve(global_exp, selector_key)

    shutdown_show_server()
            
def test_merge_models():
    
    data = adult_classification()
    X = data["full"]["X"]
    y = data["full"]["y"]
    X_te = data["test"]["X"]
    y_te = data["test"]["y"]   
    
    seed =1
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, random_state=seed)
    ebm1 = ExplainableBoostingClassifier(random_state=seed, n_jobs=-1)

    ebm1.fit(X_train, y_train)  

    seed +=10
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, random_state=seed)

    ebm2 = ExplainableBoostingClassifier(random_state=seed, n_jobs=-1)
    ebm2.fit(X_train, y_train)  

    seed +=10
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, random_state=seed)

    ebm3 = ExplainableBoostingClassifier(random_state=seed, n_jobs=-1)
    ebm3.fit(X_train, y_train) 
        
    models = [ebm1, ebm2 , ebm3]
    merged_ebm = EBMUtils.merge_models(models=models)

    ebm_global = merged_ebm.explain_global(name='EBM')
    
    valid_ebm(merged_ebm)

    global_exp = merged_ebm.explain_global()
    local_exp = merged_ebm.explain_local(X_te[:5, :], y_te[:5])

    _smoke_test_explanations(global_exp, local_exp, 6000) 