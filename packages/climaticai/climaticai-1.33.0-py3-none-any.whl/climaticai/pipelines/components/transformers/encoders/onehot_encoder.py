"""A transformer that encodes categorical features in a one-hot numeric array."""
import numpy as np
import pandas as pd

from climaticai.pipelines.components.transformers.transformer import Transformer
from climaticai.utils import infer_feature_types
from dask_ml.preprocessing import BlockTransformer
from dask_ml.preprocessing import Categorizer, DummyEncoder
from sklearn.pipeline import make_pipeline

from dask_ml.compose import make_column_transformer, ColumnTransformer
from dask_ml.preprocessing import OneHotEncoder as DaskOneHotEncoder
from dask_ml.wrappers import Incremental
from dask_ml.impute import SimpleImputer
import numpy as np
import dask.array as da
from climaticai.utils import infer_feature_types





class OneHotEncoder(Transformer):
    """A transformer that encodes categorical features in a one-hot numeric array.

    Args:
        top_n (int): Number of categories per column to encode. If None, all categories will be encoded.
            Otherwise, the `n` most frequent will be encoded and all others will be dropped. Defaults to 10.
        features_to_encode (list[str]): List of columns to encode. All other columns will remain untouched.
            If None, all appropriate columns will be encoded. Defaults to None.
        random_seed (int): Seed for the random number generator. Defaults to 0.
    """

    name = "One Hot Encoder"
    hyperparameter_ranges = {}
    """{}"""

    def __init__(
        self,
        top_n=10,
        logical_types = {},
        random_seed=0,
        **kwargs,
    ):
        parameters = {
            "top_n": top_n,
            "logical_types": logical_types
        }
        parameters.update(kwargs)


        super().__init__(
            parameters=parameters, component_obj=None, random_seed=random_seed
        )


    def _get_cat_cols(self, X):
        """Get names of categorical columns in the input DataFrame."""
        return list(X.ww.select(include=["category"], return_schema=True).columns)


    def fit(self, X, y=None):
        """Fits the one-hot encoder component.

        Args:
            X (pd.DataFrame): The input training data of shape [n_samples, n_features].
            y (pd.Series, optional): The target training data of length [n_samples].

        Returns:
            self

        Raises:
            ValueError: If encoding a column failed.
        """
        return self

    def transform(self, X, y=None):
        """One-hot encode the input data.

        Args:
            X (pd.DataFrame): Features to one-hot encode.
            y (pd.Series): Ignored.

        Returns:
            pd.DataFrame: Transformed data, where each categorical feature has been encoded into numerical columns using one-hot encoding.
        """
        top_n = self.parameters['top_n']
        logical_types = self.parameters['logical_types']
        X = infer_feature_types(X, logical_types)

        def get_onehot_cols(X, logical_types):
            X_ww = infer_feature_types(X, logical_types)
            one_hot_columns = X_ww.ww.describe(include=['category'])
            one_hot_columns = list(one_hot_columns.T.reset_index()['index'].values)
            return one_hot_columns

        def get_top_n(Xcol, top_n=top_n):
            return Xcol.value_counts()[0:top_n].values

        def func(X):
            for col in get_onehot_cols(X, logical_types):
                topn = get_top_n(X[col])
                X[col] = np.where(X[col].isin(topn), X[col], 'other')
            return X


        def _fit_transform(X):
            xformer = BlockTransformer(func)

            X_ww = xformer.fit_transform(infer_feature_types(X, logical_types))
            X_ww = infer_feature_types(X_ww, logical_types)

            for col in get_onehot_cols(X, logical_types):
                X_ww[col] = X_ww[col].astype('category')
                X_ww[col] = X_ww[col].cat.as_known()

            column_transformer = make_column_transformer(
                (DaskOneHotEncoder(sparse=False), get_onehot_cols(X, logical_types)),
                remainder='passthrough',
            )

            X_t = column_transformer.fit_transform(X_ww)
            return X_t

        return _fit_transform(X)


