from typing import List

import joblib
import numpy as np
import pandas as pd
from feature_engine.selection import DropFeatures
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder
from xgboost import XGBRegressor

from deploy_chk.config.core import config

import deploy_chk.processing.features as pp

sales_pipe = Pipeline(
    [
        ("nummonComp1", pp.nummonComp_numweekProm(2015, 12)),
        ("PromoInterval1", pp.PromoInterval_vars()),
        ("date_var_creation1", pp.date_var_creation(config.model_config.date_vars)),
        ("dummy_creation1", pp.dummy_creation(config.model_config.dummy_vars)),
        ("drop_module", DropFeatures(config.model_config.drop_vars)),
        ("regressor", XGBRegressor(
    n_estimators=20,
    max_depth=8,
    learning_rate=0.01,
    subsample=0.8,
    colsample_bytree=0.8,
    gamma=0.0,
    objective="reg:squarederror",
))
    ]
)
