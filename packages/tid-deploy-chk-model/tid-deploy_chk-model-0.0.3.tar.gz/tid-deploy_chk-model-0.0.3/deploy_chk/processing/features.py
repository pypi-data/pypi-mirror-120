from typing import List

import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin

import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.preprocessing import OneHotEncoder


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
        X = X.reset_index().drop(["index"], axis=1)
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
        X = X.reset_index().drop(self.var_list + ["index"], axis=1)
        X = pd.concat([X, dummies], axis=1)

        return X
