import copy

import numpy as np
import pandas as pd
import os
from sklearn.base import BaseEstimator, TransformerMixin
import joblib


class LogSkewNormalizer(BaseEstimator, TransformerMixin):

    def __init__(self, skew_thresh=4.0, out_col='is_churn'):
        self.skew_thresh = skew_thresh
        self.means = None
        self.stddevs = None
        self.skews = None
        self.skewed_columns = None
        self.mins = None
        self.columns = None
        self.out_col = out_col

    def fit(self, X : pd.DataFrame, y=None):
        if self.out_col is not None:
            DataToMeasure = X.drop(self.out_col,axis=1)
        else:
            DataToMeasure = X

        self.columns = copy.deepcopy(DataToMeasure.columns.values)
        self.mins = DataToMeasure.min()
        self.means = DataToMeasure.mean()
        self.stddevs = DataToMeasure.std()
        self.skews = DataToMeasure.skew()

        self.skewed_columns = (self.skews > self.skew_thresh) & (self.mins >= 0)
        self.skewed_columns=self.skewed_columns[self.skewed_columns]

        S = X.copy()
        if self.out_col is not None:
            S.drop(self.out_col, axis=1, inplace=True)
        for col in self.skewed_columns.keys():
            S[col] = np.log(1.0 + S[col])
            self.means[col] = S[col].mean()
            self.stddevs[col] = S[col].std()


    def transform(self, X, y=None):
        S = X.copy()
        if self.out_col is not None:
            S.drop(self.out_col, axis=1, inplace=True)

        assert all([col in self.columns for col in S.columns])
        S = S[self.columns]

        for col in self.skewed_columns.keys():
            S[col] = np.log(1.0 + S[col])

        S = (S - self.means) / self.stddevs
        if self.out_col is not None:
            S[self.out_col] = X[self.out_col]

        return S


def score_transformer(data_set_path,skew_thresh=4.0):
    assert os.path.isfile(data_set_path),'"{}" is not a valid dataset path'.format(data_set_path)
    churn_data = pd.read_csv(data_set_path,index_col=[0,1])

    churn_data_transformer = LogSkewNormalizer(skew_thresh=skew_thresh)

    churn_data_transformer.fit(churn_data)

    churn_scores = churn_data_transformer.transform(churn_data)

    score_save_path=data_set_path.replace('.csv','_scores.csv')
    print('Saving results to %s' % score_save_path)
    churn_scores.to_csv(score_save_path,header=True)

    transformer_save_path=data_set_path.replace('.csv','_score_transform.pkl')
    print('Saving fit Transformer to %s' % transformer_save_path)
    joblib.dump(churn_data_transformer, transformer_save_path)
