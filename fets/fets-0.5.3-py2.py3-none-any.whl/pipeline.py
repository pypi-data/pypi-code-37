import pandas as pd
from sklearn.pipeline import Pipeline, FeatureUnion, _transform_one
from sklearn.base import BaseEstimator, TransformerMixin
from joblib import Parallel, delayed

class FeatureUnion2DF(FeatureUnion):
    """Default scikit learn FeatureUnion does not contacenate 
       the different transformers output into a dataframe.

       That is what FeatureUnion2DF does.

       inspired by Michele Lacchia (fixed in 2017-10-28):
       https://signal-to-noise.xyz/post/sklearn-pipeline/

       2018-12-02: Correction made as from scikit-learn 0.20.X _transform_one
       signature changed. _transform_one is an undocumented function.
    """
    def fit_transform(self, X, y=None, **fit_params):
        # non-optimized default implementation; override when a better
        # method is possible
        if y is None:
            # Unsupervised transformation
            return self.fit(X, **fit_params).transform(X)
        else:
            # Supervised transformation
            return self.fit(X, y, **fit_params).transform(X)

    def transform(self, X):
        # self._iter() gets the list of transformers in the (sub)pipeline
        # This is a generator of tuples such as:
        # ('tranform_NAME', transform_FUNCTION(factor=w), Weight(usually None))
        tr_names = [str(tr_name) for tr_name, trans, weight in self._iter()]

        # undocumented function _transform_one has changed from sklearn version 0.20.X:
        # def _transform_one(transformer, X, y, weight, **fit_params)
        #
        Xs = Parallel(n_jobs=self.n_jobs)(
            delayed(_transform_one)(trans, X, None, weight)
            for _, trans, weight in self._iter())

        N = 0
        for X, tr in zip(Xs, tr_names):
            # dataframe case
            if hasattr(X, "columns"):
                X.columns = ["f_"+col+"_"+tr for col in X.columns]
            elif hasattr(X, "name"):
                X.name = "f"+str(N)+"_"+tr
                N += 1

        return pd.concat(Xs, axis=1, join='inner')


class Progressive(BaseEstimator, TransformerMixin):
    """ Transformer of transformer.

        It progressivly apply the transformation of another transformer
        on a timeseries.
    """

    def __init__(self, transformer, null_val=None, chunk_size=1000):
        """ Set the default parameters

            :param transformer: TransformerMixin type transformer
            :param null_val: Value of the undefined values after transformation
            :param chunk_size: number of entries to process at once. all input
            will be transformed but a LUT will be created to fasten the
            process, chunk by chunk.
        """
        self.transformer = transformer
        self.null_value = null_val

    def transform():
        pass

        # --- prepare index chunks
        full_index = input_s.index
        index_step = np.floor(float(len(full_index)) * 0.1)
        index_step = int(index_step)
        if index_step == 0:
            index_step = self.proc_steps

        # --- Interate through the chunks for progreesive transformation
        a = 0
        b = 0
        while b < len(full_index):
            chunk_index = full_index[a:b]
            valid_dates = self.full_resolution(input_s.loc[chunk_index])

            # manage null or out of format data on remaining indexes
            # with the fill_date which defaults to pd.NaT
            null_indexes = [v for v in chunk_index if v not in valid_dates.index]
            chunk_nulls = input_s.loc[null_indexes].fillna(self.fill_date)

            # Use the LUT
            transformed_dates_lut = ...
            # Converts to datetime with errors=coerce to have NaT when appropriate
            transformed_dates = valid_dates.apply(lambda x: pd.to_datetime(str(x),
                                            format="%Y%m%d",
                                            errors="coerce"))
            # Feed the LUT map (dict)


        # --- Reindex and Invalidate all other dates
        all_dates = transformed_dates.reindex(input_s.index, fill_value=self.fill_date)
