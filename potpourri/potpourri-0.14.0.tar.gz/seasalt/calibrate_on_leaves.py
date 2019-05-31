# Re-Calibrate the Probabilities
# https://gdmarmerola.github.io/probability-calibration/
from sklearn.base import BaseEstimator, ClassifierMixin
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder
from sklearn.linear_model import LogisticRegression


class CalibrateOnLeaves(BaseEstimator, ClassifierMixin):
    def __init__(self, model):
        self.model = model
        self.calibr = []

    def fit(self, X, y, **fit_params):
        # fit the base estimator
        self.model.fit(X, y, **fit_params)
        # multi-output vs single target
        self.n_targets_ = 1 if len(y.shape) is 1 else y.shape[1]
        ytmp = y.reshape(-1, 1) if self.n_targets_ is 1 else y
        # calibrate each target seperatly
        for i in range(self.n_targets_):
            self.calibr.append(Pipeline(steps=[
                ('dum', OneHotEncoder(categories='auto')),
                ('lr', LogisticRegression(solver='sag', fit_intercept=False))
            ]))
            lid = self.model.apply(X)  # leaf IDs
            lid = lid.reshape(-1, 1) if len(lid.shape) is 1 else lid
            self.calibr[i].fit(lid, ytmp[:, i])
        # other copying
        if hasattr(self.model, 'feature_importances_'):
            self.feature_importances_ = self.model.feature_importances_

    def predict_proba(self, X):
        y_pred = []
        for i in range(self.n_targets_):
            lid = self.model.apply(X)  # leaf IDs
            lid = lid.reshape(-1, 1) if len(lid.shape) is 1 else lid
            y_pred.append(self.calibr[i].predict_proba(lid))
        # done
        return y_pred[0] if self.n_targets_ is 1 else y_pred

    def predict(self, X):
        return self.model.predict(X)

    def score(self, X, y):
        return self.model.score(X, y)
