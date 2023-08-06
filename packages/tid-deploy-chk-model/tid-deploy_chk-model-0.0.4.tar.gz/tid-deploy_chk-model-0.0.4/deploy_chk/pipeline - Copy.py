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


class nummonComp_numweekProm(TransformerMixin):
    def __init__(self, ref_year: int, ref_month: int):
        self.ref_year = ref_year
        self.ref_month = ref_month
        self.frac_year = ref_month / 12

    def fit(self, X: pd.DataFrame, Y: pd.Series = None):
        return self

    def transform(self, X: pd.DataFrame, Y: pd.Series = None):
        X = X.copy()

        X["numMonthsCompetition"] = 12 * (
            self.ref_year - X["CompetitionOpenSinceYear"]
        ) + (12 * self.frac_year - X["CompetitionOpenSinceMonth"])
        X["numWeeksPromo"] = 52.178 * (self.ref_year - X["Promo2SinceYear"]) + (
            52.178 * self.frac_year - X["Promo2SinceWeek"]
        )

        return X


class PromoInterval_vars(TransformerMixin):
    def fit(self, X: pd.DataFrame, Y: pd.Series = None):
        X = X.copy()
        X["PromoInterval"] = X["PromoInterval"].fillna("")
        vectorizer = CountVectorizer()
        self.count_vect = vectorizer.fit(X["PromoInterval"])
        return self

    def transform(self, X: pd.DataFrame, Y: pd.Series = None):
        X = X.copy()
        X["PromoInterval"] = X["PromoInterval"].fillna("")
        promonths = self.count_vect.transform(X["PromoInterval"])
        promonths = pd.DataFrame(promonths.todense())
        promonths.columns = [
            "Promomonth_" + i for i in self.count_vect.get_feature_names()
        ]
        X = pd.concat([X, promonths], axis=1)

        return X


class date_var_creation(TransformerMixin):
    def __init__(self, var_list: List[str]):
        self.var_list = var_list

    def fit(self, X: pd.DataFrame, Y: pd.Series = None):
        return self

    def transform(self, X: pd.DataFrame, Y: pd.Series = None):
        X = X.copy()
        for var in self.var_list:
            X[var] = pd.to_datetime(X[var])
            X[var + "_year"] = X[var].dt.year
            X[var + "_month"] = X[var].dt.month
            X[var + "_date"] = X[var].dt.day

        return X


class dummy_creation(TransformerMixin):
    def __init__(self, var_list: List[str]):
        self.var_list = var_list

    def fit(self, X: pd.DataFrame, Y: pd.Series = None):
        X = X.copy()
        X[self.var_list] = X[self.var_list].astype("O")
        enc = OneHotEncoder(handle_unknown="ignore")
        self.encoder = enc.fit(X[self.var_list])
        return self

    def transform(self, X: pd.DataFrame, Y: pd.Series = None):
        X = X.copy()
        X[self.var_list] = X[self.var_list].astype("O")
        dummies = pd.DataFrame(self.encoder.transform(X[self.var_list]).toarray())
        feat_names = self.encoder.get_feature_names(self.var_list)
        dummies.columns = feat_names
        X = X.drop(self.var_list, axis=1)
        X = pd.concat([X, dummies], axis=1)

        return X


regressor = XGBRegressor(
    n_estimators=20,
    max_depth=8,
    learning_rate=0.01,
    subsample=0.8,
    colsample_bytree=0.8,
    gamma=0.0,
    objective="reg:squarederror",
)

sales_pipe = Pipeline(
    [
        ("nummonComp1", nummonComp_numweekProm(2015, 12)),
        ("PromoInterval1", PromoInterval_vars()),
        ("date_var_creation1", date_var_creation(config.model_config.date_vars)),
        ("dummy_creation1", dummy_creation(config.model_config.dummy_vars)),
        ("drop_module", DropFeatures(config.model_config.drop_vars)),
        ("regressor", regressor)
    ]
)
